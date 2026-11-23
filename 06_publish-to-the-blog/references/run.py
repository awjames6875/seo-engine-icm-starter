"""Room 06: put the post on a blog/<slug> branch of the site repo so the host builds a preview. Never merges.
Usage: py 06_publish-to-the-blog/references/run.py <slug> [--site-repo PATH] [--base origin/main]
Works in a temporary git worktree, so the owner's checked-out branch and uncommitted work are never touched.
Writes output/<slug>/publish-log.md. The owner opens the preview, then merges."""
import argparse
import datetime
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOM = Path(__file__).resolve().parent.parent
ROOT = ROOM.parent
SHARED = ROOT / "_shared"
OUTPUT = ROOM / "output"
POSTS = ROOT / "05_add-search-markup" / "output"
EXPERT_REVIEWS = ROOT / "04_expert-reviews-it" / "output"
BLOG_DATA = "src/data/blogPosts.ts"
BLOG_PAGE = "src/app/blog/[slug]/page.tsx"
LLMS_FILE = "public/llms.txt"
BUILD_TIMEOUT_SECONDS = 1800
DEFAULT_ICON = "\U0001F4DD"

sys.path.insert(0, str(SHARED))
from status import readReviewStatus  # noqa: E402

PAGE_END = "    </article>\n  )\n}"  # the page's closing lines; a nested </article> exists above
INTERFACE_FIELDS = ("  reviewedBy?: { name: string; credentials: string; url: string }\n"
                    "  faq?: { question: string; answer: string }[]\n")
REVIEWED_BY_JSON_LD = ('            ...(post.reviewedBy && { "reviewedBy": { "@type": "Person", '
                       '"name": post.reviewedBy.name, "jobTitle": post.reviewedBy.credentials } }),\n')
FAQ_JSON_LD = """      {post.faq && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "FAQPage",
              "mainEntity": post.faq.map(item => ({
                "@type": "Question",
                "name": item.question,
                "acceptedAnswer": { "@type": "Answer", "text": item.answer }
              }))
            })
          }}
        />
      )}
"""


def loadClient():
    return json.loads((SHARED / "client.json").read_text(encoding="utf-8"))


def runGit(repo, *arguments):
    result = subprocess.run(["git", "-C", str(repo), *arguments], capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"git {' '.join(arguments)} failed:\n{result.stderr.strip()}")
    return result.stdout.strip()


def loadPost(slug):
    postFile = POSTS / slug / f"{slug}.md"
    if not postFile.exists():
        sys.exit(f"No post file at {postFile}. Room 05 comes first.")
    if readReviewStatus(EXPERT_REVIEWS / slug) != "reviewed":
        sys.exit(f"Room 04 '{slug}' is not reviewed. The expert reviewer signs off first.")
    checks = (POSTS / slug / "checks.txt").read_text(encoding="utf-8").splitlines()
    hardFails = [line for line in checks if line.startswith("FAIL") and "internal links" not in line]
    if hardFails:
        sys.exit("Room 05 checks failed, fix them first:\n" + "\n".join(hardFails))
    return parsePost(postFile.read_text(encoding="utf-8")), checks


def parsePost(text):
    match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", text, re.S)
    if not match:
        sys.exit("Post file has no frontmatter block.")
    post, faq = {}, []
    for line in match.group(1).splitlines():
        if line.startswith("  - "):
            faq.append(json.loads(line[4:]))
        elif line.strip() != "faq:":
            key, _, value = line.partition(": ")
            post[key] = json.loads(value)
    post["faq"], post["body"] = faq, match.group(2)
    return post


def toTypeScriptString(text):
    return "'" + text.replace("\\", "\\\\").replace("'", "\\'") + "'"


def toTemplateLiteral(text):
    return "`" + text.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${") + "`"


def formatDate(isoDate):
    day = datetime.date.fromisoformat(isoDate)
    return f"{day.strftime('%B')} {day.day}, {day.year}"


def buildEntry(post):
    stringList = lambda items: "[" + ", ".join(toTypeScriptString(item) for item in items) + "]"
    reviewer, faq = post["reviewedBy"], post["faq"]
    content = f"\n# {post['title']}\n\n{post['body']}"
    faqItems = ",\n".join(f"      {{ question: {toTypeScriptString(item['question'])}, "
                          f"answer: {toTypeScriptString(item['answer'])} }}" for item in faq)
    return "\n".join([
        "  {",
        f"    slug: {toTypeScriptString(post['slug'])},",
        f"    title: {toTypeScriptString(post['title'])},",
        f"    excerpt: {toTypeScriptString(post['excerpt'])},",
        f"    content: {toTemplateLiteral(content)},",
        f"    author: {toTypeScriptString(post['author']['name'])},",
        f"    date: {toTypeScriptString(formatDate(post['date']))},",
        f"    readTime: {toTypeScriptString(post['readTime'])},",
        f"    category: {toTypeScriptString(post['category'])},",
        f"    tags: {stringList(post['tags'])},",
        "    featured: false,",
        f"    icon: {toTypeScriptString(DEFAULT_ICON)},",
        f"    metaTitle: {toTypeScriptString(post['metaTitle'])},",
        f"    metaDescription: {toTypeScriptString(post['metaDescription'])},",
        f"    relatedPosts: {stringList(post['relatedPosts'])},",
        f"    reviewedBy: {{ name: {toTypeScriptString(reviewer['name'])}, "
        f"credentials: {toTypeScriptString(reviewer['credentials'])}, url: {toTypeScriptString(reviewer['url'])} }},",
        f"    faq: [\n{faqItems}\n    ]",
        "  }"])


def patchOnce(file, alreadyDone, anchor, replacement):
    source = file.read_text(encoding="utf-8")
    if alreadyDone in source:
        return
    if source.count(anchor) != 1:
        sys.exit(f"Cannot patch {file.name}: expected one '{anchor.strip()[:40]}...', found {source.count(anchor)}.")
    file.write_text(source.replace(anchor, replacement), encoding="utf-8")


def patchSite(worktree, post, llmsLine):
    dataFile = worktree / BLOG_DATA
    source = dataFile.read_text(encoding="utf-8")
    if f"slug: '{post['slug']}'" in source:
        sys.exit(f"{BLOG_DATA} already has a post with slug '{post['slug']}'.")
    patchOnce(dataFile, "faq?:", "  relatedPosts: string[]\n", "  relatedPosts: string[]\n" + INTERFACE_FIELDS)
    source = dataFile.read_text(encoding="utf-8")
    end = source.rstrip().rfind("\n]")
    dataFile.write_text(source[:end] + ",\n" + buildEntry(post) + source[end:], encoding="utf-8")
    page = worktree / BLOG_PAGE
    patchOnce(page, "post.reviewedBy", '            "publisher": {\n', REVIEWED_BY_JSON_LD + '            "publisher": {\n')
    patchOnce(page, "post.faq", PAGE_END, FAQ_JSON_LD + PAGE_END)
    llmsFile = worktree / LLMS_FILE
    lines = llmsFile.read_text(encoding="utf-8").splitlines()
    position = next((index + 1 for index, line in enumerate(lines) if line.startswith("- Blog:")), len(lines))
    lines.insert(position, llmsLine)
    llmsFile.write_text("\n".join(lines) + "\n", encoding="utf-8")


def runBuild(worktree):
    result = subprocess.run("npm ci && npm run build", cwd=worktree, shell=True, capture_output=True, text=True,
                            timeout=BUILD_TIMEOUT_SECONDS)
    return result.returncode == 0, (result.stdout + result.stderr)[-1500:]


def writeLog(slug, lines):
    logFile = OUTPUT / slug / "publish-log.md"
    logFile.parent.mkdir(parents=True, exist_ok=True)
    logFile.write_text("\n".join([f"# Publish log: {slug}", ""] + lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"-> {logFile}")


def publish(slug, siteRepo, base):
    if (OUTPUT / slug).exists():
        sys.exit(f"{OUTPUT / slug} already exists. Delete it to re-run.")
    post, checks = loadPost(slug)
    llmsLine = (POSTS / slug / "llms-line.txt").read_text(encoding="utf-8").strip()
    branch = f"blog/{slug}"
    if runGit(siteRepo, "branch", "--list", branch):
        sys.exit(f"Branch {branch} already exists in the site repo.")
    runGit(siteRepo, "fetch", "origin")  # branch from the live site, never a stale local copy (23 Nov 2026)
    worktree = Path(tempfile.mkdtemp(prefix="room06-")) / "site"
    runGit(siteRepo, "worktree", "add", "-b", branch, str(worktree), base)
    log = [f"- Branch: `{branch}` (from `{base}`)", f"- Site repo: `{siteRepo}`"]
    isPushed = False
    try:
        patchSite(worktree, post, llmsLine)
        built, buildTail = runBuild(worktree)
        log.append(f"- Build: {'PASS' if built else 'FAIL'}")
        if not built:
            log += ["- Pushed: NO (the build failed)", "", "```", buildTail, "```"]
        else:
            runGit(worktree, "add", BLOG_DATA, BLOG_PAGE, LLMS_FILE)
            runGit(worktree, "commit", "-m", f"blog: {post['title']}")
            log.append(f"- Commit: {runGit(worktree, 'rev-parse', '--short', 'HEAD')}")
            runGit(worktree, "push", "-u", "origin", branch)
            isPushed = True
            log += ["- Pushed: yes, branch only. Nothing merged.",
                    "- Preview: open the Vercel dashboard, find the preview for this branch.",
                    "- Next: the owner opens the preview, then merges, then writes review.md (`reviewed`)."]
        log += [""] + [f"Room 05 {line}" for line in checks if line.startswith("FAIL")]
    finally:
        runGit(siteRepo, "worktree", "remove", "--force", str(worktree))
        if not isPushed:
            runGit(siteRepo, "branch", "-D", branch)
    writeLog(slug, log)


def main():
    arguments = argparse.ArgumentParser()
    arguments.add_argument("slug")
    arguments.add_argument("--site-repo", default=None)
    arguments.add_argument("--base", default="origin/main")
    options = arguments.parse_args()
    siteRepo = Path(options.site_repo or loadClient()["site_repo"])
    publish(options.slug, siteRepo, options.base)


if __name__ == "__main__":
    main()
