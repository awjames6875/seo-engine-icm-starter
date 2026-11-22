# Metrics

Source: Search Console CSV exports (free, no key). Export four files into `output/<date>/`:
`pages-7d.csv`, `pages-28d.csv`, `queries-7d.csv`, `queries-28d.csv`
(Performance > pick Pages or Queries > set 7 or 28 days > Export > Download CSV, then rename).

| Number | Meaning |
| --- | --- |
| Clicks 7d | clicks on the post's page in the last 7 days |
| Avg weekly clicks (28d) | 28-day clicks / 4 |
| Winner | clicks 7d above 1.2 x the 28-day weekly average |
| Loser | clicks 7d below 0.8 x the 28-day weekly average |
| flat / no data yet | in between / the page is in neither export |
| Query idea | 28-day query with 10 or more impressions whose main words are not all found in an existing post's slug, title or tags |

Only posts whose room 06 `review.md` says `reviewed` are listed.
Not built yet: pulling from the Search Console API and open-seo AI-visibility (needs your Google login and a paid-call OK).
