#!/usr/bin/env python3
"""Build the two homepages, /index.html and /index.zh.html.

Shares its chrome (head, masthead, footer, language script) with
scripts/build_map.py so the nav and the EN/中文 toggle cannot drift between the
index pages and the homepage — drift there is what makes a bilingual static site
quietly stop being bilingual.

    python3 scripts/build_home.py
"""

from __future__ import annotations

import json
from pathlib import Path

import build_map as B

ROOT = Path(__file__).resolve().parent.parent
MIRROR = "https://theory.clawishmacheng.com/"


def counts() -> dict:
    data = B.load()
    c = {"survived": 0, "speculative": 0, "retired": 0, "total": 0}
    for r in data["records"]:
        c["total"] += 1
        if r.get("state") in c:
            c[r["state"]] += 1
    c["zh"] = sum(1 for r in data["records"] if r.get("zh_native"))
    # Entries that are not claims at all -- the glossary, the start-here page,
    # section overviews. They carry no cognitive state, and saying so is better
    # than letting the three numbers below silently fail to add up to the total.
    c["unstated"] = c["total"] - c["survived"] - c["speculative"] - c["retired"]
    return c


def legend_strip(c: dict, *, is_zh: bool) -> str:
    """The rule, stated as the thing it actually is: a three-value tally over
    the whole program. Putting the counts here means the homepage cannot claim
    more survived work than the index can show."""
    if is_zh:
        rows = [
            ("survived", "survived 已存活", "过了真刀真枪的检验"),
            ("speculative", "speculative 推测", "有意思，但还没挣到"),
            ("retired", "retired 已撤回", "被杀掉了，通常是被作者本人"),
        ]
    else:
        rows = [
            ("survived", "survived", "has passed a real test"),
            ("speculative", "speculative", "untested. Interesting, unearned"),
            ("retired", "retired", "killed, usually by its own author"),
        ]
    items = "".join(
        f'    <li><span class="dot {k}" aria-hidden="true"></span>'
        f'<span class="tally-n">{c[k]}</span>'
        f'<span class="tally-k state {k}">{B.esc(label)}</span>'
        f'<span class="tally-d">{B.esc(desc)}</span></li>\n'
        for k, label, desc in rows
    )
    if is_zh:
        tail = (
            f'  <p class="small tally-note">这 {c["survived"] + c["speculative"] + c["retired"]} 条是主张。'
            f'另有 {c["unstated"]} 条是术语表、导航、综述一类的条目，不构成主张，因此不带状态。</p>\n'
        )
    else:
        tail = (
            f'  <p class="small tally-note">Those {c["survived"] + c["speculative"] + c["retired"]} are claims. '
            f'The other {c["unstated"]} entries — the glossary, the orientation pages, section '
            f'overviews — assert nothing, so they carry no state.</p>\n'
        )
    return f'  <ul class="tally">\n{items}  </ul>\n' + tail


EN_ABOUT = """  <h2>About</h2>
  <img class="portrait" src="/WechatIMG1106.jpeg" alt="Macheng Shen" width="96" height="96" />
  <p>I trained as an engineer and researcher, earned a PhD at MIT, and worked on
  algorithmic research in Silicon Valley startups and at the Shanghai Qi Zhi
  Institute, on foundational algorithms for embodied intelligence.</p>
  <p>I am trying to find a language that describes intelligent behaviour across
  biology and AI without collapsing it into current engineering jargon. That
  means connecting learning, control, multiscale feedback, physical
  implementation, and safety.</p>
  <p>The work runs in three long-term directions: theories of intelligence;
  how AI-native individuals and one-person companies reshape institutions; and
  personal cognition systems &mdash; agents that help people think clearly and
  decide well over long horizons.</p>
"""

ZH_ABOUT = """  <h2>关于我</h2>
  <img class="portrait" src="/WechatIMG1106.jpeg" alt="Macheng Shen" width="96" height="96" />
  <p>工程和研究出身，MIT 博士，之后在硅谷创业公司和上海期智研究院做算法研究，
  方向是具身智能的基础算法。</p>
  <p>我想找到一种语言，能同时描述生物和 AI 里的智能行为，而不必把它们压成
  当下工程圈的黑话。这意味着要把学习、控制、多尺度反馈、物理实现和安全接到一起。</p>
  <p>长期方向有三条：智能的理论；AI 原生的个人和一人公司会把制度改成什么样；
  以及个人认知系统 &mdash;&mdash; 那种能帮人想清楚、并在长时间尺度上做对决定的 agent。</p>
"""


def build(*, is_zh: bool) -> str:
    c = counts()
    path = "/index.zh.html" if is_zh else "/"
    alt = "/" if is_zh else "/index.zh.html"

    if is_zh:
        title = "沈马成 | 信息、学习，以及一个未来怎样才是可达的"
        desc = (
            "一个人的研究计划，从全息和统计力学，一路到意识、机器学习，"
            "再到 agent 原生的制度设计。每一条主张都标了状态：已存活、推测、"
            "或已被作者自己撤回。中英双语。"
        )
    else:
        title = "Macheng Shen — information, learning, and what makes futures reachable"
        desc = (
            "A one-person research program on information, learning, and what makes "
            "futures reachable — from holography and statistical mechanics, through "
            "consciousness and machine learning, to the design of agent-native "
            "institutions. Every claim carries an explicit cognitive state: survived, "
            "speculative, or retired."
        )

    out = [B.head(lang="zh-Hans" if is_zh else "en", title=title, desc=desc, path=path, alt_path=alt)]
    out.append(B.masthead(is_zh=is_zh, current=path, path=path, alt_path=alt))
    out.append('<main class="wrap">')

    if is_zh:
        out.append("  <h1>什么让一个未来是可达的</h1>")
        out.append(
            '  <p class="lede">一个人的研究计划，问的是同一个问题：一个有限的物理系统，'
            "得在自己内部造出什么东西，才够得着一个它想要的未来。一头连着物理，"
            "另一头连着 agent 原生的制度设计。</p>"
        )
        out.append(
            "  <p>这个计划有一条规矩，比里面任何一条主张都重要：<strong>每一条主张都必须"
            "说清自己现在是什么状态</strong>。撤回的东西不删——留在原地址上，"
            "免得它被重新发现、再被提一遍。</p>"
        )
        out.append(legend_strip(c, is_zh=True))
        out.append(
            f'  <div class="notice"><p><strong>中文读者：</strong>全站 {c["total"]} 条产出里，'
            f'{c["zh"]} 条正文本来就是中文或有完整中译，其余英文原文每条都配了中文摘要。'
            "整个索引、导航、术语表都有中文。</p>"
            f'<p>GitHub 在国内不稳，本站有一个内容一致的镜像：'
            f'<a href="{MIRROR}">theory.clawishmacheng.com</a></p></div>'
        )
    else:
        out.append("  <h1>What makes a future reachable</h1>")
        out.append(
            '  <p class="lede">A one-person research program asking one question: what '
            "does a finite physical system have to build inside itself in order to reach "
            "a future it wants. Physics at one end, agent-native institutions at the "
            "other.</p>"
        )
        out.append(
            "  <p>One rule matters more than any claim below it: <strong>every claim "
            "states which of three things it is</strong>. Retired work is not deleted. It "
            "stays at its original URL so it does not get rediscovered and proposed "
            "again.</p>"
        )
        out.append(legend_strip(c, is_zh=False))
        out.append(
            f'  <div class="notice"><p><strong>中文</strong> &mdash; the whole site reads in '
            f'Chinese: <a href="/index.zh.html?lang=zh">中文首页</a> · '
            f'<a href="/map.zh.html?lang=zh">全景索引</a>. '
            f'Mirror reachable from mainland China: <a href="{MIRROR}">theory.clawishmacheng.com</a></p></div>'
        )

    # doors
    if is_zh:
        doors = [
            ("/map.zh.html", "全景索引", f"{c['total']} 条产出，分六层排列，每条带状态、日期和中文摘要。"),
            ("/start-here.zh.html", "从这里开始", "一屏说完整个计划：三条分支，一条认识论规矩。"),
            ("/safety/index.zh.html", "安全是装置的属性", "把安全放在模型外面那层装置上；真在跑的闸门和只写下来的分开标。"),
            ("/glossary.zh.html", "术语表", "这个计划自己造的词，以及哪些词和别的领域撞名了。"),
        ]
    else:
        doors = [
            ("/map.html", "The map", f"All {c['total']} entries in six layers, each with its state, date, and one line."),
            ("/start-here.html", "Start here", "The whole program in one screen: three branches, one epistemic rule."),
            ("/safety/", "Safety is a property of the harness", "Gates that are actually running, kept separate from gates that are only specified."),
            ("/llms.txt", "For agents", "The same index, machine-readable, plus a typed graph and a single-fetch bundle."),
        ]
    out.append('  <div class="doors">')
    for href, t, d in doors:
        out.append(
            f'    <a class="door" href="{B.esc(href)}">'
            f'<span class="door-t">{B.esc(t)}</span>'
            f'<span class="door-d">{B.esc(d)}</span></a>'
        )
    out.append("  </div>")

    # featured essay -- linked, and embedded only on request. The 900px-tall
    # inline PDF viewer that used to open this page is unreadable on a phone and
    # is the first thing a WeChat browser chokes on.
    if is_zh:
        out.append("  <h2>主文</h2>")
        out.append(
            '  <p>《Toward a Theory of Intelligence and Contemporary AI》是这条线目前的总览：'
            "把智能看成一个有限的物理系统，它建立、更新并动用内部结构，"
            "以支撑预测、干预和控制。英文，PDF。</p>"
            '  <p><a href="/essay.pdf">打开 essay.pdf</a></p>'
            '  <details><summary>在页面内直接看</summary>'
            '  <div class="embed-wrap"><embed src="/essay.pdf" type="application/pdf" /></div></details>'
        )
        out.append(ZH_ABOUT)
        out.append(
            '  <p class="small"><a href="/assets/original_raw_prompt.txt">最初那份原始 prompt</a>'
            "仍然公开，供复现；站上不少说法后来已经改成更分层、更谨慎的版本。</p>"
        )
    else:
        out.append("  <h2>Featured essay</h2>")
        out.append(
            "  <p><em>Toward a Theory of Intelligence and Contemporary AI</em> is the "
            "current overview: intelligence as a finite physical system that builds, "
            "updates, and deploys internal structure sufficient for prediction, "
            "intervention, and control.</p>"
            '  <p><a href="/essay.pdf">Open essay.pdf</a></p>'
            '  <details><summary>Read it inline</summary>'
            '  <div class="embed-wrap"><embed src="/essay.pdf" type="application/pdf" /></div></details>'
        )
        out.append(EN_ABOUT)
        out.append(
            '  <p class="small">The <a href="/assets/original_raw_prompt.txt">original raw '
            "prompt</a> stays published for reproducibility. Several claims it seeded have "
            "since been revised into a more careful layered framing.</p>"
        )

    out.append("</main>")
    out.append(B.footer(is_zh=is_zh))
    out.append("</body>\n</html>")
    return "\n".join(out) + "\n"


def main() -> None:
    (ROOT / "index.html").write_text(build(is_zh=False), encoding="utf-8")
    (ROOT / "index.zh.html").write_text(build(is_zh=True), encoding="utf-8")
    c = counts()
    print(f"index.html + index.zh.html written: {c['total']} entries tallied, {c['zh']} Chinese-readable")


if __name__ == "__main__":
    main()
