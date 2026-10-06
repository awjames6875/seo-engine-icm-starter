# CONTEXT.md — 01 Audit the Site

Last updated: 2026-10-06

## Stage Contract
1. **Inputs:** a site URL (from `_shared/client.json` → `site_url`, or given by the owner for a new client),
   `_shared/client.json` (the NAP and insurance to check against), `references/checks.md`.
2. **Process:** `references/run.py` crawls the site (sitemap, robots, llms.txt, every page's status,
   title, meta description, H1, JSON-LD, phone numbers found), then merges open-seo and
   Search Console data when keys exist. It sorts findings into a plan: most severe first, then most pages hit.
3. **Outputs:** `output/<slug>/audit.md` (every finding, with the page and evidence),
   `output/<slug>/plan.md` (the prioritized fix list + content gaps + backlink list),
   `output/<slug>/crawl.json` (raw data).
4. **Human check:** The owner reads `plan.md`. Yes = `review.md` says `reviewed`. Then room 02.

## L3 / L4 folders
- `references/`: constraints. `run.py`, `checks.md` (what is checked and how the plan is sorted).
- `output/<slug>/`: material. One folder per audit run.

## Bucket: 60% SCRIPT
`references/run.py` does all of it. Crawling, comparing and scoring are deterministic: same site, same audit.

## Script vs. AI
- Script: crawl, compare NAP to `client.json`, check sitemap URLs return 200, check schema types present,
  sort findings by severity then pages hit, write the files.
- AI: nothing. This room is deterministic.

## Never do this
- Never fix the site from here. This room only reports. Fixes happen on a site branch.
- Never call open-seo or DataForSEO without asking the owner first (paid).
- Never guess a finding. Every line in `audit.md` names the URL and the evidence.
