#!/usr/bin/env python3
"""Enforce that every published artifact is reachable from /llms.txt.

The rule this enforces: anything published on this site must be indexed in
llms.txt, or explicitly listed in .llms-exclude with a reason. An artifact that
is neither is a silent publication -- readable by a human who happens to find
the URL, invisible to an agent handed the index. That gap is the thing this
script exists to close.

Run `python3 scripts/check_index.py`. Exit 0 clean, exit 1 with a report.
"""

from __future__ import annotations

import fnmatch
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://machengshen.github.io"

# Extensions that count as a publication. A .tex source or a .bib file is not a
# published artifact; the .pdf built from it is.
PUBLISHABLE_SUFFIXES = {".html", ".md", ".pdf"}

# Directories we never walk into.
SKIP_DIRS = {".git", ".github", "scripts", "assets", "node_modules"}

# Path prefixes that live on machengshen.github.io but are NOT served by this
# repository. GitHub mounts a repo's own Pages site at /<repo>/ on the user
# page, which shadows any folder of the same name here. Links under these
# prefixes are legitimate, but their targets cannot be verified from this repo.
EXTERNALLY_SERVED = ("/ideas/",)  # served by the separate MachengShen/ideas repo


def url_for(path: Path) -> str:
    """Map a repo path to the URL it is served at."""
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def load_exclusions() -> list[tuple[str, str]]:
    """Read .llms-exclude -> [(glob, reason)]. Blank lines and # comments skipped."""
    f = ROOT / ".llms-exclude"
    if not f.exists():
        return []
    out = []
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        glob, _, reason = line.partition("#")
        out.append((glob.strip(), reason.strip() or "(no reason given)"))
    return out


def discover() -> list[Path]:
    found = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts[:-1]):
            continue
        if p.suffix.lower() in PUBLISHABLE_SUFFIXES:
            found.append(p)
    return sorted(found)


def indexed_urls(llms: str) -> set[str]:
    """Every site-internal path llms.txt points at."""
    urls = set()
    for m in re.finditer(re.escape(SITE) + r"([^\s)\"'<>]*)", llms):
        path = m.group(1) or "/"
        urls.add(path.rstrip() or "/")
    return urls


def main() -> int:
    llms_path = ROOT / "llms.txt"
    if not llms_path.exists():
        print("FAIL: llms.txt is missing. It is the entry point; nothing works without it.")
        return 1
    llms = llms_path.read_text(encoding="utf-8")
    indexed = indexed_urls(llms)
    exclusions = load_exclusions()

    problems: list[str] = []

    # 1. Coverage: every publishable artifact is indexed or excluded-with-reason.
    unindexed = []
    for p in discover():
        rel = p.relative_to(ROOT).as_posix()
        if any(fnmatch.fnmatch(rel, g) for g, _ in exclusions):
            continue
        if url_for(p) not in indexed:
            unindexed.append(rel)
    if unindexed:
        problems.append(
            "These artifacts are published but absent from llms.txt.\n"
            "Index them, or add them to .llms-exclude with a reason:\n"
            + "".join(f"    {r}\n" for r in unindexed)
        )

    # 2. No dangling internal links: llms.txt must not point at files we do not ship.
    dangling = []
    for path in sorted(indexed):
        if path in ("/", "/llms.txt", "/llms-full.txt", "/index.jsonld", "/sitemap.xml", "/robots.txt"):
            continue
        if path.startswith(EXTERNALLY_SERVED):
            continue
        target = ROOT / path.lstrip("/")
        if path.endswith("/"):
            target = target / "index.html"
        if not target.exists():
            dangling.append(path)
    if dangling:
        problems.append(
            "llms.txt links to paths that do not exist in this repo:\n"
            + "".join(f"    {p}\n" for p in dangling)
        )

    # 3. The self-contained bundle must actually inline every theory note,
    #    otherwise "one fetch, no crawling" is a lie.
    full = ROOT / "llms-full.txt"
    if not full.exists():
        problems.append("llms-full.txt is missing. Run scripts/build-llms-full.sh.")
    else:
        body = full.read_text(encoding="utf-8")
        for note in sorted((ROOT / "theory").glob("*.md")):
            marker = f"## Source: /theory/{note.name}"
            if marker not in body:
                problems.append(
                    f"llms-full.txt does not inline theory/{note.name}. "
                    "Run scripts/build-llms-full.sh."
                )

    # 4. sitemap.xml must be current.
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.exists():
        problems.append("sitemap.xml is missing. Run scripts/gen_sitemap.py.")
    else:
        sys.path.insert(0, str(ROOT / "scripts"))
        from gen_sitemap import render  # noqa: E402

        if sitemap.read_text(encoding="utf-8").strip() != render().strip():
            problems.append("sitemap.xml is stale. Run scripts/gen_sitemap.py.")

    if problems:
        print("Index integrity check FAILED.\n")
        for i, p in enumerate(problems, 1):
            print(f"{i}. {p}")
        print(
            "Why this matters: the site's contract is that /llms.txt is a complete\n"
            "index. An unindexed page breaks that contract silently."
        )
        return 1

    n = len(discover())
    print(f"Index integrity OK — {n} artifacts, all indexed or excluded with a reason.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
