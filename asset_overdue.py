#!/usr/bin/env python3
"""Read-only report of open and overdue items in a 03_assets.csv checklist.

Never modifies any file, no network. Dates use YYYY-MM-DD.

Usage:
  python asset_overdue.py projects/acme-bakery/03_assets.csv
  python asset_overdue.py projects/acme-bakery/03_assets.csv --today 2026-11-01
"""
import argparse
import csv
import datetime as dt
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv_file")
    ap.add_argument("--today", help="override today's date (YYYY-MM-DD)")
    args = ap.parse_args()

    try:
        today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    except ValueError:
        print("Invalid --today date, use YYYY-MM-DD.", file=sys.stderr)
        return 1
    path = Path(args.csv_file)
    if not path.is_file():
        print(f"File not found: {path}", file=sys.stderr)
        return 1

    done = {"done", "received", "closed"}
    overdue, open_items, no_date, finished = [], [], [], 0
    with path.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if (row.get("status") or "").strip().lower() in done:
                finished += 1
                continue
            due_raw = (row.get("due_date") or "").strip()
            if not due_raw:
                no_date.append(row)
                continue
            try:
                due = dt.date.fromisoformat(due_raw)
            except ValueError:
                print(f"Warning: bad date '{due_raw}' for '{row.get('item')}'", file=sys.stderr)
                no_date.append(row)
                continue
            (overdue if due < today else open_items).append((due, row))

    print(f"Asset report as of {today}: {finished} done, {len(overdue)} overdue, "
          f"{len(open_items)} open, {len(no_date)} without date\n")
    for due, row in sorted(overdue, key=lambda x: x[0]):
        print(f"  OVERDUE {(today - due).days:>3} d  {row['item']}  (owner: {row.get('owner', '?')})")
    for due, row in sorted(open_items, key=lambda x: x[0]):
        print(f"  due {due}  {row['item']}  (owner: {row.get('owner', '?')})")
    for row in no_date:
        print(f"  no date     {row['item']}  (owner: {row.get('owner', '?')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
