# Publish steps

`run.py <slug>` does these in a temporary git worktree. Your checked-out branch and uncommitted work are never touched.

1. Refuse unless room 04 says `reviewed` and room 05 made the post file. Refuse if room 05 has a hard FAIL
   (everything except the internal-links check).
2. `git worktree add -b blog/<slug> <temp> main`.
3. Add the post to `src/data/blogPosts.ts` (content escaped for a template literal; date as "Month D, YYYY").
   First run only: add optional `reviewedBy` and `faq` fields to the `BlogPost` type, `reviewedBy` and a FAQPage
   JSON-LD script to `src/app/blog/[slug]/page.tsx`. Later runs skip what is already there.
4. Add the room 05 line under the `- Blog:` line in `public/llms.txt`.
5. `npm ci && npm run build` in the worktree. If it fails: no push, the branch is deleted, the log says FAIL.
6. Commit those three files, push `blog/<slug>` only, remove the worktree.

## What the owner checks on the Vercel preview
- The post opens at `/blog/<slug>` and reads like the approved article.
- Author and "reviewed by" show the right names; the FAQ section shows.
- `/llms.txt` has the new line.
- View source: two JSON-LD blocks (BlogPosting with reviewedBy, FAQPage).
- Then merge the branch yourself and write `output/<slug>/review.md` as `reviewed`.
