# CONTEXT.md — 04 Expert Reviews It

Last updated: 2026-10-06

## Stage Contract
1. **Inputs:** `03_write-the-article/output/<slug>/draft.md`, `_shared/truth-rules.md`,
   `_shared/client.json` (reviewer name), `references/claim-patterns.txt`.
2. **Process:** `references/run.py` flags every line that matches a risky claim (in health: clinical, medication, diagnosis),
   statistic or outcome pattern, plus banned phrases, and builds a review sheet. The expert reviewer reads
   the sheet and the draft and marks each flag OK or a fix.
3. **Outputs:** `output/<slug>/review-sheet.md` (each flagged line, why, OK/fix box),
   `output/<slug>/approved.md` (the draft with the expert reviewer's fixes applied).
4. **Human check:** the expert reviewer signs off. `review.md` says `reviewed`, `reviewer:` the expert reviewer. Then room 05.

## L3 / L4 folders
- `references/`: constraints. `run.py`, `claim-patterns.txt` (one regex per line, with a reason).
- `output/<slug>/`: material. The sheet and the approved copy.

## Bucket: 60% SCRIPT
`references/run.py` does the flagging. Pattern matching is deterministic. The judgment is the expert reviewer's, not the model's.

## Script vs. AI
- Script: match patterns, write the sheet, copy the draft to `approved.md` with the fixes.
- AI: nothing. This room is deterministic.

## Never do this
- Never mark a flag OK on the expert reviewer's behalf.
- Never let the owner's approval stand in for the expert reviewer's. Both are needed.
