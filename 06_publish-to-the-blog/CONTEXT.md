# CONTEXT.md — 06 Publish to the Blog

Last updated: 2026-10-06

## Stage Contract
1. **Inputs:** `05_add-search-markup/output/<slug>/<slug>.md`, `05_add-search-markup/output/<slug>/llms-line.txt`,
   `_shared/client.json` (`site_repo` path, `blog_dir`), `references/publish.md`.
2. **Process:** `references/run.py` makes a branch `blog/<slug>` in the site repo, copies the post
   into the blog folder, adds the llms.txt line, runs the site build, commits and pushes the branch.
   Your host (Vercel, Netlify…) builds a preview.
3. **Outputs:** `output/<slug>/publish-log.md` (branch name, commit, build result, preview URL).
4. **Human check:** The owner opens the preview and approves. He merges the branch. `review.md` says `reviewed`.

## L3 / L4 folders
- `references/`: constraints. `run.py`, `publish.md` (the exact git steps and what to check on the preview).
- `output/<slug>/`: material. The log.

## Bucket: 60% SCRIPT
`references/run.py` does it. Git and build steps are deterministic.

## Script vs. AI
- Script: branch, copy, build, commit, push, log.
- AI: nothing. This room is deterministic.

## Never do this
- Never push to `main` or merge. Only a `blog/<slug>` branch. The owner merges.
- Never touch uncommitted work already in the site repo. Stop and tell the owner if the tree is dirty.
- Never push if the build fails.
