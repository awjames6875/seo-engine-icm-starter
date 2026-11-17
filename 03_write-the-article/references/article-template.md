# Article Template

Write `output/<slug>/draft.md` in this order. Facts come only from `owner-facts.md` and `client.json`.

## Frontmatter
```
---
title: <plain question or promise a searcher would click; uses the keyword>
metaTitle: <50-60 characters, keyword first, ends with "| <business_name>">
metaDescription: <under 155 characters, answers the keyword, ends with nap.phone>
excerpt: <one or two sentences for the blog list>
category: <one word, matches the lane>
tags: [<3-5 short tags>]
---
```

## Body
1. **Opening: the owner's experience.** Two or three short paragraphs from `owner-facts.md`
   ("why it matters" and the true story). First person. This is the E-E-A-T proof; keep the owner's words.
2. **The plain answer.** One `##` section per brief question. The first one or two sentences answer it
   directly, so Google and AI tools can quote them. Then explain.
3. **What we offer.** Only `owner-facts.md` and `client.json` → `services`, `ages_served`, `insurance_live`.
4. **`## FAQ`.** Any brief question not covered above, plus at most three more the facts can answer.
   Each answer is two to four sentences. Format: `### <question>` then the answer.
5. **Safety line.** "If you or someone you love is in crisis, call or text 988 any time."
6. **Contact.** `nap.name`, `nap.address` (with suite) and `nap.phone`, exactly as in `client.json`.

## Rules for the brief's questions
- Skip a question about another state or a service the client does not offer. List it as skipped.
- Public facts (how a program like Medicaid works) are allowed without numbers or statistics. List each one
  under "Facts to verify" in `questions-for-owner.md` so the reviewer checks it in room 04.

## Length
No word target. Answer every kept question once. Never pad.

## Checklist (run on every line before saving)
- [ ] Every claim traces to `owner-facts.md`, `client.json`, or "Facts to verify".
- [ ] No text from `client.json` → `banned_text`. No insurance outside `insurance_live`.
- [ ] Business name spelled exactly as `business_name`.
- [ ] No advice, diagnosis or promised result. Say what the service is, not what it will do.
- [ ] Follows `_shared/voice.md`.

## `questions-for-owner.md`
Three lists: **Missing facts** (what the draft needed but the owner did not give), **Facts to verify**
(public facts for the reviewer), **Skipped questions** (and why).
