# CONTEXT.md — 02 Find What to Write

Last updated: 2026-10-06

## Stage Contract
1. **Inputs:** `01_audit-the-site/output/<audit-slug>/plan.md` (content gaps),
   the latest `07_see-what-worked/output/<week>/weekly.md` if one exists,
   `_shared/client.json` (`lanes`, `seed_keywords`), `references/scoring.md`.
2. **Process:** `references/run.py` pulls keyword volume, competition and People-Also-Ask questions
   (open-seo / DataForSEO), plus Search Console queries the site already shows up for. It scores each
   topic and writes a ranked list. The owner picks one and answers the facts questions for it.
3. **Outputs:** `output/topics-<YYYY-MM-DD>.csv` (the ranked list), then for the picked topic:
   `output/<slug>/brief.md` (keyword, questions to answer, lane, competing pages) and
   `output/<slug>/owner-facts.md` (the owner's own facts and story, in their words).
4. **Human check:** The owner picks the topic and fills `owner-facts.md`. Then room 03.

## L3 / L4 folders
- `references/`: constraints. `run.py`, `scoring.md` (score = volume × low competition × lane fit).
- `output/`: material. Topic lists, then one folder per picked article.

## Bucket: 30% DATA
open-seo, DataForSEO and the Search Console API do the work. The script only fetches, scores and sorts.

## Script vs. AI
- Script: fetch keywords and questions, score, sort, write `topics-*.csv` and `brief.md`.
- AI: nothing. The owner picks the topic, not the model.

## Never do this
- Never use a city name as a head keyword unless the data shows real volume. Local match comes from the Business Profile and NAP.
- Never write `owner-facts.md` for the owner. It is their words or it is empty.
- Never call a paid API without asking.
