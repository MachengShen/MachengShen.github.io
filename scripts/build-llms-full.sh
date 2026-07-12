#!/usr/bin/env bash
# Regenerate the self-contained, single-fetch bundles:
#
#   /llms-full.txt     = /llms.txt     + the full text of every theory note
#   /llms-full.zh.txt  = /llms.zh.txt  + the same theory notes
#
# The theory notes are NOT translated per bundle -- an artifact has one text, in
# whichever language it was written in. Only the index wrapped around them
# changes language. The `language:` field in each Source marker says which, so a
# reader is never surprised. That is the case that actually bites here: two of
# the three notes are Chinese and the English index never said so.
#
# Each Source marker carries a sha256 of the file it inlines. check_index.py
# recomputes those hashes. Before, CI only checked that the marker string
# existed, so editing a theory note and forgetting to re-run this script shipped
# a stale bundle with a green build -- /llms-full.txt quietly serving text that
# no longer matched the artifact it claimed to inline. The hash closes that, and
# with two languages it matters more: a stale bundle in one language only is
# worse than no second language at all.
#
# Run this after editing llms.txt, llms.zh.txt, or anything under theory/.
set -euo pipefail
cd "$(dirname "$0")/.."

sha12() {
  if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | cut -c1-12
  else
    sha256sum "$1" | cut -c1-12
  fi
}

# Language of an artifact, from the .llms-i18n manifest. An undeclared artifact
# yields the empty string, which check_index.py rejects -- it cannot silently
# degrade into an unlabelled note, which is the defect this whole field exists
# to prevent.
lang_of() {
  awk -v p="$1" '$1 == p { print $2; exit }' .llms-i18n
}

# $1 = index file heading the bundle, $2 = output path, $3 = "en" | "zh"
build() {
  local index="$1" out="$2" locale="$3"
  {
    cat "$index"
    echo; echo "---"; echo
    if [ "$locale" = "zh" ]; then
      echo "# 附录 —— 核心理论笔记全文"
      echo
      echo "上面的索引链接了这些笔记;它们被内联在这里,好让一次对 /llms-full.zh.txt 的抓取"
      echo "就已足够,无需爬站。每条 Source 标记带上该文件的 sha256,以及它实际使用的语言"
      echo "——笔记本身不随索引翻译,一个 artifact 只有一份正文。"
    else
      echo "# Appendix — full text of the core theory notes"
      echo
      echo "The index above links these; they are inlined here so that a single fetch of"
      echo "/llms-full.txt is sufficient and no crawling is required. Each Source marker"
      echo "carries the sha256 of the file it inlines and the language that file is"
      echo "actually written in — the notes are not translated to match the index, and"
      echo "not every note is in English."
    fi
    for f in theory/*.md; do
      echo; echo "---"; echo
      echo "## Source: /$f (sha256:$(sha12 "$f"), language: $(lang_of "$f"))"
      echo
      grep -v '^<!--' "$f"
    done
    echo; echo "---"; echo
    echo "## Source: Cognition Track graph index"
    echo
    echo "Mirrored from https://github.com/MachengShen/cognition-track (INDEX.md)."
    echo "Machine-readable graph: https://raw.githubusercontent.com/MachengShen/cognition-track/master/manifest.jsonld"
    echo
    # Rewrite the mirror's repo-relative links to absolute URLs; otherwise they
    # resolve against this site's root and 404.
    CT=https://github.com/MachengShen/cognition-track/blob/master
    curl -fsSL --max-time 20 https://raw.githubusercontent.com/MachengShen/cognition-track/master/INDEX.md \
      | sed -E "s#\]\((nodes/[^)]+)\)#](${CT}/\1)#g; s#\]\(root\.md\)#](${CT}/root.md)#g" \
      || echo "_(cognition-track INDEX.md unavailable at build time)_"
  } > "$out"

  echo "wrote $out ($(wc -c < "$out") bytes, $(wc -l < "$out") lines)"
}

build llms.txt    llms-full.txt    en
build llms.zh.txt llms-full.zh.txt zh
