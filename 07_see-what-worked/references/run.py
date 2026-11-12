"""Room 07: weekly report from Search Console CSV exports. No AI, no network, no paid API.
Usage: py 07_see-what-worked/references/run.py [YYYY-MM-DD]     (default: today)
Put these four Search Console exports (Performance > Export > Download CSV) in output/<date>/ first:
  pages-7d.csv  pages-28d.csv  queries-7d.csv  queries-28d.csv
Writes output/<date>/weekly.md and data.json. Never changes a live post; ideas go to room 02."""
import argparse
import csv
import datetime
import json
import re
import sys
from pathlib import Path

ROOM = Path(__file__).resolve().parent.parent
ROOT = ROOM.parent
SHARED = ROOT / "_shared"
OUTPUT = ROOM / "output"
PUBLISHED = ROOT / "06_publish-to-the-blog" / "output"
EXPORT_FILES = ["pages-7d.csv", "pages-28d.csv", "queries-7d.csv", "queries-28d.csv"]
WINDOW_WEEKS = 4
WINNER_RATIO = 1.2
LOSER_RATIO = 0.8
MIN_IDEA_IMPRESSIONS = 10
MIN_WORD_LENGTH = 4
MAX_IDEAS = 20

sys.path.insert(0, str(SHARED))
from status import readReviewStatus  # noqa: E402


def loadClient():
    return json.loads((SHARED / "client.json").read_text(encoding="utf-8"))


def toNumber(text):
    cleaned = re.sub(r"[^\d.\-]", "", text or "")
    return float(cleaned) if cleaned else 0.0


def readExport(file, keyColumns):
    with open(file, encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return {}
    keyName = next((name for name in rows[0] if name.strip() in keyColumns), None)
    if keyName is None:
        sys.exit(f"{file.name}: no column named one of {keyColumns}. Got: {list(rows[0])}")
    return {row[keyName].strip(): {"clicks": toNumber(row.get("Clicks")),
                                   "impressions": toNumber(row.get("Impressions")),
                                   "position": toNumber(row.get("Position"))} for row in rows}


def loadExports(runFolder):
    missing = [name for name in EXPORT_FILES if not (runFolder / name).exists()]
    if missing:
        sys.exit(f"Missing in {runFolder}: {', '.join(missing)}\n"
                 "Search Console > Performance > set the date range > Export > Download CSV, then save under those names.")
    pageKeys, queryKeys = ("Top pages", "Page", "Pages"), ("Top queries", "Query", "Queries")
    return {"pages7": readExport(runFolder / "pages-7d.csv", pageKeys),
            "pages28": readExport(runFolder / "pages-28d.csv", pageKeys),
            "queries7": readExport(runFolder / "queries-7d.csv", queryKeys),
            "queries28": readExport(runFolder / "queries-28d.csv", queryKeys)}


def listPublishedSlugs():
    if not PUBLISHED.exists():
        return []
    return sorted(folder.name for folder in PUBLISHED.iterdir()
                  if folder.is_dir() and readReviewStatus(folder) == "reviewed")


def findPage(pages, slug):
    wanted = f"/blog/{slug}".rstrip("/")
    return next((stats for url, stats in pages.items() if url.rstrip("/").endswith(wanted)), None)


def judgePost(slug, exports):
    week = findPage(exports["pages7"], slug)
    month = findPage(exports["pages28"], slug)
    if week is None and month is None:
        return {"slug": slug, "verdict": "no data yet"}
    weekClicks = week["clicks"] if week else 0.0
    averageWeekly = (month["clicks"] if month else 0.0) / WINDOW_WEEKS
    verdict = "flat"
    if weekClicks > averageWeekly * WINNER_RATIO:
        verdict = "winner"
    elif weekClicks < averageWeekly * LOSER_RATIO:
        verdict = "loser"
    return {"slug": slug, "verdict": verdict, "clicks7d": weekClicks, "averageWeeklyClicks28d": round(averageWeekly, 1),
            "impressions7d": week["impressions"] if week else 0.0, "position7d": round(week["position"], 1) if week else None}


def loadExistingPostText(client):
    siteFile = Path(client.get("site_repo", "")) / "src" / "data" / "blogPosts.ts"
    if not siteFile.exists():
        return ""
    source = siteFile.read_text(encoding="utf-8")
    return " ".join(re.findall(r"(?:slug|title):\s*'([^']+)'", source) + re.findall(r"'([^']+)'", " ".join(re.findall(r"tags:\s*\[(.*?)\]", source, re.S)))).lower()


def significantWords(query):
    return [word for word in re.findall(r"[a-z0-9]+", query.lower()) if len(word) >= MIN_WORD_LENGTH]


def findQueryIdeas(queries28, existingText):
    ideas = []
    for query, stats in queries28.items():
        words = significantWords(query)
        isCovered = bool(words) and all(word in existingText for word in words)
        if stats["impressions"] >= MIN_IDEA_IMPRESSIONS and not isCovered:
            ideas.append({"query": query, **stats})
    return sorted(ideas, key=lambda idea: -idea["impressions"])[:MAX_IDEAS]


def formatReport(date, posts, ideas):
    lines = [f"# Weekly report {date}", "", "## Published posts", ""]
    if not posts:
        lines.append("No published posts yet (room 06 `review.md` must say `reviewed`).")
    else:
        lines += ["| Post | Verdict | Clicks 7d | Avg weekly clicks (28d) | Impressions 7d | Position 7d |",
                  "| --- | --- | --- | --- | --- | --- |"]
        for post in sorted(posts, key=lambda item: item.get("clicks7d", -1), reverse=True):
            lines.append(f"| {post['slug']} | {post['verdict']} | {post.get('clicks7d', '-')} | "
                         f"{post.get('averageWeeklyClicks28d', '-')} | {post.get('impressions7d', '-')} | {post.get('position7d', '-')} |")
    lines += ["", "## New query ideas (the site shows up, no post covers them)", "",
              "These feed room 02 as new runs. Nothing here changes a live post.", ""]
    lines += [f"- {idea['query']} ({int(idea['impressions'])} impressions, position {idea['position']:.1f})" for idea in ideas] or ["- none this week"]
    return "\n".join(lines) + "\n"


def main():
    arguments = argparse.ArgumentParser()
    arguments.add_argument("date", nargs="?", default=datetime.date.today().isoformat())
    date = arguments.parse_args().date
    runFolder = OUTPUT / date
    client = loadClient()
    exports = loadExports(runFolder)
    posts = [judgePost(slug, exports) for slug in listPublishedSlugs()]
    ideas = findQueryIdeas(exports["queries28"], loadExistingPostText(client))
    (runFolder / "weekly.md").write_text(formatReport(date, posts, ideas), encoding="utf-8")
    (runFolder / "data.json").write_text(json.dumps({"date": date, "posts": posts, "queryIdeas": ideas}, indent=2), encoding="utf-8")
    print(f"{len(posts)} published post(s), {len(ideas)} query idea(s) -> {runFolder / 'weekly.md'}")


if __name__ == "__main__":
    main()
