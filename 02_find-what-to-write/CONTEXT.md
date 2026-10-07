# CONTEXT.md — 02 Find What to Write

Last updated: 2026-10-07

## Stage Contract
1. **Inputs:** `_shared/client.json` (`seed_keywords`, `lanes`, `location_name`), `references/scoring.md`,
   DataForSEO keys in `.env.local` for paid runs, optional `output/vidiq-<YYYY-MM-DD>.json`
   (YouTube volume, fetched by Claude with the VidIQ tool before the run). Later: new query ideas from room 07's `weekly.md`
   go into `seed_keywords`.
2. **Process:** `references/run.py` expands each seed with Google autocomplete (free). With `--paid` it adds
   DataForSEO volume, competition, People-Also-Ask questions and top pages, and prints the real cost.
   It adds a `youtube_volume` column from the VidIQ file if present (shown, not scored).
   It scores each topic and writes a ranked list. The owner picks one; `run.py --pick "<keyword>"` writes
   the brief and an empty facts sheet. The owner answers the facts questions.
3. **Outputs:** `output/topics-<YYYY-MM-DD>.csv` (the ranked list), then for the picked topic:
   `output/<slug>/brief.md` (keyword, questions to answer, lane, competing pages) and
   `output/<slug>/owner-facts.md` (the owner's own facts and story, in their words).
4. **Human check:** The owner picks the topic and fills `owner-facts.md`. Then room 03.

## L3 / L4 folders
- `references/`: constraints. `run.py`, `scoring.md` (score = volume × low competition × lane fit).
- `output/`: material. Topic lists, then one folder per picked article.

## Bucket: 30% DATA
Google autocomplete and DataForSEO do the work. The script only fetches, scores and sorts.

## Script vs. AI
- Script: fetch keywords and questions, score, sort, write `topics-*.csv` and `brief.md`.
- AI: nothing. The owner picks the topic, not the model.

## Never do this
- Never use a city name as a head keyword unless the data shows real volume. Local match comes from the Business Profile and NAP.
- Never write `owner-facts.md` for the owner. It is their words or it is empty.
- Never run `--paid` without asking the owner first, every time.
- Never call VidIQ without asking. It spends the owner's credits.
