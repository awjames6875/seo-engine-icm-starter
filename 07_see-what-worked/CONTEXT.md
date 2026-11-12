# CONTEXT.md — 07 See What Worked

Last updated: 2026-11-12

## Stage Contract
1. **Inputs:** the list of published slugs (every `06_publish-to-the-blog/output/<slug>/` with `review.md` reviewed),
   `_shared/client.json`, `references/metrics.md`.
2. **Process:** the owner exports four Search Console CSVs into `output/<date>/` (see `references/metrics.md`).
   `py 07_see-what-worked/references/run.py [date]` reads them, ranks each published post as winner, flat or loser
   against its 28-day weekly average, and lists queries the site shows up for but no post covers.
   The Search Console API and open-seo AI-visibility are not wired up yet (needs a Google login and a paid-call OK).
3. **Outputs:** `output/<YYYY-MM-DD>/weekly.md` (winners, losers, new query ideas) and `output/<YYYY-MM-DD>/data.json`.
4. **Human check:** The owner skims `weekly.md`. Its new query ideas feed room 02.

## L3 / L4 folders
- `references/`: constraints. `run.py`, `metrics.md` (which numbers, which windows, what counts as a winner).
- `output/<date>/`: material. One folder per weekly pull.

## Bucket: 30% DATA
The Search Console API and open-seo do the work. The script fetches, compares and sorts.

## Script vs. AI
- Script: fetch, compare week over week, rank, write the report.
- AI: nothing. This room is deterministic.

## Never do this
- Never change a live post from here. Ideas go to room 02 as new runs.
- Never call a paid API without asking.
