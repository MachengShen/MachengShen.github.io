#!/usr/bin/env python3
"""Smoke gate for the bilingual index: serve the worktree, walk every internal
link, and shoot the pages at both target widths.

Run from the repo root with a server already on 127.0.0.1:8777, or let it start
one:

    python3 scripts/smoke.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://127.0.0.1:8777"
PAGES = ["/index.html", "/index.zh.html", "/map.html", "/map.zh.html",
         "/start-here.html", "/start-here.zh.html",
         "/glossary.html", "/glossary.zh.html"]
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SHOTS = Path("/tmp/mgs-smoke")

# /ideas/ is served by a separate repository and shadows this folder entirely,
# so its targets cannot be resolved from here. Everything else must resolve.
UNVERIFIABLE = ("/ideas/",)

fails: list[str] = []
notes: list[str] = []


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs: list[str] = []
        self.srcs: list[str] = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "a" and d.get("href"):
            self.hrefs.append(d["href"])
        if tag in ("img", "script", "embed") and d.get("src"):
            self.srcs.append(d["src"])
        if tag == "link" and d.get("href"):
            self.srcs.append(d["href"])


def fetch(path: str) -> tuple[int, str]:
    try:
        with urllib.request.urlopen(BASE + path, timeout=10) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:  # noqa: BLE001
        return 0, str(e)


def main() -> int:
    SHOTS.mkdir(exist_ok=True)

    # ---- 1. every page serves, and its structured data parses ----------------
    bodies: dict[str, str] = {}
    for p in PAGES:
        code, body = fetch(p)
        if code != 200:
            fails.append(f"{p} -> HTTP {code}")
            continue
        bodies[p] = body
        for blob in re.findall(r'<script type="application/ld\+json">(.*?)</script>', body, re.S):
            try:
                json.loads(blob)
            except json.JSONDecodeError as e:
                fails.append(f"{p}: invalid JSON-LD ({e})")

    # ---- 2. every internal link and asset resolves ---------------------------
    checked: set[str] = set()
    dangling: list[str] = []
    for p, body in bodies.items():
        lk = Links()
        lk.feed(body)
        for href in lk.hrefs + lk.srcs:
            if href.startswith(("http://", "https://", "mailto:", "#", "data:")):
                continue
            target = href.split("#")[0].split("?")[0]
            if not target or not target.startswith("/"):
                continue
            if target.startswith(UNVERIFIABLE):
                continue
            if target in checked:
                continue
            checked.add(target)
            code, _ = fetch(target)
            if code != 200:
                dangling.append(f"{target}  (HTTP {code}, linked from {p})")
    if dangling:
        fails.extend(dangling)
    notes.append(f"internal targets checked: {len(checked)}, dangling: {len(dangling)}")

    # ---- 3. the language toggle actually points somewhere --------------------
    for p, body in bodies.items():
        alts = re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', body)
        if not any(a[0].startswith("zh") for a in alts):
            fails.append(f"{p}: no zh-Hans hreflang")
        if not any(a[0] == "en" for a in alts):
            fails.append(f"{p}: no en hreflang")
        for _, href in alts:
            path = href.replace("https://machengshen.github.io", "") or "/"
            code, _ = fetch(path)
            if code != 200:
                fails.append(f"{p}: hreflang target {path} -> HTTP {code}")

    # ---- 4. the Chinese index really is Chinese ------------------------------
    zh = bodies.get("/map.zh.html", "")
    body_txt = re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", zh, flags=re.S)
    cjk = len(re.findall(r"[一-鿿]", body_txt))
    latin_words = len(re.findall(r"\b[A-Za-z]{4,}\b", body_txt))
    notes.append(f"map.zh.html: {cjk} CJK chars, {latin_words} latin words")
    if cjk < 8000:
        fails.append(f"map.zh.html has only {cjk} CJK characters — abstracts missing?")
    if "中文摘要" not in zh:
        fails.append("map.zh.html: no Chinese abstract disclosures found")

    # ---- 5. no external runtime dependency (WeChat in-app browser) -----------
    for p, body in bodies.items():
        lk = Links()
        lk.feed(body)
        # Only subresources matter here: an <a> to github.com is a link a reader
        # chooses to follow, whereas a stylesheet, script or font from another
        # host is a render-blocking request that a WeChat in-app browser inside
        # mainland China may simply never complete.
        for m in lk.srcs:
            if not m.startswith(("http://", "https://")):
                continue
            if "machengshen.github.io" in m:
                continue
            fails.append(f"{p}: external subresource {m}")
        if "type=\"module\"" in body:
            fails.append(f"{p}: ES module script (breaks older in-app browsers)")

    # ---- 6. screenshots ------------------------------------------------------
    shots = []
    for p in ("/index.zh.html", "/map.zh.html", "/index.html", "/map.html"):
        for w, h, tag in ((390, 1400, "390"), (1280, 1500, "1280")):
            out = SHOTS / f"{p.strip('/').replace('.', '_')}-{tag}.png"
            subprocess.run(
                [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                 f"--screenshot={out}", f"--window-size={w},{h}", BASE + p],
                capture_output=True, timeout=60,
            )
            if out.exists() and out.stat().st_size > 5000:
                shots.append(str(out))
            else:
                fails.append(f"screenshot failed: {p} @ {w}")
    notes.append(f"screenshots: {len(shots)} written under {SHOTS}")

    print("\n".join("  " + n for n in notes))
    if fails:
        print("\nSMOKE GATE FAILED:")
        for f in fails:
            print("  - " + f)
        return 1
    print("\nSMOKE GATE PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
