# Truth Rules

These outrank SEO. A page that breaks one is a finding, never a win. Facts come from `client.json`.

## Rules
1. One office, one phone (`client.json` → `nap.phone`). Other cities are a service area, never a location.
2. Never invent a clinician, license, review, photo, statistic or testimonial.
3. Only the insurance in `client.json` → `insurance_live` may be named as accepted.
4. Only claims the owner can prove: speed, results, volume. If unsure, stop and ask.
5. The business name is spelled exactly as `client.json` → `business_name`.
6. No review or rating schema on the site's own pages (self-serving reviews earn no rich results).

## Banned or flagged text
Each client's list lives in `client.json` → `banned_text`, as `[text, why]` pairs.
`py 01_audit-the-site/references/run.py` flags any page containing one (case-insensitive).
