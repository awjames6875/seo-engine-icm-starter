"""Print each room's review state. Usage: py _shared/status.py [slug]"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROOM_PREFIXES = tuple(f"0{number}_" for number in range(1, 8))


def readReviewStatus(runFolder):
    reviewFile = runFolder / "review.md"
    if not reviewFile.exists():
        return "pending"
    for line in reviewFile.read_text(encoding="utf-8").splitlines():
        if line.startswith("review_status:"):
            return line.split(":", 1)[1].strip()
    return "pending"


def listRuns(room, requestedSlug):
    outputFolder = room / "output"
    if not outputFolder.exists():
        return []
    runs = [folder for folder in sorted(outputFolder.iterdir()) if folder.is_dir()]
    if requestedSlug:
        runs = [folder for folder in runs if folder.name == requestedSlug]
    return runs


def printRoom(room, requestedSlug):
    runs = listRuns(room, requestedSlug)
    if not runs:
        print(f"{room.name:<28} no runs yet")
        return
    for run in runs:
        files = ", ".join(sorted(file.name for file in run.iterdir() if file.is_file())) or "no files"
        print(f"{room.name:<28} {run.name:<36} {readReviewStatus(run):<9} {files}")


def main():
    requestedSlug = sys.argv[1] if len(sys.argv) > 1 else None
    rooms = [folder for folder in sorted(ROOT.iterdir()) if folder.is_dir() and folder.name.startswith(ROOM_PREFIXES)]
    for room in rooms:
        printRoom(room, requestedSlug)
    clientReady = (ROOT / "_shared" / "client.json").exists()
    print(f"\nclient.json: {'found' if clientReady else 'MISSING (copy client.example.json)'}")


if __name__ == "__main__":
    main()
