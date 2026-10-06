# CONTEXT.md — 03 Write the Article

Last updated: 2026-10-06

## Stage Contract
1. **Inputs:** `02_find-what-to-write/output/<slug>/brief.md`, `02_find-what-to-write/output/<slug>/owner-facts.md`,
   `_shared/truth-rules.md`, `_shared/voice.md`, `_shared/client.json`, `references/article-template.md`.
2. **Process:** the model drafts the article from the owner's facts in their voice, answering the brief's
   questions in the template's order, then runs the truth-rules checklist on every line.
3. **Outputs:** `output/<slug>/draft.md` (frontmatter: title, metaTitle, metaDescription, excerpt,
   category, tags; then the body; then a `## FAQ` section of question/answer pairs) and
   `output/<slug>/questions-for-owner.md` (every fact that was missing).
4. **Human check:** The owner reads `draft.md`. Yes = `review.md` says `reviewed`. Then room 04.

## L3 / L4 folders
- `references/`: constraints. `article-template.md` (E-E-A-T order: the owner's experience, what the service is
  and why it helps, what the business offers, FAQ, any safety line your field needs, contact).
- `output/<slug>/`: material. The draft and its open questions.

## Bucket: 10% AI
The model writes. Turning the owner's raw story into a clear, warm article that answers what searchers
ask is judgment a script cannot make. Model: whichever Claude model runs your Claude Code session.

## Script vs. AI
- Script: nothing yet. (Word count and banned-phrase checks run in room 04.)
- AI: the draft and the checklist pass.

## Never do this
- Never invent a fact, a statistic, a quote, a client story or an outcome. Missing = `questions-for-owner.md`.
- Never give professional advice or promise a result. Say what the service is, not what it will do for the reader.
- Never write as the expert reviewer. The owner writes as the founder with lived experience.
