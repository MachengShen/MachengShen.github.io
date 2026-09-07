#!/usr/bin/env python3
"""Build the bilingual index pages (/map.html, /map.zh.html) and the two homepages.

Why a generator and not two hand-written files: the index has ~40 records in two
languages, and the one thing that must never drift is that the English and the
Chinese index describe the *same set* of artifacts with the *same* cognitive
states. scripts/check_index.py already enforces that invariant across llms.txt
and llms.zh.txt (INV-5, INV-6); generating both HTML pages from one source keeps
the human-facing pages on the same footing instead of relying on someone
remembering to edit both.

Source of truth: data/index-records.json — records, sections, and the Chinese
abstracts, in one file. Edit that, re-run this, commit both outputs.

    python3 scripts/build_map.py
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "index-records.json"
SITE = "https://machengshen.github.io"

STATE_LABEL_EN = {
    "survived": "survived",
    "speculative": "speculative",
    "retired": "retired",
    "none": "",
}
# The three states stay in English on the Chinese page too, with a gloss. They
# are a closed vocabulary the whole site leans on -- translating the token
# itself would make the Chinese index and the English index look like different
# schemes, and an agent reading llms.zh.txt would see a state string that
# appears nowhere in llms.txt.
STATE_LABEL_ZH = {
    "survived": "survived 已存活",
    "speculative": "speculative 推测",
    "retired": "retired 已撤回",
    "none": "",
}


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------
# shared chrome
# --------------------------------------------------------------------------

LANG_SCRIPT = """  <script>
  /* Language preference for a static site, copied verbatim from index.html so
     the two behave identically. Humans get the EN/中 toggle; agents and
     crawlers do not run scripts, so they always land on the English canonical
     and read the hreflang links above. No preference is ever guessed from
     navigator.language -- only an explicit ?lang= sets one. */
  (function () {
    try {
      var doc = document.documentElement;
      var params = new URLSearchParams(location.search);
      var asked = params.get('lang');
      if (asked) {
        localStorage.setItem('lang', asked);
        params.delete('lang');
        var q = params.toString();
        history.replaceState({}, '', location.pathname + (q ? '?' + q : '') + location.hash);
      }
      var GUARD = 'i18n-landed';
      if (sessionStorage.getItem(GUARD) === location.pathname) return;
      var want = localStorage.getItem('lang');
      if (!want) return;
      want = want.slice(0, 2).toLowerCase();
      if (want === doc.lang.slice(0, 2).toLowerCase()) return;
      var alt = document.querySelector('link[rel="alternate"][hreflang^="' + want + '"]');
      if (!alt) return;
      var url = new URL(alt.href);
      if (url.pathname === location.pathname) return;
      sessionStorage.setItem(GUARD, url.pathname);
      location.replace(url.href);
    } catch (e) { /* storage blocked: stay on the page we are on */ }
  })();
  </script>"""


FILTER_SCRIPT = """  <script>
  /* The legend is the filter. Progressive enhancement on purpose: with no JS
     every record is visible and the buttons are absent, which is the correct
     degraded state for an index -- showing less than everything would be the
     failure. */
  (function () {
    var legend = document.querySelector('.legend');
    if (!legend) return;
    legend.hidden = false;
    var recs = Array.prototype.slice.call(document.querySelectorAll('.rec'));
    var on = {survived: true, speculative: true, retired: true};
    legend.addEventListener('click', function (ev) {
      var b = ev.target.closest('button[data-state]');
      if (!b) return;
      var s = b.getAttribute('data-state');
      on[s] = !on[s];
      b.setAttribute('aria-pressed', on[s] ? 'true' : 'false');
      recs.forEach(function (r) {
        var st = r.getAttribute('data-state');
        r.hidden = (st in on) && !on[st];
      });
      document.querySelectorAll('.section').forEach(function (sec) {
        var any = sec.querySelector('.rec:not([hidden])');
        sec.hidden = !any;
      });
    });
  })();
  </script>"""


def head(*, lang: str, title: str, desc: str, path: str, alt_path: str) -> str:
    """`path` and `alt_path` are site-relative, e.g. '/map.html'."""
    is_zh = lang.startswith("zh")
    en_href = SITE + (alt_path if is_zh else path)
    zh_href = SITE + (path if is_zh else alt_path)
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />

  <link rel="canonical" href="{SITE}{path}" />
  <link rel="alternate" hreflang="en" href="{en_href}" />
  <link rel="alternate" hreflang="zh-Hans" href="{zh_href}" />
  <link rel="alternate" hreflang="x-default" href="{en_href}" />

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Macheng Shen" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:url" content="{SITE}{path}" />
  <meta property="og:locale" content="{'zh_CN' if is_zh else 'en_US'}" />
  <meta property="og:image" content="{SITE}/assets/og-card{'.zh' if is_zh else ''}.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(title)}" />
  <meta name="twitter:description" content="{esc(desc)}" />
  <meta name="twitter:image" content="{SITE}/assets/og-card{'.zh' if is_zh else ''}.png" />

  <link rel="alternate" type="text/plain" href="/llms.txt" title="Agent index (llms.txt)" />
  <link rel="alternate" type="text/plain" href="/llms-full.txt" title="Agent index, self-contained" />
  <link rel="alternate" type="application/ld+json" href="/index.jsonld" title="Typed knowledge graph" />

  <link rel="stylesheet" href="/assets/site.css" />
{LANG_SCRIPT}
</head>
<body>"""


NAV_EN = [
    ("/", "Home"),
    ("/map.html", "The map"),
    ("/start-here.html", "Start here"),
    ("/glossary.html", "Glossary"),
    ("/safety/", "Safety"),
    ("/llms.txt", "For agents"),
]
NAV_ZH = [
    ("/index.zh.html", "首页"),
    ("/map.zh.html", "全景索引"),
    ("/start-here.zh.html", "从这里开始"),
    ("/glossary.zh.html", "术语表"),
    ("/safety/index.zh.html", "安全"),
    ("/llms.zh.txt", "给 agent 读"),
]


def masthead(*, is_zh: bool, current: str, path: str, alt_path: str) -> str:
    items = NAV_ZH if is_zh else NAV_EN
    links = "\n".join(
        '        <a href="{}"{}>{}</a>'.format(
            href, ' aria-current="page"' if href == current else "", esc(label)
        )
        for href, label in items
    )
    en_target = alt_path if is_zh else path
    zh_target = path if is_zh else alt_path
    return f"""<header class="masthead">
  <div class="wrap">
    <a class="name" href="{'/index.zh.html' if is_zh else '/'}">Macheng Shen</a>
    <nav aria-label="{'站内导航' if is_zh else 'Site'}">
{links}
    </nav>
    <div class="lang">
      <a href="{en_target}?lang=en" hreflang="en"{'' if is_zh else ' aria-current="true"'}>EN</a>
      <span>/</span>
      <a href="{zh_target}?lang=zh" hreflang="zh-Hans"{' aria-current="true"' if is_zh else ''}>中文</a>
    </div>
  </div>
</header>
"""


def footer(*, is_zh: bool) -> str:
    if is_zh:
        body = (
            "<p>© 2026 沈马成。本站持续修订中:已经过检验的主张、尚未检验的猜想、"
            "以及被作者自己证伪后撤回的主张,分开标注、都不删除。</p>"
            '<p><a href="/llms.zh.txt">llms.zh.txt</a> 是给 AI agent 读的中文索引;'
            '<a href="/index.jsonld">index.jsonld</a> 是同一份索引的结构化图。'
            '联系:<a href="mailto:macshen93@gmail.com">macshen93@gmail.com</a></p>'
        )
    else:
        body = (
            "<p>© 2026 Macheng Shen. Under continuous revision. Claims that have "
            "survived a test, claims that have not been tested, and claims their "
            "own author has since falsified are marked apart and none of them are "
            "deleted.</p>"
            '<p><a href="/llms.txt">llms.txt</a> is the same index for agents; '
            '<a href="/index.jsonld">index.jsonld</a> is the typed graph. '
            'Contact: <a href="mailto:macshen93@gmail.com">macshen93@gmail.com</a></p>'
        )
    return f'<footer class="foot"><div class="wrap">{body}</div></footer>\n'


# --------------------------------------------------------------------------
# records
# --------------------------------------------------------------------------


def render_record(r: dict, *, is_zh: bool) -> str:
    state = r.get("state") or "none"
    label = (STATE_LABEL_ZH if is_zh else STATE_LABEL_EN).get(state, "")
    url = r["url"]
    # On the Chinese page, link to the Chinese edition when one exists.
    href = r.get("zh_url") or url if is_zh else url
    title_main = (r.get("title_zh") or r["title_en"]) if is_zh else r["title_en"]
    title_alt = r["title_en"] if (is_zh and r.get("title_zh")) else (r.get("title_zh") if not is_zh else "")
    line = r.get("one_line_zh") if is_zh else r.get("one_line_en")

    parts = [f'      <li class="rec{" is-retired" if state == "retired" else ""}" data-state="{esc(state)}">']
    parts.append(f'        <span class="dot {esc(state)}" aria-hidden="true"></span>')
    parts.append('        <div class="rec-head">')
    parts.append(f'          <h3 class="rec-title"><a href="{esc(href)}">{esc(title_main)}</a></h3>')
    meta = []
    if label:
        meta.append(f'<span class="state {esc(state)}">{esc(label)}</span>')
    if r.get("date"):
        meta.append(f'<time datetime="{esc(r["date"])}">{esc(r["date"])}</time>')
    if meta:
        parts.append('          <p class="rec-meta">' + "".join(meta) + "</p>")
    if r.get("is_repo"):
        host = url.split("/")[2] + "/" + "/".join(url.split("/")[3:4])
        parts.append(f'          <p class="rec-meta"><span class="ext">{esc(host)}</span></p>')
    parts.append("        </div>")
    if title_alt:
        parts.append(f'        <p class="rec-alt">{esc(title_alt)}</p>')
    if line:
        parts.append(f'        <p class="rec-line">{esc(line)}</p>')

    if is_zh:
        abstract = r.get("abstract_zh")
        native = r.get("zh_native")
        if abstract:
            paras = "".join(f"<p>{esc(p)}</p>" for p in abstract.split("\n") if p.strip())
            parts.append('        <details class="zh-abstract">')
            parts.append("          <summary>中文摘要</summary>")
            parts.append(f"          {paras}")
            if not native:
                parts.append(
                    '          <p class="langnote">正文为英文。以上摘要为中文转写,'
                    "如与原文冲突以原文为准。</p>"
                )
            parts.append("        </details>")
        elif not native:
            parts.append('        <p class="langnote">正文为英文。</p>')

    parts.append("      </li>")
    return "\n".join(parts)


def render_section(sec: dict, records: list[dict], *, is_zh: bool) -> str:
    rows = [r for r in records if r.get("section") == sec["id"]]
    if not rows:
        return ""
    rows.sort(key=lambda r: (r.get("order", 999), r.get("date") or "", r["url"]))
    title = sec["title_zh"] if is_zh else sec["title_en"]
    blurb = sec.get("blurb_zh") if is_zh else sec.get("blurb_en")
    out = [f'  <section class="section" id="{esc(sec["id"])}">']
    out.append(f"    <h2>{esc(title)}</h2>")
    if blurb:
        out.append(f'    <p class="blurb">{esc(blurb)}</p>')
    out.append('    <ul class="spine">')
    out.extend(render_record(r, is_zh=is_zh) for r in rows)
    out.append("    </ul>")
    out.append("  </section>")
    return "\n".join(out)


def render_legend(records: list[dict], *, is_zh: bool) -> str:
    counts = {"survived": 0, "speculative": 0, "retired": 0}
    for r in records:
        s = r.get("state")
        if s in counts:
            counts[s] += 1
    labels = STATE_LABEL_ZH if is_zh else STATE_LABEL_EN
    hint = "点一下可以只看某一类" if is_zh else "Click to filter"
    btns = "\n".join(
        f'    <li><button type="button" class="{s}" data-state="{s}" aria-pressed="true">'
        f'<span class="dot {s}" aria-hidden="true"></span>{esc(labels[s])}'
        f'<span class="count">{counts[s]}</span></button></li>'
        for s in ("survived", "speculative", "retired")
    )
    return (
        f'  <ul class="legend" hidden aria-label="{esc(hint)}">\n{btns}\n  </ul>\n'
    )


def build_map(data: dict, *, is_zh: bool) -> str:
    recs = data["records"]
    path = "/map.zh.html" if is_zh else "/map.html"
    alt = "/map.html" if is_zh else "/map.zh.html"
    if is_zh:
        title = "全景索引 | 沈马成"
        desc = (
            "这个研究计划的全部公开产出,按五层排列:宇宙与信息、智能与记忆、"
            "主体与边界、多主体与共处、工程装置与安全。每一条都标了它现在是什么状态——"
            "已存活、推测、还是已被作者自己撤回——并附中文摘要。"
        )
        h1 = "全景索引"
        intro = data["intro_zh"]
    else:
        title = "The map | Macheng Shen"
        desc = (
            "Everything this research program has published, in five layers: universe "
            "and information, intelligence and memory, agency and boundary, many agents "
            "and coexistence, engineering harness and safety. Every entry carries its "
            "cognitive state — survived, speculative, or retired."
        )
        h1 = "The map"
        intro = data["intro_en"]

    out = [head(lang="zh-Hans" if is_zh else "en", title=title, desc=desc, path=path, alt_path=alt)]
    out.append(masthead(is_zh=is_zh, current=path, path=path, alt_path=alt))
    out.append('<main class="wrap">')
    out.append(f"  <h1>{esc(h1)}</h1>")
    for i, para in enumerate(intro):
        cls = ' class="lede"' if i == 0 else ""
        # Authored copy, written by hand in sections.json -- inline markup is
        # intended and is not escaped. Everything that comes from the record
        # inventory goes through esc() instead.
        out.append(f"  <p{cls}>{para}</p>")
    out.append(render_legend(recs, is_zh=is_zh))
    for sec in data["sections"]:
        s = render_section(sec, recs, is_zh=is_zh)
        if s:
            out.append(s)
    out.append("</main>")
    out.append(footer(is_zh=is_zh))
    out.append(FILTER_SCRIPT)
    out.append("</body>\n</html>")
    return "\n".join(out) + "\n"


def main() -> None:
    data = load()
    (ROOT / "map.html").write_text(build_map(data, is_zh=False), encoding="utf-8")
    (ROOT / "map.zh.html").write_text(build_map(data, is_zh=True), encoding="utf-8")
    n = len(data["records"])
    zh = sum(1 for r in data["records"] if r.get("abstract_zh"))
    print(f"map.html + map.zh.html written: {n} records, {zh} with Chinese abstracts")


if __name__ == "__main__":
    main()
