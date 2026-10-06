# CONTEXT.md — 05 Add Search Markup

Last updated: 2026-10-06

## Stage Contract
1. **Inputs:** `04_expert-reviews-it/output/<slug>/approved.md`, `_shared/client.json`
   (author, reviewer, publisher, site URL), `references/post-format.md`.
2. **Process:** `references/run.py` turns the approved draft into one blog post file in the site's format,
   with author (the owner, Person), reviewedBy (the expert reviewer), FAQ pairs, date, read time, related posts and
   internal links, plus the line to add to `/llms.txt`.
3. **Outputs:** `output/<slug>/<slug>.md` (the post file, ready to drop into the site repo),
   `output/<slug>/llms-line.txt`, `output/<slug>/checks.txt` (what was validated).
4. **Human check:** None. Flows straight to room 06, which has the preview check.

## L3 / L4 folders
- `references/`: constraints. `run.py`, `post-format.md` (the frontmatter fields the site's blog loader reads).
- `output/<slug>/`: material. The finished post file.

## Bucket: 60% SCRIPT
`references/run.py` does all of it. Reformatting and computing read time are deterministic.

## Script vs. AI
- Script: frontmatter, read time, related posts by shared tags, FAQ extraction, llms line, validation.
- AI: nothing. This room is deterministic.

## Never do this
- Never change a word of the approved body. Markup only.
- Never write `review.md` here as a human approval. This room has no human check.
