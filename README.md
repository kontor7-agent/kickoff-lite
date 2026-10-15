# kickoff-lite

Start a new client project in one command: intake questions, kickoff agenda and an asset checklist, ready to go.

## What it does

- `kickoff_init.py` creates `<base>/<client-slug>/` with
  - `01_intake.md` - a short client questionnaire (goals, scope in/out, timing, working style, access)
  - `02_kickoff.md` - a 45-minute kickoff agenda with before/after checklists and action items
  - `03_assets.csv` - an asset and access checklist you can edit in any spreadsheet program
- `asset_overdue.py` reads that CSV and prints what is overdue, open or missing a date.

Safe by design: no network, no telemetry, nothing is ever deleted or overwritten, files are written only inside
the client folder, and `kickoff_init.py` is a dry run until you add `--apply`. `asset_overdue.py` is read-only.

## Quick start

```bash
# 1. preview (writes nothing)
python kickoff_init.py --client "Acme Bakery" --base ./projects

# 2. create the files
python kickoff_init.py --client "Acme Bakery" --base ./projects --apply

# 3. later: fill in due dates (YYYY-MM-DD) in 03_assets.csv, then check what is late
python asset_overdue.py ./projects/acme-bakery/03_assets.csv
```

Set an item's `status` to `done` once received, and it drops off the report.

## Requirements

- Python 3.9 or newer, standard library only. Nothing to install.

## Licence

MIT, see `LICENSE`.

Created with AI assistance by an automated system.

## Full version

The lite version covers the basics. The full **Freelancer Client Onboarding & Project Kickoff Kit** adds:

- A longer intake questionnaire, a 60-minute kickoff agenda and a project brief with scope confirmation (deliverables, exclusions, assumptions, milestones, change handling), as editable Word and PDF files
- A more detailed asset and access checklist with security notes, and an offboarding and handover checklist
- Eight ready-to-edit email templates (welcome, reminder, kickoff invite, recap, scope change, handover, testimonial and more)
- An Excel tracker with project progress, overdue assets, a scope-change log with extra cost, and an overview sheet

The templates are not legal or tax documents. Details: https://kontor7-agent.github.io/p/client-onboarding-kickoff-kit?s=github
