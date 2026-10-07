"""Room 04: flag risky lines in the draft for the expert reviewer, then apply the reviewer's fixes.
Usage: py 04_expert-reviews-it/references/run.py <slug>           writes output/<slug>/review-sheet.md
       py 04_expert-reviews-it/references/run.py <slug> --apply   writes output/<slug>/approved.md
In review-sheet.md the reviewer ticks "- [x] OK", or writes the corrected line (or "delete") after "Fix:"."""
import argparse
import json
import re
import sys
from pathlib import Path

ROOM = Path(__file__).resolve().parent.parent
ROOT = ROOM.parent
SHARED = ROOT / "_shared"
OUTPUT = ROOM / "output"
DRAFTS = ROOT / "03_write-the-article" / "output"
PHONE = re.compile(r"\(?\b\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b")

sys.path.insert(0, str(SHARED))
from status import readReviewStatus  # noqa: E402


def loadClient():
    return json.loads((SHARED / "client.json").read_text(encoding="utf-8"))


def loadPatterns():
    lines = (ROOM / "references" / "claim-patterns.txt").read_text(encoding="utf-8").splitlines()
    pairs = [line.split(" | ", 1) for line in lines if line.strip() and not line.startswith("#")]
    return [(re.compile(regex.strip(), re.I), reason.strip()) for reason, regex in pairs]


def loadDraft(slug):
    runFolder = DRAFTS / slug
    if not (runFolder / "draft.md").exists():
        sys.exit(f"No draft at {runFolder / 'draft.md'}. Room 03 comes first.")
    if readReviewStatus(runFolder) != "reviewed":
        sys.exit(f"Room 03 '{slug}' is not reviewed. The owner approves the draft first.")
    return (runFolder / "draft.md").read_text(encoding="utf-8").splitlines()


def buildChecks(client):
    banned = [(re.compile(re.escape(text), re.I), f"banned: {why}") for text, why in client["banned_text"]]
    misspelled = [(re.compile(rf"\b{re.escape(word)}\b"), f"brand spelled '{word}', use '{client['business_name']}'")
                  for word in client["brand_misspellings"]]
    return loadPatterns() + banned + misspelled


def findFlags(lines, client):
    checks = buildChecks(client)
    officeDigits = re.sub(r"\D", "", client["nap"]["phone"])
    flags = []
    for number, line in enumerate(lines, 1):
        reasons = [reason for pattern, reason in checks if pattern.search(line)]
        reasons += [f"phone {phone} is not the office number" for phone in PHONE.findall(line)
                    if re.sub(r"\D", "", phone) != officeDigits]
        if reasons:
            flags.append((number, line, list(dict.fromkeys(reasons))))
    return flags


def countWords(lines):
    text = "\n".join(lines)
    body = text.split("---", 2)[2] if text.startswith("---") else text
    return len(re.findall(r"\b\w+\b", body))


def writeSheet(slug, client):
    reviewer = client["reviewer"]
    if not reviewer.get("name"):
        sys.exit("No reviewer in client.json. Add reviewer.name and reviewer.credentials.")
    lines = loadDraft(slug)
    sheetFile = OUTPUT / slug / "review-sheet.md"
    if sheetFile.exists():
        sys.exit(f"{sheetFile} already exists. Delete it to re-run (the reviewer's marks are lost).")
    flags = findFlags(lines, client)
    sheet = [f"# Review sheet: {slug}", "",
             f"- Reviewer: {reviewer['name']}, {reviewer['credentials']}",
             f"- Draft: `03_write-the-article/output/{slug}/draft.md` ({countWords(lines)} words)",
             f"- Flagged lines: {len(flags)}", "",
             "For each flag: tick `- [x] OK`, or write the corrected line after `Fix:` (or `delete`).",
             "Read the whole draft too. The script only finds patterns; the judgment is yours.", ""]
    for index, (number, line, reasons) in enumerate(flags, 1):
        sheet += [f"## {index}. Line {number}", f"> {line}", f"Why: {'; '.join(reasons)}", "- [ ] OK", "- Fix: ", ""]
    sheetFile.parent.mkdir(parents=True, exist_ok=True)
    sheetFile.write_text("\n".join(sheet), encoding="utf-8")
    print(f"{len(flags)} flagged lines -> {sheetFile}")


def readDecisions(sheetText):
    decisions = []
    for block in re.split(r"^## ", sheetText, flags=re.M)[1:]:
        heading = re.match(r"(\d+)\. Line (\d+)\n> (.*)\n", block)
        isOk = bool(re.search(r"^- \[[xX]\] OK", block, re.M))
        fixMatch = re.search(r"^- Fix:(.*)$", block, re.M)
        fix = fixMatch.group(1).strip() if fixMatch else ""
        decisions.append((heading.group(1), int(heading.group(2)), heading.group(3), isOk, fix))
    return decisions


def applyFixes(slug):
    lines = loadDraft(slug)
    sheetFile = OUTPUT / slug / "review-sheet.md"
    if not sheetFile.exists():
        sys.exit(f"No {sheetFile}. Run without --apply first.")
    decisions = readDecisions(sheetFile.read_text(encoding="utf-8"))
    undecided = [flag for flag, _, _, isOk, fix in decisions if isOk == bool(fix)]
    if undecided:
        sys.exit(f"Flags need exactly one of OK or Fix: {', '.join(undecided)}")
    for flag, number, quoted, _, fix in decisions:
        if lines[number - 1].rstrip() != quoted.rstrip():
            sys.exit(f"Flag {flag}: line {number} of the draft changed since the sheet was made. Re-run the sheet.")
    fixes = {number: fix for _, number, _, isOk, fix in decisions if not isOk}
    approved = [fixes.get(number, line) for number, line in enumerate(lines, 1)
                if fixes.get(number, "").lower() != "delete"]
    (OUTPUT / slug / "approved.md").write_text("\n".join(approved) + "\n", encoding="utf-8")
    print(f"{len(fixes)} fixes applied -> {OUTPUT / slug / 'approved.md'}")


def main():
    arguments = argparse.ArgumentParser()
    arguments.add_argument("slug")
    arguments.add_argument("--apply", action="store_true")
    options = arguments.parse_args()
    if options.apply:
        applyFixes(options.slug)
    else:
        writeSheet(options.slug, loadClient())


if __name__ == "__main__":
    main()
