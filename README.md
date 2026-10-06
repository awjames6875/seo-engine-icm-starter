# SEO Engine — ICM Starter

An AI SEO engine you **own**. It audits your site, finds what to write, drafts articles from *your* facts,
has an expert check them, adds the search markup, and puts each post on a preview branch.
**Nothing goes live until a human says yes.**

Built in public on YouTube by Adam James, one room per episode.
**This version (`ep00`) is the empty hotel:** the map and every room's card. Each episode adds the room it built.

## The idea in 30 seconds: it's a hotel
| Hotel | In this repo |
| --- | --- |
| The map in the lobby | `CLAUDE.md`. The AI reads it first, so it never gets lost. |
| Each room | A numbered folder (`01_audit-the-site` … `07_see-what-worked`). One job per room. |
| The card on each door | That room's `CONTEXT.md`: what comes in, what goes out, what's never allowed. |
| The front desk | `review.md`. You can't leave a room until a person signs off. |
| A new guest | A new business. It's a new `client.json`, not new code. |

This structure is Jake Van Clief's **ICM** (Interpretable Context Methodology). See the credits below.

## The 7 rooms
| # | Room | Who does the work | Stops for |
| --- | --- | --- | --- |
| 01 | Audit the site | Script | You read the plan |
| 02 | Find what to write | Data | You pick a topic and give your real facts |
| 03 | Write the article | AI (the only AI room) | You approve the draft |
| 04 | Expert reviews it | Script flags, the expert decides | The expert signs off |
| 05 | Add search markup | Script | — |
| 06 | Publish to the blog | Script (a branch only, never main) | You approve the preview and merge |
| 07 | See what worked | Data | You skim the Monday report |

60% scripts · 30% data · 10% AI. The AI only does the part it's actually good at.

> In the original build (a behavioral health practice), room 04 is `04_therapist-reviews-it`:
> a licensed therapist checks every article.

## Quick start
1. Install [Claude Code](https://claude.com/claude-code) and Python 3.
2. Clone this repo and open the folder.
3. Copy `_shared/client.example.json` to `_shared/client.json` and fill in your business.
4. Start Claude Code in the folder and say: **"new site: https://yoursite.com"**.
5. Follow the room it routes you to. Watch the episodes as each room gets built.

## Credits
See [CREDITS.md](CREDITS.md). Short version: the SEO agent idea is **Kevin Bahrabadi's**, ICM is **Jake Van Clief's**,
the SEO data is **open-seo's**, and this healthcare-safe build is Adam's.

## License
MIT. See [LICENSE](LICENSE).
