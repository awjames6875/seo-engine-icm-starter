# CONTEXT.md — SEO Engine (ICM Starter)

Last updated: 2026-10-06

## Purpose and boundary
- **Trigger:** a site needs an audit (room 01), or the owner wants the next article (room 02).
- **Repeating unit:** one article = one run. An audit is its own run.
- **Done:** the post is merged into the site repo and live, and it appears in `/sitemap.xml` and `/llms.txt`.
- **Out of scope:** auto-publishing, paid ads, customer or patient data of any kind.

## Starting a run
- **Run ID = slug:** lowercase `kebab-case`, set once, never renamed.
  - Audit runs: `audit-<domain>-<YYYY-MM-DD>` (e.g. `audit-example-2026-10-06`).
  - Article runs: the article slug (e.g. `how-our-service-works`), set in room 02.
- Every room writes only to its own `output/<slug>/`, so runs cannot overwrite each other.
- Test runs start with `zz-` and are deleted when the test is done.
- Run `py _shared/doctor.py` before a run.

## Stable vs. per-run
- **Stable:** `_shared/` (`client.json`, `truth-rules.md`, `voice.md`, `status.py`, `doctor.py`, `sweep.py`)
  and each room's `references/`.
- **Per run:** everything under `*/output/<slug>/`.
- **The owner must supply:** their own facts and story for each article (room 02), the expert reviewer's
  name and credentials (`_shared/client.json`), and API keys in `.env.local`.

## Status and review
- `py _shared/status.py [slug]` prints each room's review state and which key files exist.
- **A file existing is NOT approval.** Each room's `output/<slug>/review.md` carries:

      review_status: pending | reviewed
      reviewer: <owner> | <expert name>
      date: YYYY-MM-DD
      notes: (what they said, in their words)

- **No `review.md` means pending.** It is written as `reviewed` only when the reviewer says yes.
- **Changing an approved room makes every later room `stale`.** Re-run it and get a fresh yes.
- Room 04's reviewer is the subject expert, not the owner. Room 05 has no human check.

Room list and task routing live in `CLAUDE.md`. Do not duplicate them here.
