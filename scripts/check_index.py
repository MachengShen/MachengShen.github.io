#!/usr/bin/env python3
"""Enforce that the index tells agents the truth — in both languages.

The original rule this enforced: anything published on this site must be indexed
in llms.txt, or explicitly listed in .llms-exclude with a reason. An artifact
that is neither is a silent publication -- readable by a human who happens to
find the URL, invisible to an agent handed the index.

Coverage was never the only way to lie, though. The index can also be *complete
and wrong*: it can tell an agent that a claim its author already retracted is
still live. That is what happened -- llms.txt said `retired` for the
wave-equation derivation while index.jsonld said `speculative` for the very same
URL, and nothing checked, because nothing compared the two files. An agent
traversing the graph was being told a dead claim was alive. For an index whose
entire selling point is that cognitive state is load-bearing, that is the worst
failure available, and it went unnoticed for as long as it existed.

Adding a second language multiplies the ways to lie rather than adding one. A
Chinese index that still says `speculative` after the English one retired a claim
is worse than having no Chinese index at all: it does not merely omit the
convention, it actively breaks it. So the invariants below are not "nice to have
before we translate" -- they are the precondition for translating at all.

Run `python3 scripts/check_index.py`. Exit 0 clean, exit 1 with a report.

The invariants, and what each one is defending against:

  INV-1  coverage          a page ships with no index entry           (silent publication)
  INV-2  no dangling links the index points at a file we do not ship  (broken promise)
  INV-3  bundle inlining   llms-full is missing a theory note         ("one fetch" is a lie)
  INV-4  sitemap current   sitemap.xml drifted from the repo
  INV-5  locale set parity an artifact was added to EN and not ZH     (the Chinese index rots)
  INV-6  locale state parity a claim is retired in one language only  (the convention breaks)
  INV-7  state vocabulary  an invented or leaked-in cognitive state
  INV-8  llms.txt <-> jsonld the two indexes disagree                 (this is the live bug)
  INV-9  bundle freshness  a theory note changed, the bundle did not  (stale text, green CI)
  INV-10 hreflang honesty  a language link points at the wrong language
  INV-11 no orphan locales a .zh. file with no canonical sibling
  INV-12 language declared a publishable .md/.pdf with no stated language
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
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

# Surfaces that exist but are not artifacts, so they are never index entries.
MACHINE_SURFACES = {
    "/", "/llms.txt", "/llms-full.txt", "/llms.zh.txt", "/llms-full.zh.txt",
    "/index.jsonld", "/sitemap.xml", "/robots.txt",
}

# The closed vocabulary. Three values, and the whole index leans on them.
STATES = {"survived", "speculative", "retired"}

# The two language editions of the index. English is canonical: /llms.txt never
# redirects and never content-negotiates, because agents fetch it by exact URL.
EN_INDEX = "llms.txt"
ZH_INDEX = "llms.zh.txt"
BUNDLES = {EN_INDEX: "llms-full.txt", ZH_INDEX: "llms-full.zh.txt"}


def canon(url_or_path: str) -> str:
    """Strip the locale infix. `a/b.zh.html` -> `a/b.html`.

    This one-liner is the whole reason the locale is an infix before the final
    suffix (`llms.zh.txt`) rather than a hyphen suffix (`llms-zh.txt`). The
    hyphen already means "another variant of this document" -- llms-full is the
    full variant of llms -- and two orthogonal axes sharing one separator makes
    `llms-full-zh` ambiguous. With the infix, pairing an artifact with its
    translation is a string replace, which is what lets INV-5 and INV-6 be
    written at all.

    Caveat, deliberate: `-en` in `wave-backprop-en.html` is NOT a locale marker.
    It is a legacy part of that artifact's base name, and it stays, because
    llms.txt promises in prose that the retracted claim is kept "at its original
    URL". Its Chinese alternate is therefore `wave-backprop-en.zh.html`, which
    reads oddly and is nonetheless correct. Renaming the file to satisfy a naming
    scheme would break the one guarantee the tombstone exists to make.
    """
    return url_or_path.replace(".zh.", ".")


def url_for(path: Path) -> str:
    """Map a repo path to the URL it is served at."""
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def path_for(url_path: str) -> Path:
    """Inverse of url_for, for site-internal paths."""
    target = ROOT / url_path.lstrip("/")
    if url_path.endswith("/"):
        target = target / "index.html"
    return target


def load_pairs(filename: str) -> list[tuple[str, str]]:
    """Read a `<token>  <value>  # reason` manifest. Blank/# lines skipped."""
    f = ROOT / filename
    if not f.exists():
        return []
    out = []
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        body, _, reason = line.partition("#")
        parts = body.split()
        if not parts:
            continue
        out.append((parts[0], (parts[1] if len(parts) > 1 else reason.strip())))
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


def indexed_urls(text: str) -> set[str]:
    """Every site-internal path this index points at, prose or bullet."""
    urls = set()
    for m in re.finditer(re.escape(SITE) + r"([^\s)\"'<>]*)", text):
        path = m.group(1) or "/"
        urls.add(path.rstrip() or "/")
    return urls


# A bullet: [Title](url) `state` · 中文 — body. State and language marker are
# both optional, and their absence is not an assertion: llms.txt has always
# badged only the claims, not the repos, and inventing a cognitive state for an
# artifact whose author never asserted one would be worse than leaving it blank.
ENTRY_RE = re.compile(
    r"\]\((https?://[^)\s]+)\)"          # the link target
    r"(?:\s*`([A-Za-z][\w-]*)`)?"        # optional cognitive-state badge
    r"(?:\s*·\s*(中文))?"                # optional language marker
)


def entries(text: str) -> dict[str, tuple[str | None, str | None]]:
    """url -> (cognitive state or None, language marker or None)."""
    out: dict[str, tuple[str | None, str | None]] = {}
    for m in ENTRY_RE.finditer(text):
        url, state, lang = m.group(1), m.group(2), m.group(3)
        prev = out.get(url)
        # The same URL can be linked twice (once badged, once in prose). Keep the
        # assertion, not the silence.
        if prev and prev[0] and not state:
            continue
        out[url] = (state, lang)
    return out


def html_lang(path: Path) -> str | None:
    m = re.search(r"<html[^>]*\blang=\"([^\"]+)\"", path.read_text(encoding="utf-8"))
    return m.group(1) if m else None


LINK_RE = re.compile(r"<link\b[^>]*>", re.I)
ATTR_RE = re.compile(r"(\w[\w-]*)\s*=\s*\"([^\"]*)\"")


def alternates(text: str) -> list[tuple[str, str]]:
    """Every <link rel=alternate> that declares a LANGUAGE -> [(hreflang, href)].

    Parsed attribute-wise rather than with one positional regex, because a regex
    that expects `rel` then `hreflang` then `href` in that order silently ignores
    any link written in a different order — and a check you can bypass by moving
    an attribute is not a check. Links with no hreflang (the machine-format
    alternates on the homepage: /llms.txt, /index.jsonld, ...) are alternate
    *representations*, not translations, and are correctly not language links.
    """
    out = []
    for tag in LINK_RE.findall(text):
        attrs = {k.lower(): v for k, v in ATTR_RE.findall(tag)}
        if attrs.get("rel", "").lower() != "alternate":
            continue
        if "hreflang" in attrs and "href" in attrs:
            out.append((attrs["hreflang"], attrs["href"]))
    return out


def declared_language(path: Path, i18n: dict[str, str]) -> str | None:
    """What language is this artifact written in?

    HTML declares its own language in <html lang> and that attribute is
    authoritative. .md and .pdf have nowhere to carry one, so they are declared
    in .llms-i18n. This is the single source of truth that index.jsonld's
    inLanguage is checked against.
    """
    rel = path.relative_to(ROOT).as_posix()
    if path.suffix.lower() == ".html":
        return html_lang(path)
    return i18n.get(rel)


def main() -> int:  # noqa: C901 - one function, one report; splitting it hides the order
    problems: list[str] = []

    en_path = ROOT / EN_INDEX
    if not en_path.exists():
        print(f"FAIL: {EN_INDEX} is missing. It is the entry point; nothing works without it.")
        return 1
    zh_path = ROOT / ZH_INDEX
    if not zh_path.exists():
        print(f"FAIL: {ZH_INDEX} is missing. The index claims a Chinese edition exists.")
        return 1

    en = en_path.read_text(encoding="utf-8")
    zh = zh_path.read_text(encoding="utf-8")
    exclusions = load_pairs(".llms-exclude")
    i18n = dict(load_pairs(".llms-i18n"))

    # Both editions index the site. A file need only appear in one of them --
    # the Chinese alternate of a page is listed in the Chinese index, not the
    # English one, which is exactly what INV-5 is there to keep honest.
    indexed = indexed_urls(en) | indexed_urls(zh)

    # ---- INV-1. Coverage: every publishable artifact is indexed or excluded. ----
    unindexed = []
    for p in discover():
        rel = p.relative_to(ROOT).as_posix()
        if any(fnmatch.fnmatch(rel, g) for g, _ in exclusions):
            continue
        if url_for(p) not in indexed:
            unindexed.append(rel)
    if unindexed:
        problems.append(
            "INV-1. These artifacts are published but absent from both indexes.\n"
            "Index them, or add them to .llms-exclude with a reason:\n"
            + "".join(f"    {r}\n" for r in unindexed)
        )

    # ---- INV-2. No dangling internal links. ----
    dangling = []
    for path in sorted(indexed):
        if path in MACHINE_SURFACES or path.startswith(EXTERNALLY_SERVED):
            continue
        if not path_for(path).exists():
            dangling.append(path)
    if dangling:
        problems.append(
            "INV-2. The index links to paths that do not exist in this repo:\n"
            + "".join(f"    {p}\n" for p in dangling)
        )

    # ---- INV-5. The two language editions index the same artifact set. ----
    # Without this, the Chinese index rots on the first expansion. Guaranteed:
    # someone adds an entry to llms.txt, forgets llms.zh.txt, and the two drift
    # silently forever. Print both directions -- the asymmetry is the diagnosis.
    en_entries, zh_entries = entries(en), entries(zh)
    en_set = {canon(u) for u in en_entries}
    zh_set = {canon(u) for u in zh_entries}
    if en_set != zh_set:
        only_en = sorted(en_set - zh_set)
        only_zh = sorted(zh_set - en_set)
        msg = f"INV-5. {EN_INDEX} and {ZH_INDEX} do not index the same artifacts.\n"
        if only_en:
            msg += f"  In {EN_INDEX}, missing from {ZH_INDEX}:\n" + "".join(f"    {u}\n" for u in only_en)
        if only_zh:
            msg += f"  In {ZH_INDEX}, missing from {EN_INDEX}:\n" + "".join(f"    {u}\n" for u in only_zh)
        problems.append(msg)

    # ---- INV-6. Cognitive state and language agree across the two editions. ----
    # The highest-value check here. A claim cannot be retired in English and
    # still speculative in Chinese: an artifact has ONE cognitive state, and the
    # epistemic layer is not a property of a language.
    state_disagreements = []
    for url, (state, lang) in sorted(en_entries.items()):
        c = canon(url)
        match = next((v for u, v in zh_entries.items() if canon(u) == c), None)
        if match is None:
            continue  # already reported by INV-5
        zstate, zlang = match
        if state != zstate:
            state_disagreements.append(
                f"    {c}\n        {EN_INDEX}: {state or '(no badge)'}   "
                f"{ZH_INDEX}: {zstate or '(no badge)'}"
            )
        if lang != zlang:
            state_disagreements.append(
                f"    {c}\n        language marker differs: "
                f"{EN_INDEX}: {lang or '(none)'}   {ZH_INDEX}: {zlang or '(none)'}"
            )
    if state_disagreements:
        problems.append(
            "INV-6. The two editions disagree about an artifact.\n"
            "A claim retired in one language is retired in every language; the language\n"
            "an artifact is written in does not change with the index pointing at it.\n"
            + "\n".join(state_disagreements) + "\n"
        )

    # ---- INV-7. Cognitive-state vocabulary is closed. ----
    # Catches invented states, and catches cognition-track's own vocabulary
    # (`survived-stress-test`, `raw`) leaking in through a copy-paste.
    jsonld_path = ROOT / "index.jsonld"
    graph = None
    if not jsonld_path.exists():
        problems.append("INV-7. index.jsonld is missing.")
    else:
        try:
            graph = json.loads(jsonld_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            problems.append(f"INV-7. index.jsonld is not valid JSON: {e}")

    bad_states = set()
    for src, ents in ((EN_INDEX, en_entries), (ZH_INDEX, zh_entries)):
        for url, (state, _) in ents.items():
            if state and state not in STATES:
                bad_states.add(f"    {state!r}  ({src}, on {url})")
    if graph:
        for node in graph.get("@graph", []):
            st = node.get("cognitiveState")
            if st and st not in STATES:
                bad_states.add(f"    {st!r}  (index.jsonld, node {node.get('id')})")
        declared = set(graph.get("stateVocabulary", {}).get("values", []))
        if declared != STATES:
            problems.append(
                f"INV-7. index.jsonld stateVocabulary.values is {sorted(declared)}, "
                f"expected {sorted(STATES)}."
            )
    if bad_states:
        problems.append(
            "INV-7. Cognitive states outside the closed vocabulary "
            f"{sorted(STATES)}:\n" + "\n".join(sorted(bad_states)) + "\n"
            "  cognition-track/manifest/v0 uses a different vocabulary "
            "(survived-stress-test / raw).\n"
            "  The mapping is written down in index.jsonld's stateVocabulary. Use it; "
            "do not add a third variant.\n"
        )

    # ---- INV-8. llms.txt and index.jsonld agree. ----
    # These two had already drifted, and nothing compared them. Six artifacts
    # were in llms.txt and absent from the graph, and one URL carried two
    # different cognitive states depending on which file you read.
    if graph:
        node_urls: dict[str, dict] = {}
        for node in graph.get("@graph", []):
            u = node.get("url")
            if u and u.startswith(SITE):
                node_urls[canon(u[len(SITE):] or "/")] = node

        index_site_paths = {
            canon(u[len(SITE):] or "/") for u in en_entries if u.startswith(SITE)
        }
        missing_nodes = sorted(index_site_paths - set(node_urls))
        if missing_nodes:
            problems.append(
                "INV-8. In llms.txt but absent from index.jsonld — an agent traversing\n"
                "the graph cannot see these at all:\n"
                + "".join(f"    {p}\n" for p in missing_nodes)
            )
        orphan_nodes = sorted(set(node_urls) - index_site_paths)
        if orphan_nodes:
            problems.append(
                "INV-8. In index.jsonld but absent from llms.txt:\n"
                + "".join(f"    {p}\n" for p in orphan_nodes)
            )

        # State agreement, where llms.txt actually asserts a state. Silence in
        # llms.txt is not an assertion of "no state" -- only ~2/3 of bullets are
        # badged by long-standing convention -- so it is not a violation for the
        # graph to carry a state the prose index leaves off. A *contradiction* is.
        contradictions = []
        for url, (state, _) in en_entries.items():
            if not (url.startswith(SITE) and state):
                continue
            node = node_urls.get(canon(url[len(SITE):] or "/"))
            if node and node.get("cognitiveState") != state:
                contradictions.append(
                    f"    {url}\n        llms.txt: {state}   "
                    f"index.jsonld ({node.get('id')}): {node.get('cognitiveState')}"
                )
        if contradictions:
            problems.append(
                "INV-8. llms.txt and index.jsonld state DIFFERENT cognitive states for the\n"
                "same URL. One of them is telling agents a retracted claim is still live:\n"
                + "\n".join(contradictions) + "\n"
            )

        # inLanguage must match what the artifact actually declares about itself.
        lang_lies = []
        for p, node in sorted(node_urls.items()):
            if p in MACHINE_SURFACES and p != "/":
                continue
            if p.startswith(EXTERNALLY_SERVED):
                continue  # served by another repo; unverifiable from here
            f = path_for(p)
            if not f.exists():
                continue  # INV-2 owns this
            actual = declared_language(f, i18n)
            stated = node.get("inLanguage")
            if stated is None:
                lang_lies.append(
                    f"    {p}  (node {node.get('id')}) has no inLanguage; the file says {actual!r}"
                )
            elif actual and stated != actual:
                lang_lies.append(
                    f"    {p}  (node {node.get('id')}) says inLanguage={stated!r}, "
                    f"the file itself says {actual!r}"
                )
        if lang_lies:
            problems.append(
                "INV-8. index.jsonld's inLanguage disagrees with the artifact, or is absent.\n"
                "The index is English; the corpus is not. Saying nothing is how an agent ends\n"
                "up handed two-thirds Chinese prose with no warning:\n"
                + "\n".join(lang_lies) + "\n"
            )

        # A translation must exist, and must not claim to be its own original.
        for node in graph.get("@graph", []):
            wt = node.get("workTranslation")
            if not wt:
                continue
            if not wt.startswith(SITE):
                continue
            t = path_for(wt[len(SITE):])
            if not t.exists():
                problems.append(
                    f"INV-8. node {node.get('id')} declares workTranslation {wt}, "
                    "which this repo does not ship."
                )
            elif node.get("inLanguage") and declared_language(t, i18n) == node["inLanguage"]:
                problems.append(
                    f"INV-8. node {node.get('id')} declares a workTranslation in the same "
                    f"language as itself ({node['inLanguage']}). That is not a translation."
                )

    # ---- INV-3 + INV-9. The bundles inline the theory notes, and are current. ----
    # INV-3 used to check only that the marker string was present. So editing a
    # theory note and forgetting to rebuild shipped a stale bundle with a green
    # build: /llms-full.txt served text that no longer matched the artifact it
    # claimed to inline, and the "one fetch, no crawling" promise quietly became
    # "one fetch, of something else". The hash is what actually closes it.
    for index_name, bundle_name in BUNDLES.items():
        bundle = ROOT / bundle_name
        if not bundle.exists():
            problems.append(f"INV-3. {bundle_name} is missing. Run scripts/build-llms-full.sh.")
            continue
        body = bundle.read_text(encoding="utf-8")
        head = (ROOT / index_name).read_text(encoding="utf-8")
        if not body.startswith(head):
            problems.append(
                f"INV-9. {bundle_name} does not open with the current {index_name}.\n"
                "    The bundle is stale. Run scripts/build-llms-full.sh."
            )
        for note in sorted((ROOT / "theory").glob("*.md")):
            rel = note.relative_to(ROOT).as_posix()
            digest = hashlib.sha256(note.read_bytes()).hexdigest()[:12]
            lang = i18n.get(rel, "")
            marker = f"## Source: /{rel} (sha256:{digest}, language: {lang})"
            if marker not in body:
                stale = f"## Source: /{rel} (sha256:" in body
                problems.append(
                    f"INV-9. {bundle_name} does not inline the current {rel}.\n"
                    + (
                        "    It inlines an older revision of it — the bundle is serving text\n"
                        "    that no longer matches the artifact.\n"
                        if stale
                        else "    The note is not inlined at all; 'one fetch, no crawling' is a lie.\n"
                    )
                    + "    Run scripts/build-llms-full.sh."
                )

    # ---- INV-12. Every publishable .md/.pdf declares a language. ----
    # Same doctrine as .llms-exclude: silence is not an option. HTML declares its
    # own language in <html lang>; markdown and PDF have nowhere to put one, so
    # they say it in .llms-i18n or they do not ship.
    undeclared = []
    for p in discover():
        rel = p.relative_to(ROOT).as_posix()
        if any(fnmatch.fnmatch(rel, g) for g, _ in exclusions):
            continue
        if p.suffix.lower() == ".html":
            if html_lang(p) is None:
                undeclared.append(f"    {rel}  (no <html lang> attribute)")
        elif rel not in i18n:
            undeclared.append(f"    {rel}  (not listed in .llms-i18n)")
    if undeclared:
        problems.append(
            "INV-12. These published artifacts do not say what language they are in:\n"
            + "\n".join(undeclared) + "\n"
        )

    # ---- INV-10. hreflang points at the language it claims, and points back. ----
    # One-way hreflang is the classic rot: page A says "my Chinese version is B",
    # B says nothing, a crawler treats them as unrelated duplicates, and the
    # translation is invisible. Worse is an hreflang="en" aimed at a page written
    # in Chinese, which is a lie told directly to the machines this site is for.
    for p in discover():
        if p.suffix.lower() != ".html":
            continue
        rel = p.relative_to(ROOT).as_posix()
        alts = alternates(p.read_text(encoding="utf-8"))
        if not alts:
            continue
        self_url = SITE + url_for(p)
        for tag, href in alts:
            if not href.startswith(SITE):
                problems.append(f"INV-10. {rel}: alternate {href} is not on this site.")
                continue
            target = path_for(href[len(SITE):])
            if not target.exists():
                problems.append(
                    f"INV-10. {rel}: hreflang=\"{tag}\" points at {href}, which does not exist."
                )
                continue
            if target.suffix.lower() != ".html":
                continue  # a language link to a non-page; existence is all we can check
            # The target must actually be in the language the link claims. An
            # hreflang="en" aimed at a page written in Chinese is a lie told
            # directly to the machines this site exists to serve.
            if tag != "x-default":
                actual = html_lang(target) or ""
                if actual.split("-")[0].lower() != tag.split("-")[0].lower():
                    problems.append(
                        f"INV-10. {rel}: hreflang=\"{tag}\" points at {href}, "
                        f"but that page declares lang=\"{actual}\"."
                    )
            # ...and it must point back with a LANGUAGE-tagged alternate, or the
            # pair is invisible to crawlers. x-default does not count as pointing
            # back: every page in a set names the same x-default, so accepting it
            # would let a one-way hreflang pass as reciprocal — which is exactly
            # the rot this check exists to catch.
            back = [h for t2, h in alternates(target.read_text(encoding="utf-8")) if t2 != "x-default"]
            if href != self_url and self_url not in back:
                problems.append(
                    f"INV-10. {rel} declares an alternate at {href}, but that page does not\n"
                    f"    declare a language-tagged alternate back at {self_url}.\n"
                    "    One-way hreflang does not pair; a crawler reads them as unrelated."
                )

    # ---- INV-11. No orphan locale files. ----
    # `.zh.` means "the Chinese edition of the file next to me". If that file is
    # not there, the name is a promise nothing keeps.
    for p in discover():
        rel = p.relative_to(ROOT).as_posix()
        if ".zh." not in rel:
            continue
        sibling = ROOT / canon(rel)
        if not sibling.exists():
            problems.append(
                f"INV-11. {rel} is a locale variant with no canonical sibling.\n"
                f"    Expected {canon(rel)} to exist."
            )
        if not (html_lang(p) or "").startswith("zh") and p.suffix.lower() == ".html":
            problems.append(
                f"INV-11. {rel} carries the .zh. locale infix but declares "
                f"lang=\"{html_lang(p)}\"."
            )

    # ---- INV-4. sitemap.xml must be current. ----
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.exists():
        problems.append("INV-4. sitemap.xml is missing. Run scripts/gen_sitemap.py.")
    else:
        sys.path.insert(0, str(ROOT / "scripts"))
        from gen_sitemap import render  # noqa: E402

        if sitemap.read_text(encoding="utf-8").strip() != render().strip():
            problems.append("INV-4. sitemap.xml is stale. Run scripts/gen_sitemap.py.")

    if problems:
        print("Index integrity check FAILED.\n")
        for i, p in enumerate(problems, 1):
            print(f"{i}. {p}")
        print(
            "Why this matters: the site's contract is that /llms.txt is a complete and\n"
            "truthful index, in every language it is published in. An unindexed page breaks\n"
            "that contract silently; a stale cognitive state breaks it loudly, by telling an\n"
            "agent that a claim its author already retracted is still standing."
        )
        return 1

    n = len(discover())
    zh_files = sum(1 for p in discover() if ".zh." in p.name)
    print(
        f"Index integrity OK — {n} artifacts ({zh_files} locale variants), "
        f"indexed in {len(BUNDLES)} languages or excluded with a reason.\n"
        "  Cognitive states agree across llms.txt, llms.zh.txt, and index.jsonld."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
