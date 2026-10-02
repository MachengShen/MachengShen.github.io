#!/usr/bin/env python3
"""Offline integrity check for the site's plain-link public HTML graph."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import deque
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://machengshen.github.io"
NON_PUBLIC = {
    "agent/index.html", "ideas/index.html", "scripts/head-template.html",
    "reports/dharma-v3-review/index.html", "reports/ccd-hcloud-habitat-lens/index.html",
}
EXTERNALLY_SERVED = ("/ideas/",)


class Links(HTMLParser):
    def __init__(self): super().__init__(); self.anchors=[]; self.alternates=[]
    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k,v in attrs}
        if tag.lower() == "a" and "href" in a: self.anchors.append(a["href"])
        if tag.lower() == "link" and "alternate" in a.get("rel", "").lower() and "href" in a:
            self.alternates.append(a["href"])


def url_for(rel: str) -> str:
    if rel == "index.html": return "/"
    if rel.endswith("/index.html"): return "/" + rel[:-10]
    return "/" + rel


def path_for(url: str) -> str:
    p = unquote(urlsplit(url).path).lstrip("/")
    if not p: return "index.html"
    if p.endswith("/"): return p + "index.html"
    return p


def pages() -> dict[str, Path]:
    out = {}
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if rel in NON_PUBLIC or ".git" in p.parts: continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if re.search(r'<meta[^>]+name=["\']robots["\'][^>]+noindex', text[:5000], re.I): continue
        out[url_for(rel)] = p
    return out


def sitemap_html() -> set[str]:
    text = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    return {urlsplit(x).path for x in re.findall(r"<loc>(.*?)</loc>", text) if urlsplit(x).path.endswith(("/", ".html"))}


def resolve(base: str, href: str) -> tuple[str | None, str | None]:
    s = urlsplit(href)
    if s.scheme in {"mailto", "tel", "javascript", "data"}: return None, None
    if s.scheme and s.scheme not in {"http", "https"}: return None, None
    if s.netloc and s.netloc != "machengshen.github.io": return None, None
    absolute = urljoin(SITE + base, href)
    path = urlsplit(absolute).path
    rel = path_for(path)
    return path, rel


def run(check_alternates: bool = True) -> dict:
    public = pages(); graph={u:set() for u in public}; broken=[]; forbidden=[]; alt_broken=[]; crosslink_errors=[]
    for u,p in public.items():
        raw=p.read_text(encoding="utf-8", errors="replace")
        parser=Links(); parser.feed(raw)
        marked=re.search(r'<!-- crosslink:start -->(.*?)<!-- crosslink:end -->',raw,re.S)
        if not marked:
            crosslink_errors.append({"source":u,"error":"missing marked crosslink block"})
        else:
            bp=Links(); bp.feed(marked.group(1)); block_paths={resolve(u,h)[0] for h in bp.anchors}
            expected_hub="/theory-mainline-index.zh.html" if re.search(r'<html[^>]+lang=["\']zh',raw[:1000],re.I) else "/theory-mainline-index.html"
            if u not in {"/theory-mainline-index.html","/theory-mainline-index.zh.html"} and expected_hub not in block_paths:
                crosslink_errors.append({"source":u,"error":"crosslink block lacks language hub"})
            for required in ("/llms.txt","/sitemap.xml"):
                if required not in block_paths: crosslink_errors.append({"source":u,"error":f"crosslink block lacks {required}"})
        for href in parser.anchors:
            target, rel = resolve(u, href)
            if target is None: continue
            if any(target.startswith(prefix) for prefix in EXTERNALLY_SERVED): continue
            if rel in NON_PUBLIC:
                forbidden.append({"source":u,"href":href,"target":rel}); continue
            disk = ROOT / rel
            if target in public: graph[u].add(target)
            elif not disk.exists(): broken.append({"source":u,"href":href,"resolved":target})
        if check_alternates:
            for href in parser.alternates:
                target, rel = resolve(u, href)
                if target is not None and not (ROOT / rel).exists():
                    alt_broken.append({"source":u,"href":href,"resolved":target})
    inbound={u:0 for u in public}
    for targets in graph.values():
        for t in targets: inbound[t]+=1
    orphans=sorted(u for u,n in inbound.items() if not n)
    unreachable=[]; distances=[]; max_hops=0
    for start in public:
        dist={start:0}; q=deque([start])
        while q:
            cur=q.popleft()
            for nxt in graph[cur]:
                if nxt not in dist: dist[nxt]=dist[cur]+1; q.append(nxt)
        for target in public:
            if target == start: continue
            if target not in dist: unreachable.append([start,target])
            else: distances.append(dist[target]); max_hops=max(max_hops,dist[target])
    sm=sitemap_html(); ps=set(public)
    report={
        "page_count":len(public), "pair_count":len(public)*(len(public)-1),
        "reachable_pair_count":len(distances), "min_hops":min(distances) if distances else 0,
        "max_hops":max_hops, "orphans":orphans, "broken_internal_links":broken,
        "links_to_non_public":forbidden, "alternate_targets_missing":alt_broken,
        "crosslink_errors":crosslink_errors,
        "public_only":sorted(ps-sm), "sitemap_only":sorted(sm-ps),
        "unreachable_pairs":unreachable[:100], "unreachable_pair_count":len(unreachable),
    }
    report["ok"] = not any((orphans,broken,forbidden,alt_broken,crosslink_errors,ps-sm,sm-ps,unreachable)) and max_hops <= 3
    return report


def main() -> None:
    ap=argparse.ArgumentParser(); ap.add_argument("--no-alternates", action="store_true"); ap.add_argument("--json")
    args=ap.parse_args(); report=run(not args.no_alternates)
    text=json.dumps(report,ensure_ascii=False,indent=2)
    if args.json: Path(args.json).write_text(text+"\n",encoding="utf-8")
    print(text); raise SystemExit(0 if report["ok"] else 1)


if __name__ == "__main__": main()
