# HANDOFF: Safe Harbor SEO engine + social rooms 08-10 (2026-11-23)

## Start here
Open Claude Code in `C:\Users\1alph\seo-engine-icm-starter`, then say: "Read HANDOFF_STATE.md and continue."
**First thing to do:** check Gmail (safeharbor account) for Apollo's reply on the blind-spot post (thread 1a2090686e4de18a).

## Where things stand
- Done (Part 1, SEO engine reliable):
  - Room 06 `run.py` fetches first and branches from `origin/main`.
  - Sunday autopilot: one article at a time, blog queue first (`tasks/blog-queue.md`), answer mode (no story needed).
  - Fact check by script: `client.json` banned_text now catches couples therapy, evenings, weekends, "adults, ages 5".
  - Headless Sunday run passed (log `_shared/autopilot-logs/2026-11-23-sunday-0955.txt`). Room 07 wrote `07_see-what-worked/output/2026-11-23/weekly.md`.
  - Hook rules ("How NOT to", "5 Ways", "What to Do When") in `_shared/voice.md`.
  - Blind-spot post (`why-motivated-people-still-struggle-blind-spot`) approved by Adam, emailed to Apollo 23 Nov.
- In progress (Part 2, rooms 08-10: article -> carousel, pin, captions, animated Short, post):
  - repo-to-icm teardown done: `C:\Users\1alph\_reference\seo-rooms-08-10\` (MERGE-PLAN.md + 2 TEARDOWN files).
  - Claude corrected 3 wrong claims in it: no Remotion (paid license over 3 people; use `graphics.py stills`), `post_social.py` calls GHL directly with the Adam James Speaks location hard-coded (must become brand-aware), no orchestrator folder (autopilot runs rooms 08-10).
  - Phase C interview (8 points) shown to Adam. Waiting on his yes.

## Next steps (in order)
1. Adam says yes (or fixes) the 8-point interview. (Adam)
2. Claude shows room names 08 `make-the-social-pack`, 09 `make-the-short`, 10 `post-everywhere` with 60/30/10 tags. Adam approves. No files before that. (Claude, then Adam)
3. Build rooms (repo-to-icm Phase E), dry run with a `zz-` slug, then GSD builds the scripts (`_build/gsd-brief.md`). (Claude)
4. When Apollo replies: show Adam, `py 04_expert-reviews-it/references/run.py why-motivated-people-still-struggle-blind-spot --apply`, publish only on Adam's yes. (Claude, then Adam)
5. First full run of rooms 08-10 on the published blind-spot post. AWS render of the Short (paid: ask first). (Claude)

## Waiting on Adam
- Yes on the 8-point interview for rooms 08-10.
- Safe Harbor GHL sub-account: which social accounts are connected; Adam types its API key into `.env.local` himself.
- Apollo's profile URL (`client.json` reviewer.url) and the Saturday hours.
- Whether to commit `_archive/` (old zz- test drafts).

## Key facts
- `_shared/autopilot.json` `state` is null on purpose, so the daily checker will NOT read Apollo's reply. Claude reads it by hand.
- Windows tasks: `SafeHarbor-SEO-Autopilot-Sunday` (Sun 8 AM), `SafeHarbor-SEO-Autopilot-Check` (7, 12, 18). PC must be on.
- Composio Gmail alias `safeharbor` = default sender. Apollo = apollo@safeharborbehavioralhealth.com.
- Repos for rooms 08-10 (MIT, keep notices): `C:\Users\1alph\claude-animation-skills`, `C:\Users\1alph\vox-style-animation`.
- Plan: `C:\Users\1alph\.claude\plans\gentle-snacking-blossom-of-b8af7838-9416-425c-a9fd-7bbfcd056604.md`.
- Nothing posts for Safe Harbor without Adam's yes every time.
- Write JSON/review.md without a BOM (PowerShell `Set-Content -Encoding utf8` adds one and breaks parsing).
- Search Console data starts 2026-11-17. Never delete `public/google4f8af9f121926fc0.html` on the site.
- Site repo: `C:\Users\1alph\safeharbor-behavioral-health\safeharbor-behavioral-health` (work off `origin/main`).
