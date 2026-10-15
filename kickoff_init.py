#!/usr/bin/env python3
"""kickoff-lite: scaffold a client project folder with a short intake questionnaire,
a kickoff agenda and an asset checklist (CSV).

Safe by design: no network, never deletes, never overwrites existing files, and writes
only inside <base>/<client-slug>/. Dry-run by default; add --apply to write files.

Usage:
  python kickoff_init.py --client "Acme Bakery" --base ./projects            # preview
  python kickoff_init.py --client "Acme Bakery" --base ./projects --apply    # write
"""
import argparse
import re
import sys
from pathlib import Path

INTAKE = """# Client intake - {client}

Short and rough answers are fine. "Not sure yet" is a good answer.

## 1. Basics
- Main contact (name, role, email):
- Who has the final say on decisions?
- Who else gives feedback? Who collects it into ONE list?
- Billing contact:

## 2. The project
- In one sentence: what are we making or fixing?
- Why now?
- What does a great result look like in three months?

## 3. Scope
- Must-haves:
- Nice-to-haves:
- Explicitly NOT part of this project:

## 4. Timing
- Ideal start:
- Hard deadline (and what it is tied to):
- Typical feedback turnaround (e.g. 2 working days):
- Expected feedback rounds:

## 5. Working together
- Preferred channel for quick questions:
- Preferred channel for files and approvals:
- Meeting rhythm:
- Time zone and best hours:

## 6. Access and content
- Who provides texts, images, data - and when?
- Which accounts or systems will I need access to?
- Anything held by a third party (agency, previous freelancer, IT)?
"""

KICKOFF = """# Kickoff - {client}

Goal: leave the call with one shared picture of what, by when, who does what, and how we talk.
Plan 45 minutes. Send this agenda 2 days ahead.

| Min | Topic | What we settle |
|---|---|---|
| 0-5 | Welcome, goal of the call | Everyone knows what we leave with |
| 5-15 | Recap of intake | Goal, audience, success measure confirmed |
| 15-27 | Scope in / out | Deliverables and exclusions read aloud and agreed |
| 27-35 | Timeline | Milestones, who delivers what by when |
| 35-42 | Communication | Channel, response times, feedback owner, revision rounds |
| 42-45 | Action items | Owner + due date for each |

## Before the call
- [ ] Intake answers read and summarised
- [ ] Agenda sent
- [ ] Draft scope ready to read aloud

## After the call (same day)
- [ ] Recap email with decisions and action items sent
- [ ] Scope confirmed by the client in writing (a reply "Confirmed" is enough for you both)
- [ ] Asset checklist shared

## Action items
| Action | Owner | Due |
|---|---|---|
|  |  |  |
"""

ASSETS = """item,category,owner,due_date,status,notes
Logo files (vector if possible),Brand,Client,,open,
Brand colours and fonts,Brand,Client,,open,
Texts / copy,Content,Client,,open,
Images / photos (with usage rights),Content,Client,,open,
Existing site or system access,Access,Client,,open,Use individual accounts; never send passwords by email
Analytics access,Access,Client,,open,
Domain / hosting contact,Access,Client,,open,
Approver named,Process,Client,,open,
Signed-off scope,Process,Both,,open,
"""

FILES = [
    ("01_intake.md", INTAKE),
    ("02_kickoff.md", KICKOFF),
    ("03_assets.csv", ASSETS),
]


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "client"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--client", required=True, help="client or project name")
    ap.add_argument("--base", required=True, help="folder in which the client folder is created")
    ap.add_argument("--apply", action="store_true", help="actually write files (default: preview only)")
    args = ap.parse_args()

    base = Path(args.base).resolve()
    target = base / slugify(args.client)
    if target.resolve().parent != base:
        print("Refusing: target is outside the base folder.", file=sys.stderr)
        return 1

    mode = "WRITE" if args.apply else "DRY-RUN (use --apply to write)"
    print(f"[{mode}] target folder: {target}")
    if args.apply:
        target.mkdir(parents=True, exist_ok=True)
    for fname, template in FILES:
        path = target / fname
        if path.exists():
            print(f"  skip (exists): {fname}")
            continue
        print(f"  {'create' if args.apply else 'would create'}: {fname}")
        if args.apply:
            path.write_text(template.replace("{client}", args.client.strip()), encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
