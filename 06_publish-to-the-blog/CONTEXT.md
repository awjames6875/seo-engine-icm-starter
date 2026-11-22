# CONTEXT.md — 06 Publish to the Blog

Last updated: 2026-11-12

## Stage Contract
1. **Inputs:** `05_add-search-markup/output/<slug>/<slug>.md`, `05_add-search-markup/output/<slug>/llms-line.txt`,
   `_shared/client.json` (`site_repo` path, `blog_dir`), `references/publish.md`.
2. **Process:** `py 06_publish-to-the-blog/references/run.py <slug>` refuses unless room 04 is `reviewed` and room 05
   made the post. In a temporary git worktree it makes branch `blog/<slug>` from `main`, adds the post to the site's
   `src/data/blogPosts.ts`, adds the llms.txt line, runs `npm ci && npm run build`, commits and pushes the branch.
   Vercel builds a preview. The first run also patches the blog page for reviewedBy and FAQ JSON-LD.
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
- Never touch the owner's checked-out branch or uncommitted work. The script works in a temporary worktree.
- Never push if the build fails.
