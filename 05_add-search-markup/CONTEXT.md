# CONTEXT.md — 05 Add Search Markup

Last updated: 2026-11-12

## Stage Contract
1. **Inputs:** `04_expert-reviews-it/output/<slug>/approved.md`, `_shared/client.json`
   (author, reviewer, publisher, site URL), `references/post-format.md`.
2. **Process:** `py 05_add-search-markup/references/run.py <slug>` refuses unless room 04's `review.md` says
   `reviewed` and `approved.md` exists. It writes one post file: frontmatter (author, reviewedBy, publisher, FAQ pairs
   from the `## FAQ` section, date, read time, up to 3 related posts by shared tags from the site's `blogPosts.ts`)
   plus the approved body untouched. It also writes the line for `/llms.txt`. It refuses to overwrite a run.
3. **Outputs:** `output/<slug>/<slug>.md` (the post file; room 06 converts it into the site's format),
   `output/<slug>/llms-line.txt`, `output/<slug>/checks.txt` (PASS/FAIL: body unchanged, author, reviewedBy, FAQ count, banned text, internal links).
4. **Human check:** None. Flows straight to room 06, which has the preview check.

## L3 / L4 folders
- `references/`: constraints. `run.py`, `post-format.md` (each frontmatter field, where it comes from, and how room 06 maps it to the site's `BlogPost`).
- `output/<slug>/`: material. The finished post file.

## Bucket: 60% SCRIPT
`references/run.py` does all of it. Reformatting and computing read time are deterministic.

## Script vs. AI
- Script: frontmatter, read time, related posts by shared tags, FAQ extraction, llms line, validation.
- AI: nothing. This room is deterministic.

## Never do this
- Never change a word of the approved body. Markup only.
- Never write `review.md` here as a human approval. This room has no human check.
