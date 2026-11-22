# HANDOFF_STATE.md — SEO Engine (ICM Starter)

Saved: 2026-11-17 (Monday)

## Where things stand
| Room | Run | Status |
| --- | --- | --- |
| 01-04 | medicaid-counselors-near-me (audit: 2026-10-06) | reviewed |
| 05 | medicaid-counselors-near-me | auto-pass |
| 06 | medicaid-counselors-near-me | reviewed, published |
| 07 | — | no runs yet |

## Done this session
- Opened PR #1 (`gsd-room-05` -> `main`): rooms 05-07, publish skill, status fix, rule 7.
  https://github.com/awjames6875/seo-engine-icm-starter/pull/1
- Search Console was never set up for safeharborbehavioralhealth.com. Added the property under
  `1alphaj@gmail.com` and verified it with the HTML file method.
- Site PR #5 (adds `public/google4f8af9f121926fc0.html`) merged. **Never delete that file** or Google un-verifies the site.

## Next steps
1. Owner merges PR #1 on seo-engine-icm-starter.
2. Monday 2026-11-24: run room 07. Export `pages-7d.csv`, `pages-28d.csv`, `queries-7d.csv`,
   `queries-28d.csv` from Search Console into `07_see-what-worked/output/2026-11-24/`, then
   `py 07_see-what-worked/references/run.py 2026-11-24`. Owner skims `weekly.md`.
3. New query ideas from `weekly.md` feed room 02 for the next topic.

## Notes
- Search Console only records data from verification day (2026-11-17), so the first report is a thin baseline.
- Search Console API and open-seo AI visibility are not wired up (needs a paid-call OK).
- Site repo: `C:\Users\1alph\safeharbor-behavioral-health` (local `main` is behind origin; use a worktree off `origin/main`).
- Untracked tool folders `.bg-shell/` and `.gsd/` are not part of the pipeline.
