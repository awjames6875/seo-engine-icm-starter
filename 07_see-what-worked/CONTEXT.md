# CONTEXT.md — 07 See What Worked

Last updated: 2026-10-06

## Stage Contract
1. **Inputs:** the list of published slugs (every `06_publish-to-the-blog/output/<slug>/` with `review.md` reviewed),
   `_shared/client.json`, `references/metrics.md`.
2. **Process:** `references/run.py` pulls the last 7 and 28 days from the Search Console API (clicks, impressions,
   position per page and query) and open-seo rank and AI-visibility data, then ranks posts and finds
   queries the site shows up for but has no post about.
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
