# Note for `site/bilingual-redesign`

`/charter/` (the Human–Agent Coexistence Charter, published 2026-09-07) is a
**self-contained** static directory: it inlines its own CSS and does not import
any site-wide layout. It uses the same font stack and the same light/dark tokens
as `/safety/`, so folding it into the redesign should be mechanical — but nothing
in `/charter/` depends on the redesign landing first, and nothing breaks if it
never does.

Two things the redesign should pick up when it converts the site to its shared
layout:

1. The charter pages carry a `@media (prefers-color-scheme: dark)` token block
   that the older pages do not. If the redesign standardises on a single token
   set, take the charter's — it is a superset.
2. The mobile breakpoint at 640px turns the retirement-condition table into
   stacked labelled cards via `td::before { content: attr(data-label) }`. That
   table is nine rows of three columns and is unreadable as a table at 390px, so
   whatever the redesign does with tables must keep an equivalent.

Cross-links between `/charter/` and `/safety/` are already in place in both
directions and in both languages, as is the entry link from `start-here.html`
(branch 3) and the indexing in `llms.txt` / `llms.zh.txt` / `index.jsonld`.

This file lives under `scripts/` because that directory is in `SKIP_DIRS` for
both `check_index.py` and `gen_sitemap.py`, so it is not a published artifact and
needs no index entry.
