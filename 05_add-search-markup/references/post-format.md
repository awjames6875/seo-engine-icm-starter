# Post format

`run.py` writes `output/<slug>/<slug>.md`: frontmatter, then the approved body copied untouched.
Every value is JSON, so it parses without a YAML library.

| Field | Comes from | Room 06 maps it to (Safe Harbor `BlogPost`) |
| --- | --- | --- |
| `slug` | the run slug | `slug` |
| `title`, `metaTitle`, `metaDescription`, `excerpt`, `category`, `tags` | `approved.md` frontmatter (room 03 template) | same names |
| `date` | today, ISO (`2026-11-12`) | `date` (site shows "January 15, 2024"; room 06 reformats) |
| `readTime` | body words / 200, rounded up | `readTime` ("8 min read") |
| `author` | `client.json` `author` (name, role, url) | `author` (name only) + Person JSON-LD |
| `reviewedBy` | `client.json` `reviewer` (name, credentials, url) | no site field; room 06 adds `reviewedBy` to the Article JSON-LD |
| `publisher` | `client.json` `publisher.name` | Article JSON-LD `publisher` |
| `relatedPosts` | site `blogPosts.ts` slugs, ranked by shared tags, max 3 | `relatedPosts` |
| `faq` | the body's `## FAQ` section (`### question` + answer) | no site field; room 06 adds FAQPage JSON-LD |
| body | `approved.md`, unchanged | `content` |

Not set here (room 06 decides): `icon`, `featured`.

`llms-line.txt` is one line for the site's `public/llms.txt` Key Pages list:
`- <title>: <site_url>/blog/<slug> - <excerpt>`.

`checks.txt` lists PASS or FAIL for: body unchanged, author, reviewedBy, FAQ count, banned text, internal links.
A FAIL does not stop the run. Room 06 shows it to the owner.
