"""Room 02: find topics, score them, write topics-<date>.csv. Then write the brief for the one the owner picks.
Usage: py 02_find-what-to-write/references/run.py              free: seeds + Google autocomplete
       py 02_find-what-to-write/references/run.py --paid       adds DataForSEO data (ask the owner first)
       py 02_find-what-to-write/references/run.py --pick "keyword from the csv"
Paid keys live in .env.local: DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD.
If output/vidiq-<today>.json exists ({"keyword": monthly YouTube searches}), it fills youtube_volume."""
import argparse
import base64
import csv
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOM = Path(__file__).resolve().parent.parent
ROOT = ROOM.parent
SHARED = ROOT / "_shared"
OUTPUT = ROOM / "output"
DATAFORSEO = "https://api.dataforseo.com/v3"
AUTOCOMPLETE = "https://suggestqueries.google.com/complete/search?client=firefox&hl=en&gl=us&q="
SMALL_WORDS = {"in", "for", "of", "the", "a", "to", "and", "my", "near", "me"}
COLUMNS = ["keyword", "seed", "lane", "lane_fit", "volume", "competition_index", "score", "youtube_volume",
           "questions", "top_pages"]


def loadClient():
    return json.loads((SHARED / "client.json").read_text(encoding="utf-8"))


def loadEnv():
    envFile = ROOT / ".env.local"
    if not envFile.exists():
        return {}
    pairs = [line.split("=", 1) for line in envFile.read_text(encoding="utf-8").splitlines() if "=" in line]
    return {key.strip(): value.strip().strip('"') for key, value in pairs}


def fetchJson(url, body=None, auth=None):
    headers = {"User-Agent": "SeoEngineTopics/1.0", "Content-Type": "application/json"}
    if auth:
        headers["Authorization"] = "Basic " + base64.b64encode(auth.encode()).decode()
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def words(text):
    return set(re.findall(r"[a-z0-9]+", text.lower())) - SMALL_WORDS


def laneFit(keyword, lanes):
    keywordWords = words(keyword)
    best = ("", 0.1)
    for lane in lanes:
        laneWords = words(lane)
        if laneWords and laneWords <= keywordWords:
            return (lane, 1.0)
        if laneWords & keywordWords and best[1] < 0.5:
            best = (lane, 0.5)
    return best


def collectTopics(seeds):
    topics = {}
    for seed in seeds:
        topics.setdefault(seed.lower(), seed)
        try:
            suggestions = fetchJson(AUTOCOMPLETE + quote(seed))[1]
        except Exception as error:
            print(f"autocomplete failed for '{seed}': {error}")
            suggestions = []
        for suggestion in suggestions:
            topics.setdefault(suggestion.lower(), seed)
    return topics


def checkTasks(response):
    for task in response.get("tasks", []):
        if task.get("status_code") != 20000:
            sys.exit(f"DataForSEO error {task.get('status_code')}: {task.get('status_message')}")


def fetchVolumes(keywords, location, auth):
    body = [{"keywords": keywords[:1000], "location_name": location, "language_code": "en"}]
    response = fetchJson(f"{DATAFORSEO}/keywords_data/google_ads/search_volume/live", body, auth)
    checkTasks(response)
    rows = response["tasks"][0].get("result") or []
    return {row["keyword"].lower(): row for row in rows}, response.get("cost", 0)


def fetchSerp(seed, location, auth):
    body = [{"keyword": seed, "location_name": location, "language_code": "en", "depth": 10}]
    response = fetchJson(f"{DATAFORSEO}/serp/google/organic/live/advanced", body, auth)
    checkTasks(response)
    items = (response["tasks"][0].get("result") or [{}])[0].get("items") or []
    questions = [element["title"] for item in items if item["type"] == "people_also_ask"
                 for element in item.get("items") or [] if element.get("title")]
    topPages = [item["url"] for item in items if item["type"] == "organic"][:3]
    return {"questions": questions, "top_pages": topPages}, response.get("cost", 0)


def fetchPaidData(topics, seeds, location):
    env = loadEnv()
    if not env.get("DATAFORSEO_LOGIN") or not env.get("DATAFORSEO_PASSWORD"):
        sys.exit("No DataForSEO keys. Add DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD to .env.local.")
    auth = f"{env['DATAFORSEO_LOGIN']}:{env['DATAFORSEO_PASSWORD']}"
    volumes, totalCost = fetchVolumes(list(topics), location, auth)
    serps = {}
    for seed in seeds:
        serps[seed], cost = fetchSerp(seed, location, auth)
        totalCost += cost
    print(f"DataForSEO cost this run: ${totalCost:.4f}")
    return volumes, serps


def loadYoutubeVolumes():
    vidiqFile = OUTPUT / f"vidiq-{date.today()}.json"
    if not vidiqFile.exists():
        return {}
    return {keyword.lower(): volume for keyword, volume in json.loads(vidiqFile.read_text(encoding="utf-8")).items()}


def scoreTopics(topics, client, volumes, serps):
    youtubeVolumes = loadYoutubeVolumes()
    rows = []
    for keyword, seed in topics.items():
        lane, fit = laneFit(keyword, client["lanes"])
        data = volumes.get(keyword, {})
        volume = data.get("search_volume") or 0
        competition = data.get("competition_index")
        serp = serps.get(seed, {})
        score = volume * (1 - (50 if competition is None else competition) / 100) * fit if volumes else fit
        rows.append({"keyword": keyword, "seed": seed, "lane": lane, "lane_fit": fit,
                     "volume": volume if volumes else "", "competition_index": "" if competition is None else competition,
                     "score": round(score, 2), "youtube_volume": youtubeVolumes.get(keyword, ""), "questions": " | ".join(serp.get("questions", [])),
                     "top_pages": " | ".join(serp.get("top_pages", []))})
    return sorted(rows, key=lambda row: -row["score"])


def writeTopics(rows):
    path = OUTPUT / f"topics-{date.today()}.csv"
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} topics -> {path}")


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def findPicked(keyword):
    lists = sorted(OUTPUT.glob("topics-*.csv"))
    if not lists:
        sys.exit("No topics list yet. Run without --pick first.")
    with lists[-1].open(encoding="utf-8") as file:
        for row in csv.DictReader(file):
            if row["keyword"] == keyword.lower():
                return row
    sys.exit(f"'{keyword}' is not in {lists[-1].name}.")


def bulletList(text, empty):
    items = [item for item in text.split(" | ") if item]
    return [f"- {item}" for item in items] or [f"- {empty}"]


def writeBrief(row):
    folder = OUTPUT / slugify(row["keyword"])
    if folder.exists():
        sys.exit(f"{folder.name} already exists. A slug is set once and never overwritten.")
    folder.mkdir(parents=True)
    brief = [f"# Brief: {row['keyword']}", "",
             f"- Slug: `{folder.name}`", f"- Keyword: {row['keyword']}", f"- Lane: {row['lane'] or 'none'}",
             f"- Monthly volume: {row['volume'] or 'unknown (free run)'}",
             f"- Competition index: {row['competition_index'] or 'unknown'}", f"- Score: {row['score']}",
             f"- YouTube monthly volume: {row['youtube_volume'] or 'unknown (no VidIQ data)'}", "",
             "## Questions to answer", *bulletList(row["questions"], "none yet (needs a --paid run)"), "",
             "## Competing pages", *bulletList(row["top_pages"], "none yet (needs a --paid run)"), ""]
    (folder / "brief.md").write_text("\n".join(brief), encoding="utf-8")
    facts = [f"# Owner facts: {row['keyword']}", "",
             "Your words only. Leave a question blank rather than guess. Room 03 writes only from what is here.", "",
             "## Why does this topic matter to you?", "", "## A true story or moment from your own life or work", "",
             "## What does your business actually do for this? (services, who you serve, insurance)", "",
             "## Anything that must NOT be said?", ""]
    (folder / "owner-facts.md").write_text("\n".join(facts), encoding="utf-8")
    print(f"brief.md and owner-facts.md -> {folder}")


def main():
    arguments = argparse.ArgumentParser()
    arguments.add_argument("--paid", action="store_true")
    arguments.add_argument("--pick")
    options = arguments.parse_args()
    if options.pick:
        writeBrief(findPicked(options.pick))
        return
    client = loadClient()
    seeds = client["seed_keywords"]
    topics = collectTopics(seeds)
    volumes, serps = fetchPaidData(topics, seeds, client["location_name"]) if options.paid else ({}, {})
    writeTopics(scoreTopics(topics, client, volumes, serps))


if __name__ == "__main__":
    main()
