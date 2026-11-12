"""Room 05: turn the expert-approved article into a post file with search markup. No AI, no network.
Usage: py 05_add-search-markup/references/run.py <slug>
Writes output/<slug>/<slug>.md, llms-line.txt and checks.txt. The article body is copied untouched."""
import argparse
import datetime
import json
import math
import re
import sys
from pathlib import Path

ROOM = Path(__file__).resolve().parent.parent
ROOT = ROOM.parent
SHARED = ROOT / "_shared"
OUTPUT = ROOM / "output"
APPROVED = ROOT / "04_expert-reviews-it" / "output"
WORDS_PER_MINUTE = 200
MAX_RELATED_POSTS = 3
REQUIRED_FIELDS = ["title", "metaTitle", "metaDescription", "excerpt", "category", "tags"]

sys.path.insert(0, str(SHARED))
from status import readReviewStatus  # noqa: E402


def loadClient():
    return json.loads((SHARED / "client.json").read_text(encoding="utf-8"))


def loadApproved(slug):
    runFolder = APPROVED / slug
    if not (runFolder / "approved.md").exists():
        sys.exit(f"No approved.md at {runFolder}. Room 04 comes first.")
    if readReviewStatus(runFolder) != "reviewed":
        sys.exit(f"Room 04 '{slug}' is not reviewed. The expert reviewer signs off first.")
    return (runFolder / "approved.md").read_text(encoding="utf-8")


def splitFrontmatter(text):
    match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", text, re.S)
    if not match:
        sys.exit("approved.md has no frontmatter block (--- ... ---).")
    fields = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    missing = [name for name in REQUIRED_FIELDS if not fields.get(name)]
    if missing:
        sys.exit(f"approved.md frontmatter is missing: {', '.join(missing)}")
    return fields, match.group(2)


def parseTags(rawTags):
    return [tag.strip() for tag in rawTags.strip("[]").split(",") if tag.strip()]


def extractFaq(body):
    section = re.search(r"^## FAQ\s*\n(.*?)(?=^## |\Z)", body, re.S | re.M | re.I)
    if not section:
        sys.exit("No '## FAQ' section in the approved article. Room 03's template requires one.")
    pairs = []
    for block in re.split(r"^### ", section.group(1), flags=re.M)[1:]:
        question, _, answer = block.partition("\n")
        pairs.append({"question": question.strip(), "answer": " ".join(answer.split())})
    if not pairs:
        sys.exit("The '## FAQ' section has no '### question' entries.")
    return pairs


def readSiteFile(client, relativePath):
    siteFile = Path(client.get("site_repo", "")) / relativePath
    return siteFile.read_text(encoding="utf-8") if siteFile.exists() else None


def findRelatedPosts(client, tags, slug):
    source = readSiteFile(client, "src/data/blogPosts.ts")
    if source is None:
        return [], "site repo not found, no related posts"
    ownTags = {tag.lower() for tag in tags}
    scored = []
    for match in re.finditer(r"slug:\s*'([^']+)'.*?tags:\s*\[(.*?)\]", source, re.S):
        otherSlug, otherTags = match.group(1), re.findall(r"'([^']+)'", match.group(2))
        shared = len(ownTags & {tag.lower() for tag in otherTags})
        if shared and otherSlug != slug:
            scored.append((shared, otherSlug))
    related = [name for _, name in sorted(scored, key=lambda pair: (-pair[0], pair[1]))[:MAX_RELATED_POSTS]]
    return related, f"{len(related)} related post(s) by shared tags"


def countInternalLinks(body, siteUrl):
    links = re.findall(r"\]\(([^)\s]+)\)", body)
    return sum(1 for link in links if link.startswith("/") or link.startswith(siteUrl))


def buildFrontmatter(slug, fields, tags, faq, related, client):
    reviewer, author = client["reviewer"], client["author"]
    wordCount = len(re.findall(r"\b\w+\b", fields["body"]))
    values = [
        ("slug", slug), ("title", fields["title"]), ("metaTitle", fields["metaTitle"]),
        ("metaDescription", fields["metaDescription"]), ("excerpt", fields["excerpt"]),
        ("category", fields["category"]), ("tags", tags),
        ("date", datetime.date.today().isoformat()),
        ("readTime", f"{math.ceil(wordCount / WORDS_PER_MINUTE)} min read"),
        ("author", {"name": author["name"], "role": author["role"], "url": author["url"]}),
        ("reviewedBy", {"name": reviewer["name"], "credentials": reviewer["credentials"], "url": reviewer["url"]}),
        ("publisher", client["publisher"]["name"]), ("relatedPosts", related),
    ]
    lines = ["---"] + [f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in values]
    lines += ["faq:"] + [f"  - {json.dumps(pair, ensure_ascii=False)}" for pair in faq] + ["---"]
    return "\n".join(lines) + "\n"


def runChecks(postText, body, fields, faq, client):
    postBody = postText.split("\n---\n", 1)[1]
    bannedHits = [text for text, _ in client["banned_text"] if text.lower() in body.lower()]
    results = [
        ("body identical to approved.md", postBody == body),
        ("author present", bool(client["author"].get("name"))),
        ("reviewedBy present", bool(client["reviewer"].get("name"))),
        (f"FAQ pairs: {len(faq)}", len(faq) > 0),
        ("no banned_text in body" + (f" (found: {', '.join(bannedHits)})" if bannedHits else ""), not bannedHits),
        ("internal links in body: " + str(countInternalLinks(body, client["site_url"])),
         countInternalLinks(body, client["site_url"]) > 0),
    ]
    return results


def buildLlmsLine(slug, fields, client):
    return f"- {fields['title']}: {client['site_url']}/blog/{slug} - {fields['excerpt']}"


def writeRun(slug):
    client = loadClient()
    fields, body = splitFrontmatter(loadApproved(slug))
    runFolder = OUTPUT / slug
    if runFolder.exists():
        sys.exit(f"{runFolder} already exists. Delete it to re-run.")
    tags, faq = parseTags(fields["tags"]), extractFaq(body)
    related, relatedNote = findRelatedPosts(client, tags, slug)
    postText = buildFrontmatter(slug, {**fields, "body": body}, tags, faq, related, client) + body
    runFolder.mkdir(parents=True)
    (runFolder / f"{slug}.md").write_text(postText, encoding="utf-8")
    (runFolder / "llms-line.txt").write_text(buildLlmsLine(slug, fields, client) + "\n", encoding="utf-8")
    results = runChecks((runFolder / f"{slug}.md").read_text(encoding="utf-8"), body, fields, faq, client)
    report = [f"{'PASS' if passed else 'FAIL'}  {label}" for label, passed in results] + [f"NOTE  {relatedNote}"]
    (runFolder / "checks.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    print(f"-> {runFolder}")


def main():
    arguments = argparse.ArgumentParser()
    arguments.add_argument("slug")
    writeRun(arguments.parse_args().slug)


if __name__ == "__main__":
    main()
