# CONTEXT.md — 03 Write the Article

Last updated: 2026-10-07

## Stage Contract
1. **Inputs:** `02_find-what-to-write/output/<slug>/brief.md`, `02_find-what-to-write/output/<slug>/owner-facts.md`,
   `_shared/truth-rules.md`, `_shared/voice.md`, `_shared/client.json`, `references/article-template.md`.
2. **Process:** the model drafts the article from the owner's facts in their voice, answering the brief's
   questions in the template's order, then runs the truth-rules checklist on every line.
3. **Outputs:** `output/<slug>/draft.md` (frontmatter: title, metaTitle, metaDescription, excerpt,
   category, tags; then the body; then a `## FAQ` section of question/answer pairs) and
   `output/<slug>/questions-for-owner.md` (missing facts, public facts for the reviewer to verify,
  brief questions skipped and why).
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

## Answer mode (Adam, 23 Nov 2026)
When there is no owner story, the draft answers the public's questions from `client.json` facts only (see `_shared/autopilot-sunday.md` steps 4-6). No "owner's experience" section, no invented story. General facts go to `questions-for-owner.md` for Apollo to verify.
**Fact check before the draft leaves this room:** every service, age, insurance, hour and phrase like "we offer" or "we accept" must match a line in `owner-facts.md`. A service not in `client.json` `services` (for example couples therapy) is never offered, only discussed. Hours: only what Adam has said (Saturday times, 22 Nov 2026); never "evenings" or "weekends" unless it is in `owner-facts.md`. Ages: "ages 5 and up: kids, teens, and adults", never "adults, ages 5 and up". (The 23 Nov 2026 dry run broke all three; a passing banned-text check does not catch this.)

## Never do this
- Never invent a fact, a statistic, a quote, a client story or an outcome. Missing = `questions-for-owner.md`.
- Never give professional advice or promise a result. Say what the service is, not what it will do for the reader.
- Never write as the expert reviewer. The owner writes as the founder with lived experience.
