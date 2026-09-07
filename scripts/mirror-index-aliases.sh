#!/usr/bin/env bash
# Publish /llms.txt at the alias paths agents actually guess.
#
# WHY THIS EXISTS (root cause, 2026-08-22)
# ----------------------------------------
# An external agent was pointed at this site, decided the index was worth
# keeping as a standing data source -- and reached for `/llm.txt`, singular.
# That path returned 404. `/llms.txt` was fine; nobody had ever checked the
# name one character away from it. The index is only as reachable as the URL a
# stranger guesses, and the guess is not always the canonical spelling.
#
# So the canonical file is mirrored, byte for byte, to every path that a
# reasonable agent might try:
#
#   /llm.txt                 the singular. Common typo, common guess.
#   /.well-known/llms.txt    the metadata well-known location, alongside
#                            security.txt. A real if secondary convention; the
#                            root remains canonical.
#
# NOT MIRRORED, deliberately:
#
#   /ai.txt                  In current practice this path means training-data
#                            licensing and opt-out preferences, not a content
#                            index. Answering it with an index would misreport
#                            what the file claims to be, which is worse than
#                            404ing. If an opt-out policy is ever published, it
#                            belongs there -- and it is not this.
#
# Mirrors are copies, not redirects, because GitHub Pages serves static files
# and cannot redirect a .txt; and because an agent that guessed wrong should get
# the content, not a pointer it has to follow. The cost of a copy is drift, so
# check_index.py fails the build if a mirror stops matching its source.
#
# Run this after editing llms.txt. scripts/build-llms-full.sh calls it for you.
set -euo pipefail
cd "$(dirname "$0")/.."

SRC=llms.txt
MIRRORS=(llm.txt .well-known/llms.txt)

for m in "${MIRRORS[@]}"; do
  mkdir -p "$(dirname "$m")"
  cp "$SRC" "$m"
  echo "mirrored $SRC -> $m"
done
