# scoring.md — how room 02 ranks topics

## Where the topics come from
1. `client.json` → `seed_keywords`.
2. Google autocomplete for each seed (free, no key).
3. With `--paid` only: DataForSEO adds volume and competition for every topic, and for each seed the
   People-Also-Ask questions and the top 3 ranking pages. Cost: one volume call (about $0.075 for up to
   1,000 keywords) plus one SERP call per seed. The script prints the real cost the API reports.

4. Optional: `output/vidiq-<YYYY-MM-DD>.json`, a map of keyword → estimated monthly YouTube searches
   (US). Claude fetches it with the VidIQ tool (uses credits, so ask first) before the run. A script
   cannot call VidIQ, so the file is the hand-off.

## Score
`score = volume × (1 − competition_index ÷ 100) × lane_fit`

| Part | Meaning |
| --- | --- |
| `volume` | Google monthly searches in `client.json` → `location_name`. Unknown = 0. |
| `competition_index` | Google Ads competition, 0–100. A stand-in for how crowded the topic is. Unknown = 50. |
| `lane_fit` | 1.0 if every word of one `lanes` entry is in the topic, 0.5 if some words are, 0.1 if none. Small words (in, for, of, the, a, to, and, my, near, me) do not count. |

Free runs have no volume, so they rank by `lane_fit` only. Treat a free list as a draft.

`youtube_volume` is shown but never scored. Articles must rank on Google; the YouTube number only says
which picked topics are also worth a video later.

## Reading the list
- High score, high lane fit: write it.
- High volume, lane fit 0.1: off-topic for this client. Skip it, even if it is tempting.
- A city word with zero volume is not a topic. Local ranking comes from the Business Profile and NAP.
