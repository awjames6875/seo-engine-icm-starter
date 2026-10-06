# checks.md — what room 01 checks and how each is scored

Severity: **critical** (blocks ranking or is false) · **high** · **medium** · **low**.
Every finding names the URL and the evidence. The script never guesses.

| ID | Severity | Check | Fix to put in plan.md |
| --- | --- | --- | --- |
| CANON-1 | critical | `rel=canonical` missing, or points at a different page than the one fetched | One self-referencing canonical per page. |
| CANON-2 | high | Canonical host is not the `site_url` host (www vs non-www) | Use `site_url` host everywhere. |
| CANON-3 | medium | `og:url` differs from the canonical | Make `og:url` match the canonical. |
| PHONE-1 | critical | A phone number other than `nap.phone` or `phone_allowlist` appears in the page | Replace with the one office number. Toll-free numbers (crisis lines) are ignored. |
| PHONE-2 | low | `format-detection` meta has `telephone=no` | Remove it; calls are the conversion. |
| NAP-1 | medium | Page has no street address (`client.json` → `address_match.street`) | Put the full address in the footer. |
| NAP-2 | high | Street address appears without the suite (`address_match.suite`) | Add the suite number everywhere. |
| TITLE-1 | high | Title missing, or identical to another page's | Unique title per page. |
| TITLE-2 | medium | Title longer than 60 or shorter than 30 characters | Aim for 50-60. |
| TITLE-3 | high | Title or H1 uses a misspelling from `client.json` → `brand_misspellings` | Spell it as `business_name`. |
| H1-1 | high | Page has no H1, more than one, or the same H1 as another page | One unique H1 per page. |
| DESC-1 | medium | Meta description missing, duplicated, or over 155 characters | Unique, under 155, end with the phone. |
| SCHEMA-1 | medium | No JSON-LD on the page | Add the right type for the page. |
| SCHEMA-2 | high | `AggregateRating` or `Review` in JSON-LD | Remove (truth rule 6). |
| SCHEMA-3 | high | Business schema with its own address on a page that is not the homepage | One organization; use `areaServed`. |
| SCHEMA-4 | low | Business schema with no `image` | Add the logo or office photo. |
| TRUTH-1 | high | Text from `client.json` → `banned_text` appears | Remove or owner decides. |
| FILE-1 | high | `robots.txt` missing, blocks everything, or blocks an AI crawler | Allow Googlebot and the AI search bots. |
| FILE-2 | medium | `robots.txt` has no `Sitemap:` line | Add it. |
| FILE-3 | high | `sitemap.xml` missing, or lists a URL that is not 200 or not on the `site_url` host | Fix the sitemap. |
| FILE-4 | high | `llms.txt` missing, or has banned text, or lacks the phone or suite | Rewrite from `client.json`. |
| PAGE-1 | high | A page returns a status other than 200 | Fix or remove the link. |

## Not checked here (needs a browser or a paid key)
Page speed and LCP, JavaScript-rendered content, keyword rankings, backlinks, AI answer mentions.
Search Console and open-seo data merge in later, only after the owner says yes to the cost.

## Score
`plan.md` sorts checks by severity (critical, high, medium, low), then by how many pages each one hits,
so the biggest problem is first.
