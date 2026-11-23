# Competitor check: how room 02 uses it

Why: the free run has no competition number, so a topic's competition is a guess. This file replaces the guess with what competitors really publish.

## How to make it (free, read-only, about 15 minutes)
1. For each Tulsa-area provider in `_shared/client.json` lanes and the latest competitor list, open its real website in Chrome and find its blog or resources page.
2. Record only what is on the page: does a blog exist, how many posts, newest and oldest date, post titles. If a page will not load, write that. Never fill a gap from memory.
3. Save it as `output/competitors-<YYYY-MM-DD>.md`: a table of providers, then every post title grouped by topic (addiction, family, kids, couples, insurance, other), then a **gaps** list.
4. A gap is worded "no provider post found on the pages I checked". Never write "no competition".

## How the engine uses it
- When picking a topic (Adam's pick, or the Sunday autopilot's), a topic whose question is in the **gaps** list ranks above one a competitor already answers well.
- A topic a competitor already covers can still be chosen if Safe Harbor can answer it better: more specific, more local, or with Apollo's name on it.
- Refresh the file about once a month. An older file is stale: say so before using it.

## Never do this
- Never claim "low competition" or "high volume" without a number or a page you saw.
- Never log in, fill a form or use a paid tool to make this file.
