#!/usr/bin/env python3
"""Generate sitemap.xml from what is actually in the repo.

sitemap.xml tells search engines which URLs exist. It is the counterpart to
llms.txt, which tells agents what those URLs are about. Neither replaces the
other, and robots.txt does neither -- it only says who may fetch what.

Run `python3 scripts/gen_sitemap.py` to write sitemap.xml.
Importing `render()` returns the same text without writing, which is how
check_index.py detects staleness.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://machengshen.github.io"

INCLUDE_SUFFIXES = {".html", ".md", ".pdf", ".txt", ".jsonld"}
SKIP_DIRS = {".git", ".github", "scripts", "assets", "node_modules"}
SKIP_FILES = {"robots.txt", "sitemap.xml", "README.md"}


def last_commit_date(path: Path) -> str:
    """Last commit touching this path, as YYYY-MM-DD. Falls back to mtime."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(path.relative_to(ROOT))],
            cwd=ROOT, capture_output=True, text=True, timeout=15, check=True,
        ).stdout.strip()
        if out:
            return out
    except (subprocess.SubprocessError, OSError):
        pass
    import datetime
    return datetime.date.fromtimestamp(path.stat().st_mtime).isoformat()


def url_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return SITE + "/"
    if rel.endswith("/index.html"):
        return SITE + "/" + rel[: -len("index.html")]
    return SITE + "/" + rel


def entries() -> list[tuple[str, str]]:
    out = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file():
            continue
        parts = p.relative_to(ROOT).parts
        if any(part in SKIP_DIRS for part in parts[:-1]):
            continue
        if p.name in SKIP_FILES or p.name.startswith("."):
            continue
        if p.suffix.lower() not in INCLUDE_SUFFIXES:
            continue
        # Drafts and sources are not published surfaces.
        if p.suffix == ".md" and "_draft" in p.name:
            continue
        out.append((url_for(p), last_commit_date(p)))
    return out


def render() -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url, lastmod in entries():
        lines += ["  <url>", f"    <loc>{escape(url)}</loc>",
                  f"    <lastmod>{lastmod}</lastmod>", "  </url>"]
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    (ROOT / "sitemap.xml").write_text(render(), encoding="utf-8")
    print(f"wrote sitemap.xml — {len(entries())} urls")
