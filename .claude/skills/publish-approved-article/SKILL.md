---
name: publish-approved-article
description: Use when Adam says he accepts, approves or wants to publish an article that the therapist has already signed off (room 04 reviewed). Runs room 05, room 06, opens the pull request, merges it when checks are green, and checks the live page.
---

# Publish an approved article

Adam saying "accept", "approve" or "publish" for a slug IS the owner approval. Do all steps without asking again.

## Hard stops (never skip)
- Room 04 `review.md` must say `reviewed`. If not, stop and tell Adam the therapist has not signed off. Never tick flags or write that review.md yourself.
- Never edit the article body. Never call a paid API.
- If any step fails, stop and report. Do not retry blindly or force anything.

## Steps
1. Find the slug: the one Adam names, else the newest in `04_expert-reviews-it/output/`.
2. Check room 04 `output/<slug>/review.md` says `review_status: reviewed`.
3. Room 05: `py 05_add-search-markup/references/run.py <slug>`. Every line in `checks.txt` must be PASS.
4. Room 06: `py 06_publish-to-the-blog/references/run.py <slug>`. Build must PASS, branch pushed.
5. In the `site_repo` from `_shared/client.json`: `gh pr create --base main --head blog/<slug>` (title "Blog: <slug>").
6. Wait for `gh pr checks`. All must pass. If any fail, stop and report.
7. `gh pr merge <number> --merge`.
8. Wait about 90 seconds, then `curl` the live `/blog/<slug>` page. Expect HTTP 200 and `reviewedBy` and `FAQPage` in the HTML.
9. Write `06_publish-to-the-blog/output/<slug>/review.md` (`review_status: reviewed`, reviewer Adam James, today's date, PR number).
10. Add a short entry to `tasks/build-log.md`.
11. Tell Adam: live URL, what passed, and that room 07 gives the first report in about a week.
