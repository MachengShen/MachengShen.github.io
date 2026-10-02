# MachengShen.github.io

Personal site.

## Essay publishing
- Put the original essay PDF at repository root as `essay.pdf`.
- The homepage embeds `essay.pdf` by default and also links it directly.
## Offline site-link integrity

`python3 scripts/crosslink.py` idempotently applies the checked-in graph in
`data/linkmap.json`. `python3 scripts/crawl_check.py` then verifies, without
network access, that the sitemap and public HTML set agree, ordinary links are
not broken, language alternates exist, and every public page reaches every
other public page within three hops.
