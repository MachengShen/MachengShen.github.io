#!/usr/bin/env bash
# Regenerate /llms-full.txt — the self-contained, single-fetch bundle.
# Source of truth is /llms.txt plus the markdown under /theory.
set -euo pipefail
cd "$(dirname "$0")/.."

OUT=llms-full.txt
{
  cat llms.txt
  echo; echo "---"; echo
  echo "# Appendix — full text of the core theory notes"
  echo
  echo "The index above links these; they are inlined here so that a single fetch of"
  echo "/llms-full.txt is sufficient and no crawling is required."
  for f in theory/*.md; do
    echo; echo "---"; echo
    echo "## Source: /$f"
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
} > "$OUT"

echo "wrote $OUT ($(wc -c < "$OUT") bytes, $(wc -l < "$OUT") lines)"
