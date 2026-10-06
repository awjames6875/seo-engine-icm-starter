# CLAUDE.md — SEO Engine (ICM Starter)

One website goes in. An audit, a plan, and approved articles that rank on Google and get cited by AI come out.

## Identity
You are helping a business owner grow in search and AI answers. The business facts live in
`_shared/client.json` (copy `_shared/client.example.json` to start). A new client is a new config, never new code.

ALWAYS: number every step · one task at a time · copy-paste ready commands ·
warn before destructive or paid actions · tables and lists · say what good looks like.

## Where things live
| Folder | Bucket | What happens here |
| --- | --- | --- |
| `01_audit-the-site/` | 60% SCRIPT | Crawl any URL, merge SEO data, write the audit and the plan. |
| `02_find-what-to-write/` | 30% DATA | Keyword and question data, scored. The owner picks one topic. |
| `03_write-the-article/` | 10% AI | Draft in the owner's voice from their facts. The one AI room. |
| `04_expert-reviews-it/` | 60% SCRIPT | Flag risky claims. A subject expert signs off. |
| `05_add-search-markup/` | 60% SCRIPT | Post file, FAQ, author and reviewedBy, llms.txt line, links. |
| `06_publish-to-the-blog/` | 60% SCRIPT | Write the post to the site repo branch. Preview build. |
| `07_see-what-worked/` | 30% DATA | Weekly rank, clicks and AI visibility. Feeds room 02. |
| `_shared/` | — | Client config, truth rules, voice, status/doctor/sweep scripts. |

## Route by what just happened
| If | Go to | Then stop at |
| --- | --- | --- |
| new site or client | `01_audit-the-site/CONTEXT.md` | the owner reads the plan |
| plan approved, or weekly report in | `02_find-what-to-write/CONTEXT.md` | the owner picks a topic and gives their facts |
| topic picked | `03_write-the-article/CONTEXT.md` | the owner approves the draft |
| draft approved | `04_expert-reviews-it/CONTEXT.md` | the expert signs off |
| expert signed off | `05_add-search-markup/CONTEXT.md` | flows straight on |
| markup built | `06_publish-to-the-blog/CONTEXT.md` | the owner approves the preview and merges |
| it is Monday | `07_see-what-worked/CONTEXT.md` | the owner skims the report |
| asked for status | `py _shared/status.py` | report what it prints |

Run conventions, stable vs. per-run material, and review status: `CONTEXT.md`.

## Critical Rules
1. Never commit secrets. Keys live in `.env.local` (gitignored).
2. When a room's behavior changes, update its `CONTEXT.md` and bump `Last updated`.
3. Never bleed context between rooms. Load only what the room's Stage Contract names.
4. **60-30-10:** a room tagged 60% or 30% runs a script, never the model.
5. **Nothing moves on until that room's `review.md` says `reviewed`.**
6. **Never call a paid API without asking, every time** (open-seo, DataForSEO).
7. **Nothing publishes itself.** Room 06 only ever pushes a branch. The owner merges.
8. Truth rules in `_shared/truth-rules.md` outrank everything, including SEO.
9. When a run goes wrong, fix the reference file that allowed it, not the artifact.

## Anti-patterns
- No `CLAUDE.md` inside a room. Exactly `references/` and `output/` per room.
- The room list lives in this file only. Never repeat it in `CONTEXT.md`.
- Python runs as `py` on Windows (`python3` on Mac/Linux).

Last updated: 2026-10-06
