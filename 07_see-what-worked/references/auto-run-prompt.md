Run room 07 for run date RUN_DATE. Work only inside this repo. Do not ask questions; there is nobody to answer.

1. Dates. END = RUN_DATE minus 2 days (Search Console lags). 7-day window: END-6 to END. 28-day window: END-27 to END.
2. Pull 4 datasets with COMPOSIO_MULTI_EXECUTE_TOOL, tool GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY,
   site_url "https://www.safeharborbehavioralhealth.com/", row_limit 1000, all 4 in one call:
   - dimensions ["page"], 7-day window   -> pages-7d.csv
   - dimensions ["page"], 28-day window  -> pages-28d.csv
   - dimensions ["query"], 7-day window  -> queries-7d.csv
   - dimensions ["query"], 28-day window -> queries-28d.csv
3. Write each file to 07_see-what-worked/output/RUN_DATE/ with exactly this header:
   pages:   Page,Clicks,Impressions,CTR,Position
   queries: Query,Clicks,Impressions,CTR,Position
   One row per API row: keys[0], clicks, impressions, ctr, position. Quote any value that has a comma.
   If the API returns no rows, write the header only.
4. Run: py 07_see-what-worked/references/run.py RUN_DATE
5. Print one line: how many published posts, how many query ideas, and the path to weekly.md.
   If any step failed, print FAILED and the reason instead. Change nothing else.
