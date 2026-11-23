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

## Autopilot (added 2026-11-22)
On Sundays the autopilot proposes the topic and fills `owner-facts.md` only with lines copied from `_shared/story-bank.md`.
Adam's email YES on the draft is the pick. See `_shared/autopilot-sunday.md`.

## Research order (Adam, 23 Nov 2026: "beat everyone", answer what the public asks)
1. **Questions people ask (free):** `run.py` free mode (Google autocomplete). Optional: a list of questions from "Answer the Public", saved as `output/questions-<YYYY-MM-DD>.md`. People Also Ask needs `--paid`: ask first.
2. **Competitor check (free):** `references/competitors.md` says how. Output: `output/competitors-<YYYY-MM-DD>.md`. Topics in its gaps list rank higher.
3. **vidIQ (ask first, about 5 credits a keyword):** adds the `youtube_volume` column for the video that goes with each post. It tells us YouTube demand only, never Google web ranking.
4. **Answer mode:** with no owner story, the article answers the public's question from `_shared/client.json` facts (see `03_write-the-article/CONTEXT.md`).
Mental health is a high-trust topic: every post names the reviewing therapist (room 04). Nothing here promises a ranking.

## Never do this
- Never use a city name as a head keyword unless the data shows real volume. Local match comes from the Business Profile and NAP.
- Never write `owner-facts.md` for the owner. It is their words or it is empty.
- Never run `--paid` without asking the owner first, every time.
- Never call VidIQ without asking. It spends the owner's credits.
