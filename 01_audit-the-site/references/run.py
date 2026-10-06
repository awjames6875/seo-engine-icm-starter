"""Room 01: crawl a site and write audit.md, plan.md, crawl.json.
Usage: py 01_audit-the-site/references/run.py [--url URL] [--max N]
Free only: no paid API is called here."""
import argparse
import json
import re
import sys
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOM = Path(__file__).resolve().parent.parent
SHARED = ROOM.parent / "_shared"
POINTS = {"critical": 10, "high": 5, "medium": 2, "low": 1}
SEVERITY_ORDER = ["critical", "high", "medium", "low"]
AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot",
           "PerplexityBot", "Google-Extended", "Googlebot", "Bingbot", "Applebot"]
PHONE_PATTERN = re.compile(r"\(?\b\d{3}\)?[-. )]+\d{3}[-. ]\d{4}\b")
TOLL_FREE_PREFIXES = ("800", "833", "844", "855", "866", "877", "888")
BUSINESS_TYPES ={"LocalBusiness", "MedicalBusiness", "MedicalOrganization", "Organization", "HealthAndBeautyBusiness"}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.h1s = []
        self.metas = {}
        self.canonical = ""
        self.jsonLdBlocks = []
        self._tag = None
        self._buffer = ""

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "meta":
            key = attributes.get("name") or attributes.get("property")
            if key:
                self.metas[key.lower()] = attributes.get("content") or ""
        elif tag == "link" and "canonical" in (attributes.get("rel") or "").split():
            self.canonical = attributes.get("href") or ""
        elif tag == "script" and attributes.get("type") == "application/ld+json":
            self._tag, self._buffer = "ldjson", ""
        elif tag in ("title", "h1"):
            self._tag, self._buffer = tag, ""

    def handle_data(self, data):
        if self._tag:
            self._buffer += data

    def handle_endtag(self, tag):
        if tag != self._tag and not (tag == "script" and self._tag == "ldjson"):
            return
        text = " ".join(self._buffer.split())
        if self._tag == "title" and not self.title:
            self.title = text
        elif self._tag == "h1":
            self.h1s.append(text)
        elif self._tag == "ldjson":
            self.jsonLdBlocks.append(self._buffer)
        self._tag = None


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "SeoEngineAudit/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read().decode("utf-8", errors="replace")
            return {"url": url, "status": response.status, "type": response.headers.get("Content-Type", ""), "body": body}
    except urllib.error.HTTPError as error:
        return {"url": url, "status": error.code, "type": "", "body": ""}
    except Exception as error:
        return {"url": url, "status": 0, "type": "", "body": "", "error": str(error)}


def loadClient():
    return json.loads((SHARED / "client.json").read_text(encoding="utf-8"))


def digitsOnly(text):
    return re.sub(r"\D", "", text)


def normalizeUrl(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc.lower()}{parsed.path.rstrip('/')}"


def collectSchemaTypes(node, found):
    if isinstance(node, list):
        for item in node:
            collectSchemaTypes(item, found)
    elif isinstance(node, dict):
        types = node.get("@type", [])
        found.append({"types": [types] if isinstance(types, str) else types, "node": node})
        for value in node.values():
            collectSchemaTypes(value, found)


def parseSchema(blocks):
    found = []
    for block in blocks:
        try:
            collectSchemaTypes(json.loads(block), found)
        except ValueError:
            continue
    return found


def parsePage(fetched):
    parser = PageParser()
    parser.feed(fetched["body"])
    return {
        "url": fetched["url"], "status": fetched["status"], "title": parser.title, "h1s": parser.h1s,
        "description": parser.metas.get("description", ""), "canonical": parser.canonical,
        "ogUrl": parser.metas.get("og:url", ""), "formatDetection": parser.metas.get("format-detection", ""),
        "schema": parseSchema(parser.jsonLdBlocks), "html": fetched["body"],
    }


def finding(checkId, severity, url, evidence):
    return {"id": checkId, "severity": severity, "url": url, "evidence": evidence}


def checkCanonical(page, client):
    url, canonical = page["url"], page["canonical"]
    if not canonical:
        return [finding("CANON-1", "critical", url, "no canonical tag")]
    results = []
    if normalizeUrl(canonical) != normalizeUrl(url):
        results.append(finding("CANON-1", "critical", url, f"canonical points to {canonical}"))
    if urlparse(canonical).netloc.lower() != urlparse(client["site_url"]).netloc.lower():
        results.append(finding("CANON-2", "high", url, f"canonical host is {urlparse(canonical).netloc}"))
    if page["ogUrl"] and normalizeUrl(page["ogUrl"]) != normalizeUrl(canonical):
        results.append(finding("CANON-3", "medium", url, f"og:url {page['ogUrl']} vs canonical {canonical}"))
    return results


def checkPhones(page, client):
    results = []
    allowedPhones = {digitsOnly(phone) for phone in [client["nap"]["phone"]] + client.get("phone_allowlist", [])}
    found = {digitsOnly(match) for match in PHONE_PATTERN.findall(page["html"])}
    others = sorted(number for number in found - allowedPhones if not number.startswith(TOLL_FREE_PREFIXES))
    if others:
        results.append(finding("PHONE-1", "critical", page["url"], "other numbers: " + ", ".join(others)))
    if "telephone=no" in page["formatDetection"].replace(" ", ""):
        results.append(finding("PHONE-2", "low", page["url"], "format-detection telephone=no"))
    return results


def checkAddress(page, client):
    html, url, addressMatch = page["html"], page["url"], client["address_match"]
    if not re.search(addressMatch["street"], html, re.I):
        return [finding("NAP-1", "medium", url, "no street address in the page")]
    if not re.search(addressMatch["suite"], html, re.I):
        return [finding("NAP-2", "high", url, "street address found without the suite number")]
    return []


def checkHeadings(page, client):
    url, results = page["url"], []
    if not page["title"]:
        results.append(finding("TITLE-1", "high", url, "no title"))
    elif not 30 <= len(page["title"]) <= 60:
        results.append(finding("TITLE-2", "medium", url, f"{len(page['title'])} characters: {page['title']}"))
    for label, text in [("title", page["title"])] + [("h1", h1) for h1 in page["h1s"]]:
        for misspelling in client.get("brand_misspellings", []):
            if re.search(rf"\b{re.escape(misspelling)}\b", text):
                results.append(finding("TITLE-3", "high", url, f"{label} misspells the brand as {misspelling}: {text}"))
    if len(page["h1s"]) != 1:
        results.append(finding("H1-1", "high", url, f"{len(page['h1s'])} H1 tags"))
    description = page["description"]
    if not description:
        results.append(finding("DESC-1", "medium", url, "no meta description"))
    elif len(description) > 155:
        results.append(finding("DESC-1", "medium", url, f"{len(description)} characters"))
    return results


def checkDuplicates(pages):
    results = []
    for checkId, label, valueOf in [
        ("TITLE-1", "title", lambda page: page["title"]),
        ("H1-1", "H1", lambda page: page["h1s"][0] if page["h1s"] else ""),
        ("DESC-1", "meta description", lambda page: page["description"]),
    ]:
        groups = defaultdict(list)
        for page in pages:
            if valueOf(page):
                groups[valueOf(page)].append(page["url"])
        for value, urls in groups.items():
            for url in urls if len(urls) > 1 else []:
                results.append(finding(checkId, "high" if checkId != "DESC-1" else "medium", url,
                                       f"same {label} on {len(urls)} pages: {value}"))
    return results


def checkSchema(page, isHome):
    url, results = page["url"], []
    if not page["schema"]:
        return [finding("SCHEMA-1", "medium", url, "no JSON-LD")]
    allTypes = {name for entry in page["schema"] for name in entry["types"]}
    if allTypes & {"AggregateRating", "Review"}:
        results.append(finding("SCHEMA-2", "high", url, "review or rating schema: " + ", ".join(sorted(allTypes & {"AggregateRating", "Review"}))))
    for entry in page["schema"]:
        if not set(entry["types"]) & BUSINESS_TYPES:
            continue
        if not isHome and "address" in entry["node"]:
            results.append(finding("SCHEMA-3", "high", url, f"{entry['types']} has its own address"))
        if "image" not in entry["node"] and "logo" not in entry["node"] and isHome:
            results.append(finding("SCHEMA-4", "low", url, f"{entry['types']} has no image"))
    return results


def checkBannedText(page, bannedText):
    htmlLower = page["html"].lower()
    return [finding("TRUTH-1", "high", page["url"], f"'{phrase}' found: {reason}")
            for phrase, reason in bannedText if phrase.lower() in htmlLower]


def checkPage(page, client, bannedText, isHome):
    results = checkCanonical(page, client) + checkPhones(page, client) + checkAddress(page, client)
    results += checkHeadings(page, client) +checkSchema(page, isHome) + checkBannedText(page, bannedText)
    if page["status"] != 200:
        results.append(finding("PAGE-1", "high", page["url"], f"status {page['status']}"))
    return results


def parseRobots(robots):
    results = []
    blockedAgents, agents, inRules = set(), [], False
    for line in robots["body"].splitlines():
        key, _, value = line.split("#")[0].partition(":")
        key, value = key.strip().lower(), value.strip()
        if key == "user-agent":
            agents, inRules = ([] if inRules else agents) + [value], False
        elif key in ("allow", "disallow"):
            inRules = True
            if key == "disallow" and value == "/":
                blockedAgents.update(agents)
    watched = {bot.lower() for bot in AI_BOTS} | {"*"}
    for blocked in sorted(agent for agent in blockedAgents if agent.lower() in watched):
        results.append(finding("FILE-1", "high", robots["url"], f"Disallow: / for {blocked}"))
    if "sitemap:" not in robots["body"].lower():
        results.append(finding("FILE-2", "medium", robots["url"], "no Sitemap: line"))
    return results


def checkFiles(base, client, bannedText, sitemapUrls, pageStatus):
    results = []
    robots, llms = fetch(base + "/robots.txt"), fetch(base + "/llms.txt")
    results += parseRobots(robots) if robots["status"] == 200 else [finding("FILE-1", "high", robots["url"], f"status {robots['status']}")]
    if llms["status"] != 200:
        results.append(finding("FILE-4", "high", llms["url"], f"status {llms['status']}"))
    else:
        bodyLower = llms["body"].lower()
        for phrase, reason in bannedText:
            if phrase.lower() in bodyLower:
                results.append(finding("FILE-4", "high", llms["url"], f"'{phrase}' found: {reason}"))
        if digitsOnly(client["nap"]["phone"]) not in digitsOnly(llms["body"]):
            results.append(finding("FILE-4", "high", llms["url"], "main phone number missing"))
        if not re.search(client["address_match"]["suite"], llms["body"], re.I):
            results.append(finding("FILE-4", "high", llms["url"], "suite number missing"))
    siteHost = urlparse(client["site_url"]).netloc.lower()
    for url in sitemapUrls:
        if urlparse(url).netloc.lower() != siteHost:
            results.append(finding("FILE-3", "high", url, f"sitemap URL is not on {siteHost}"))
        elif pageStatus.get(url, 200) != 200:
            results.append(finding("FILE-3", "high", url, f"sitemap URL returns {pageStatus[url]}"))
    return results


def listSitemapUrls(base):
    sitemap = fetch(base + "/sitemap.xml")
    return re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sitemap["body"]), sitemap["status"]


def groupFindings(findings):
    grouped = defaultdict(list)
    for item in findings:
        grouped[item["id"]].append(item)
    return grouped


def writeAudit(folder, findings, pageCount, base):
    lines = [f"# Audit: {base}", f"Run: {date.today()} · pages checked: {pageCount} · findings: {len(findings)}", ""]
    for checkId, items in sorted(groupFindings(findings).items()):
        lines += [f"## {checkId} ({len(items)})", ""]
        lines += [f"- [{item['severity']}] {item['url']} — {item['evidence']}" for item in items]
        lines.append("")
    (folder / "audit.md").write_text("\n".join(lines), encoding="utf-8")


def loadFixText():
    fixes = {}
    for line in (ROOM / "references" / "checks.md").read_text(encoding="utf-8").splitlines():
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) == 4 and re.match(r"^[A-Z0-9]+-\d$", cells[0]):
            fixes[cells[0]] = (cells[2], cells[3])
    return fixes


def writePlan(folder, findings, pageCount, base):
    fixes = loadFixText()
    ranked = sorted(groupFindings(findings).items(),
                    key=lambda pair: -sum(POINTS[item["severity"]] for item in pair[1]))
    lines = [f"# Plan: {base}", f"{pageCount} pages checked. Biggest problem first. Read this, then say yes or no.", ""]
    for number, (checkId, items) in enumerate(ranked, 1):
        problem, fix = fixes.get(checkId, ("", ""))
        urls = sorted({item["url"] for item in items})
        lines += [f"## {number}. {checkId} [{items[0]['severity']}] on {len(urls)} URLs",
                  f"- Problem: {problem}", f"- Fix: {fix}", f"- Example: {items[0]['url']} — {items[0]['evidence']}", ""]
    (folder / "plan.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    arguments = argparse.ArgumentParser()
    arguments.add_argument("--url")
    arguments.add_argument("--max", type=int, default=80)
    options = arguments.parse_args()
    client = loadClient()
    bannedText = client.get("banned_text", [])
    base = (options.url or client["site_url"]).rstrip("/")
    domain = urlparse(base).netloc.replace("www.", "").split(".")[0]
    folder = ROOM / "output" / f"audit-{domain}-{date.today()}"
    folder.mkdir(parents=True, exist_ok=True)

    sitemapUrls, sitemapStatus = listSitemapUrls(base)
    urlsToCrawl = [base + "/"] + [url for url in sitemapUrls if normalizeUrl(url) != normalizeUrl(base)]
    if sitemapStatus != 200:
        print(f"sitemap.xml returned {sitemapStatus}; auditing the homepage only", file=sys.stderr)
    with ThreadPoolExecutor(8) as pool:
        pages = [parsePage(fetched) for fetched in pool.map(fetch, urlsToCrawl[: options.max])]

    findings = []
    for page in pages:
        findings += checkPage(page, client, bannedText, normalizeUrl(page["url"]) == normalizeUrl(base))
    findings += checkDuplicates([page for page in pages if page["status"] == 200])
    findings += checkFiles(base, client, bannedText, sitemapUrls, {page["url"]: page["status"] for page in pages})
    if sitemapStatus != 200:
        findings.append(finding("FILE-3", "high", base + "/sitemap.xml", f"status {sitemapStatus}"))

    crawlData = [{key: value for key, value in page.items() if key not in ("html", "schema")} for page in pages]
    (folder / "crawl.json").write_text(json.dumps(crawlData, indent=2), encoding="utf-8")
    writeAudit(folder, findings, len(pages), base)
    writePlan(folder, findings, len(pages), base)
    print(f"{len(pages)} pages, {len(findings)} findings -> {folder}")


if __name__ == "__main__":
    main()
