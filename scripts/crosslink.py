#!/usr/bin/env python3
"""Build and apply the site's visible, bilingual cross-link graph.

The checked-in source of truth is data/linkmap.json.  Running this module is
idempotent: it updates one marked body block and additive head metadata only.
"""
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data/linkmap.json"
SITE = "https://machengshen.github.io"
START, END = "<!-- crosslink:start -->", "<!-- crosslink:end -->"
EXCLUDED = {
    "agent/index.html", "ideas/index.html", "scripts/head-template.html",
    "reports/dharma-v3-review/index.html",
    "reports/ccd-hcloud-habitat-lens/index.html",
}


def url_for(rel: str) -> str:
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-len("index.html")]
    return "/" + rel


def rel_for(url: str) -> str:
    path = urlsplit(url).path.lstrip("/")
    if not path:
        return "index.html"
    if path.endswith("/"):
        return path + "index.html"
    return path


def public_files() -> list[Path]:
    out = []
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if rel in EXCLUDED or ".git" in p.parts:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if re.search(r'<meta[^>]+name=["\']robots["\'][^>]+noindex', text[:5000], re.I):
            continue
        out.append(p)
    return out


def _match(text: str, pattern: str) -> str:
    m = re.search(pattern, text, re.I | re.S)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1))).strip()) if m else ""


def facts(p: Path) -> dict:
    text = p.read_text(encoding="utf-8", errors="replace")
    rel = p.relative_to(ROOT).as_posix()
    title = _match(text, r"<title[^>]*>(.*?)</title>") or _match(text, r"<h1[^>]*>(.*?)</h1>") or rel
    lang = _match(text, r"<html[^>]*\blang=[\"']([^\"']+)") or ("zh-Hans" if ".zh." in rel else "en")
    desc = _match(text, r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']')
    if not desc:
        desc = _match(text, r"<main[^>]*>.*?<p[^>]*>(.*?)</p>") or _match(text, r"<p[^>]*>(.*?)</p>")
    desc = desc[:300].rstrip(" ,;:-") or title
    return {"path": rel, "url": url_for(rel), "lang": lang, "title": title, "description": desc}


def counterpart(rel: str, available: set[str]) -> str | None:
    candidates = []
    if rel == "index.html": candidates = ["index.zh.html"]
    elif rel == "index.zh.html": candidates = ["index.html"]
    elif rel == "long-term-memory/index.html": candidates = ["long-term-memory/index.en.html"]
    elif rel == "long-term-memory/index.en.html": candidates = ["long-term-memory/index.html"]
    elif ".zh.html" in rel: candidates = [rel.replace(".zh.html", ".html")]
    elif rel.endswith(".html"): candidates = [rel[:-5] + ".zh.html"]
    if rel.endswith("/index.html") and rel not in {"index.html", "long-term-memory/index.html"}:
        candidates.insert(0, rel[:-10] + "index.zh.html")
    if rel.endswith("/index.zh.html"):
        candidates.insert(0, rel.replace("/index.zh.html", "/index.html"))
    return next((x for x in candidates if x in available), None)


def group_for(rel: str) -> str:
    if rel.startswith("safety/"): return "Safety and verification"
    if rel.startswith("charter/"): return "Human-agent coexistence"
    if rel.startswith("research/"): return "Learning and physical credit"
    if rel.startswith("essays/"): return "Agent architectures and learning"
    if rel.startswith(("reports/", "thailand-energy/", "global-climate/", "continual-learning/", "complexity/", "company-architecture/")): return "Other public pages (outside the theory index)"
    if rel.startswith(("tasks/", "sophon/", "long-term-memory/")): return "Other public pages (outside the theory index)"
    if rel.startswith(("pipeline/", "spine/", "whitepaper-agent-native-communication/")) or "agent-comm" in rel or rel in {"substrate.html", "locality-as-protocol.html", "open-source.html", "open-source.zh.html"}: return "Agent systems and protocols"
    if rel in {"index.html", "index.zh.html", "map.html", "map.zh.html", "start-here.html", "start-here.zh.html", "glossary.html", "glossary.zh.html", "theory-mainline-index.html", "theory-mainline-index.zh.html"}: return "Orientation and indexes"
    return "Information, mind, and agency"


def is_tier_b(rel: str) -> bool:
    return group_for(rel) == "Other public pages (outside the theory index)"


def load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def _deny_terms(path: Path | None) -> list[str]:
    if not path:
        return []
    obj = json.loads(path.read_text(encoding="utf-8"))
    values = obj.values() if isinstance(obj, dict) else (obj if isinstance(obj, list) else [])
    return [str(term) for value in values if isinstance(value, list) for term in value if str(term)]


def validate(data: dict, deny_path: Path | None = None) -> None:
    """Reject unsafe or mechanically duplicated link-map prose before rendering."""
    pages = data.get("pages")
    if not isinstance(pages, list):
        raise SystemExit("linkmap check: pages must be a list")
    by_url = {p.get("url"): p for p in pages}
    by_path = {p.get("path"): p for p in pages}
    reasons: dict[str, str] = {}
    stems: dict[str, int] = {}
    errors: list[str] = []
    deny = _deny_terms(deny_path)
    actual_facts = {x["path"]: x for x in (facts(p) for p in public_files())}
    for page in pages:
        path = page.get("path", "<unknown>")
        zh = str(page.get("lang", "")).lower().startswith("zh")
        desc = page.get("description")
        if not isinstance(desc, str) or not desc.strip():
            errors.append(f"{path}: missing directory/llms description")
        for field, text in (("description", desc),):
            if isinstance(text, str):
                for term in deny:
                    if term.casefold() in text.casefold(): errors.append(f"{path}: {field} contains denylist term")
        related = page.get("related")
        if not isinstance(related, list) or not 3 <= len(related) <= 5:
            errors.append(f"{path}: related must contain 3-5 entries")
            continue
        for item in related:
            reason = item.get("reason")
            target = by_url.get(item.get("url"))
            if not isinstance(reason, str) or not reason.strip():
                errors.append(f"{path} -> {item.get('url')}: missing reason")
                continue
            if reason in reasons:
                errors.append(f"{path}: duplicate reason also used by {reasons[reason]}")
            reasons[reason] = path
            length = len(reason) if zh else len(re.findall(r"\b[\w’'-]+\b", reason))
            if length > (45 if zh else 30):
                errors.append(f"{path}: reason too long ({length})")
            for term in deny:
                if term.casefold() in reason.casefold(): errors.append(f"{path}: reason contains denylist term")
            if not target:
                errors.append(f"{path}: unknown related target {item.get('url')}")
                continue
            if page.get("tier") == "A" and target.get("tier") == "B":
                errors.append(f"{path}: Tier A points to Tier B target {target.get('path')}")
            target_zh = str(target.get("lang", "")).lower().startswith("zh")
            if zh != target_zh:
                cp = rel_for(target.get("counterpart") or "")
                if cp and cp in by_path and str(by_path[cp].get("lang", "")).lower().startswith("zh") == zh:
                    errors.append(f"{path}: cross-language target used despite same-language counterpart {cp}")
                marker = "(English)" if zh else "(Chinese)"
                if marker not in str(item.get("title", "")):
                    errors.append(f"{path}: cross-language target lacks {marker} marker")
            meta = actual_facts.get(target.get("path"), {}).get("description", "")
            compact_reason = re.sub(r"\s+", " ", reason)
            compact_meta = re.sub(r"\s+", " ", meta)
            if any(compact_meta[i:i+20] in compact_reason for i in range(max(0, len(compact_meta)-19))):
                errors.append(f"{path}: reason overlaps target meta description by at least 20 characters")
            # Hand-written-prose guards: reject templated, truncated, or garbled reasons.
            words = re.findall(r"[\w’'-]+", reason.lower()) if not zh else []
            if any(a == b for a, b in zip(words, words[1:])):
                errors.append(f"{path}: reason repeats a word ({reason[:50]})")
            if not reason.rstrip().endswith((".", "。", "!", "！", "?", "？")):
                errors.append(f"{path}: reason does not end like a sentence ({reason[-30:]})")
            if words and words[-1].rstrip(".") in {"as", "of", "and", "the", "to", "for", "in", "with", "a", "an", "that", "which", "how", "by", "on", "or", "from", "is", "are"}:
                errors.append(f"{path}: reason ends on a dangling word ({reason[-30:]})")
            if zh and re.search(r"[的与和对在把将为而及或]。?$", reason.rstrip()):
                errors.append(f"{path}: reason ends on a dangling particle ({reason[-12:]})")
            if (zh and len(reason) < 12) or (not zh and len(words) < 7):
                errors.append(f"{path}: reason too short ({reason})")
            if re.match(r"(From |To test |The adjacent mechanism|The argument here meets|Use |For the adjacent|The next conceptual step|This page.s boundary|从“|要检验|相邻机制|可用《|本页留下|对应的机制|相邻的概念|本页的论点|“)", reason):
                errors.append(f"{path}: reason uses a banned template opening ({reason[:30]})")
            stem = " ".join(words[:2]) if words else reason[:4]
            stems[stem] = stems.get(stem, 0) + 1
    for stem, count in stems.items():
        if count > 8:
            errors.append(f"reason opening '{stem}' used {count} times (templated?)")
    if errors:
        raise SystemExit("linkmap check failed:\n- " + "\n- ".join(errors))


def _head_metadata(text: str, page: dict, data: dict, deny: list[str] | None = None) -> str:
    url = page["url"]
    absolute = SITE + url
    lang = page["lang"]
    cp = page.get("counterpart")
    additions = []
    if not re.search(r"<title[^>]*>\s*\S", text, re.I):
        additions.append(f"  <title>{html.escape(page['title'])}</title>")
    if not re.search(r'<meta[^>]+name=["\']description["\']', text, re.I):
        additions.append(f'  <meta name="description" content="{html.escape(page["description"], quote=True)}" />')
    if not re.search(r'<link[^>]+rel=["\']canonical["\']', text, re.I):
        additions.append(f'  <link rel="canonical" href="{absolute}" />')
    if not re.search(r'<link[^>]+rel=["\']alternate["\'][^>]+type=["\']text/plain["\']', text, re.I):
        additions.append('  <link rel="alternate" type="text/plain" href="/llms.txt" />')
    if cp:
        en = cp if lang.lower().startswith("zh") else url
        zh = url if lang.lower().startswith("zh") else cp
        for code, href in (("en", en), ("zh-Hans", zh), ("x-default", en)):
            # Remove stale duplicates for this language, then add one honest target.
            text = re.sub(r'\s*<link\b(?=[^>]*\brel=["\']alternate["\'])(?=[^>]*\bhreflang=["\']' + re.escape(code) + r'["\'])[^>]*>\s*', "\n", text, flags=re.I)
            additions.append(f'  <link rel="alternate" hreflang="{code}" href="{SITE}{href}" />')
    if additions:
        text = text.replace("</head>", "\n" + "\n".join(additions) + "\n</head>", 1)
    # Extend the first parseable JSON-LD object; do not create a second graph.
    pat = re.compile(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.I | re.S)
    matches = list(pat.finditer(text))
    obj = None; match = None
    for m in matches:
        try:
            candidate = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        if isinstance(candidate, dict): obj, match = candidate, m; break
    hub = data["hubs"]["zh" if lang.lower().startswith("zh") else "en"]
    related = [SITE + hub] + [SITE + r["url"] for r in page["related"]]
    obj = obj or {"@context": "https://schema.org", "@type": "Article"}
    obj.setdefault("@context", "https://schema.org")
    obj.setdefault("@type", "Article")
    obj["url"] = absolute; obj["name"] = page["title"]; obj["inLanguage"] = lang
    if url in data["hubs"].values():
        obj["isPartOf"] = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/"}
    else:
        obj["isPartOf"] = {"@type": "CollectionPage", "@id": SITE + hub, "url": SITE + hub}
    obj["relatedLink"] = related
    if cp:
        key = "translationOfWork" if lang.lower().startswith("zh") else "workTranslation"
        obj[key] = {"@type": "CreativeWork", "url": SITE + cp}
    payload = json.dumps(obj, ensure_ascii=False, indent=2)
    # Preserve pre-existing JSON-LD string values while preventing an old
    # private term from becoming a newly added literal merely because the
    # object is re-indented. JSON Unicode escapes decode to the same value.
    for term in deny or []:
        if term and term.casefold() in payload.casefold():
            payload = re.sub(re.escape(term), lambda m: f"\\u{ord(m.group(0)[0]):04x}" + m.group(0)[1:], payload, flags=re.I)
    rendered = '<script type="application/ld+json">\n' + payload + "\n</script>"
    if match:
        text = text[:match.start()] + rendered + text[match.end():]
    else:
        text = text.replace("</head>", "  " + rendered.replace("\n", "\n  ") + "\n</head>", 1)
    return text


def _block(page: dict, data: dict) -> str:
    zh = page["lang"].lower().startswith("zh")
    hub = data["hubs"]["zh" if zh else "en"]
    heading = "全站目录" if page["url"] in data["hubs"].values() else ("相关阅读" if zh else "Related reading")
    lines = [START, '<section class="crosslink" aria-labelledby="crosslink-heading">', f'  <h2 id="crosslink-heading">{heading}</h2>']
    if page["url"] in data["hubs"].values():
        by_group: dict[str, list[dict]] = {}
        for x in data["pages"]: by_group.setdefault(x["group"], []).append(x)
        for group, items in by_group.items():
            label = "其他公开页面（不属于理论索引）" if zh and group.startswith("Other public") else group
            lines += [f"  <h3>{html.escape(label)}</h3>", "  <ul>"]
            for x in items:
                desc = x["description"]
                suffix = " (English)" if zh and not x["lang"].lower().startswith("zh") else ""
                lines.append(f'    <li><a href="{x["url"]}">{html.escape(x["title"] + suffix)}</a> — {html.escape(desc)}</li>')
            lines.append("  </ul>")
    else:
        lines += [f'  <p><a href="{hub}">{"理论主线索引" if zh else "Theory mainline index"}</a> — {"返回全站枢纽与分组目录。" if zh else "Return to the site hub and grouped directory."}</p>', "  <ul>"]
        for r in page["related"]:
            lines.append(f'    <li><a href="{r["url"]}">{html.escape(r["title"])}</a> — {html.escape(r["reason"])}</li>')
        lines.append("  </ul>")
    if page.get("counterpart"):
        label = "English version" if zh else "中文版本"
        lines.append(f'  <p><a href="{page["counterpart"]}">{label}</a></p>')
    lines.append('  <p><a href="/llms.txt">llms.txt</a> · <a href="/sitemap.xml">sitemap.xml</a></p>')
    lines += ["</section>", END]
    return "\n".join(lines)


def apply(deny: list[str] | None = None, only: set[str] | None = None) -> None:
    data = load(); current = {x["path"]: x for x in data["pages"]}
    actual = {p.relative_to(ROOT).as_posix() for p in public_files()}
    if set(current) != actual:
        raise SystemExit(f"linkmap/public-page drift: data-only={sorted(set(current)-actual)}, files-only={sorted(actual-set(current))}")
    for rel, page in current.items():
        if only is not None and rel not in only:
            continue
        p = ROOT / rel; text = p.read_text(encoding="utf-8")
        text = re.sub(r"[ \t]*\n*" + re.escape(START) + r".*?" + re.escape(END) + r"[ \t]*\n*", "\n", text, flags=re.S)
        text = _head_metadata(text, page, data, deny)
        block = _block(page, data)
        marker = "</main>" if "</main>" in text else ("<footer" if "<footer" in text else "</body>")
        text = text.replace(marker, block + "\n" + marker, 1)
        p.write_text(text, encoding="utf-8")


def update_llms() -> None:
    """Append a generated complete-page section without disturbing authored index prose."""
    data = load()
    begin, finish = "<!-- crosslink-pages:start -->", "<!-- crosslink-pages:end -->"
    authored = {}
    entry_re = re.compile(r'\]\((https?://[^)\s]+)\)(?:\s*`([A-Za-z][\w-]*)`)?')
    cleaned = {}
    for filename in ("llms.txt", "llms.zh.txt"):
        raw = (ROOT / filename).read_text(encoding="utf-8")
        raw = re.sub(re.escape(begin) + r".*?" + re.escape(finish) + r"\n?", "", raw, flags=re.S)
        cleaned[filename] = raw
        for u, state in entry_re.findall(raw):
            key = urlsplit(u).path.replace(".zh.", ".").rstrip("/") or "/"
            if state: authored[key] = state
    for filename, zh in (("llms.txt", False), ("llms.zh.txt", True)):
        p = ROOT / filename; text = p.read_text(encoding="utf-8")
        text = re.sub(re.escape(begin) + r".*?" + re.escape(finish) + r"\n?", "", text, flags=re.S)
        present = {urlsplit(u).path.rstrip("/") or "/" for u in re.findall(re.escape(SITE) + r"[^\s)\"<>]*", text)}
        missing = [x for x in data["pages"] if (x["url"].rstrip("/") or "/") not in present]
        lines = [begin, "## 其他公开页面（不属于理论索引）" if zh else "## Other public pages (outside the theory index)", ""]
        intro = ("以下条目补齐站点的公开 HTML 阅读面；列在这里表示可发现，不表示它们是理论主张。" if zh else
                 "These entries complete discovery of the site's public HTML reading surfaces. Listing them here does not present them as theory claims.")
        lines += [intro, ""]
        for x in missing:
            key = x["url"].replace(".zh.", ".").rstrip("/") or "/"
            badge = f" `{authored[key]}`" if key in authored else ""
            lines.append(f"- [{x['title']}]({SITE}{x['url']}){badge} — {x['description']}")
        lines += [finish, ""]
        p.write_text(text.rstrip() + "\n\n" + "\n".join(lines), encoding="utf-8")


def update_index_jsonld() -> None:
    """Keep the typed site graph complete with the same public-page inventory."""
    p = ROOT / "index.jsonld"; obj = json.loads(p.read_text(encoding="utf-8")); data = load()
    graph = [n for n in obj.get("@graph", []) if not str(n.get("id", "")).startswith("crosslink-page:")]
    known = {n.get("url") for n in graph if isinstance(n.get("url"), str)}
    by_path = {x["path"]: x for x in data["pages"]}
    candidates = {}
    index_text = (ROOT / "llms.txt").read_text(encoding="utf-8")
    indexed = {urlsplit(u).path.replace(".zh.", ".") or "/"
               for u in re.findall(r'\]\((https?://[^)\s]+)\)', index_text)
               if u.startswith(SITE)}
    for url in indexed:
        rel = rel_for(url)
        source = by_path.get(rel)
        if source:
            candidates[url] = source
    for url, x in sorted(candidates.items()):
        absolute = SITE + url
        if absolute in known: continue
        graph.append({"id": "crosslink-page:" + url, "@type": "WebPage", "url": absolute,
                      "label": {"en": x["title"]}, "inLanguage": x["lang"]})
    obj["@graph"] = graph
    obj.pop("crosslinkPages", None)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="validate linkmap without rendering")
    ap.add_argument("--deny", type=Path, help="private denylist JSON (path is never stored)")
    args = ap.parse_args()
    validate(load(), args.deny)
    if args.check:
        print(f"linkmap check passed: {len(load()['pages'])} pages")
        return
    apply(_deny_terms(args.deny))
    update_llms()
    update_index_jsonld()
    print(f"crosslinked {len(load()['pages'])} public pages")


if __name__ == "__main__": main()
