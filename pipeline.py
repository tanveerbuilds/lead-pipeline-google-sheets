#!/usr/bin/env python3
"""
Sample lead-pipeline script for Google Sheets — demonstration only.

Takes new leads from sample_leads.csv, removes duplicates (by email),
assigns a pipeline stage, and upserts them into a Google Sheet.

Default is --dry-run: no credentials needed, prints what would happen.
With GOOGLE_SHEETS_CREDENTIALS (service-account JSON path) and SHEET_ID
set, it writes to the real sheet via gspread.

Usage:
    python pipeline.py --dry-run
    python pipeline.py
"""
import argparse
import csv
import json
import os
from pathlib import Path

HEADERS = ["name", "email", "source", "stage", "notes"]
DEFAULT_STAGE = "New"


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def dedupe(leads):
    """Keep the first occurrence of each email (case-insensitive)."""
    seen = set()
    unique, duplicates = [], 0
    for lead in leads:
        key = (lead.get("email") or "").strip().lower()
        if key and key in seen:
            duplicates += 1
            continue
        seen.add(key)
        unique.append(lead)
    return unique, duplicates


def to_rows(leads):
    rows = []
    for lead in leads:
        rows.append([
            lead.get("name", ""),
            lead.get("email", ""),
            lead.get("source", ""),
            lead.get("stage", "") or DEFAULT_STAGE,
            lead.get("notes", ""),
        ])
    return rows


def dry_run(leads):
    unique, duplicates = dedupe(leads)
    print(f"Read {len(leads)} leads from CSV.")
    print(f"Removed {duplicates} duplicate(s). {len(unique)} unique leads.")
    print()
    print(f"{'Name':<18}{'Email':<30}{'Source':<14}{'Stage':<10}")
    print("-" * 76)
    for row in to_rows(unique):
        print(f"{row[0]:<18}{row[1]:<30}{row[2]:<14}{row[3]:<10}")
    print()
    print("Dry run — nothing was written. Drop --dry-run to write to Google Sheets.")


def write_sheet(leads):
    import gspread

    creds_path = os.environ.get("GOOGLE_SHEETS_CREDENTIALS")
    sheet_id = os.environ.get("SHEET_ID")
    if not creds_path or not sheet_id:
        print("Set GOOGLE_SHEETS_CREDENTIALS and SHEET_ID, or use --dry-run.")
        return

    unique, duplicates = dedupe(leads)
    gc = gspread.service_account(filename=creds_path)
    sheet = gc.open_by_key(sheet_id).sheet1

    existing = {r[1].strip().lower() for r in sheet.get_all_values()[1:] if len(r) > 1}
    new_rows = [r for r in to_rows(unique) if r[1].strip().lower() not in existing]

    if sheet.get_all_values() == []:
        sheet.append_row(HEADERS)
    if new_rows:
        sheet.append_rows(new_rows)
    print(f"Skipped {duplicates} duplicate(s) from CSV, "
          f"added {len(new_rows)} new lead(s) to the sheet.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="print what would happen, write nothing")
    args = parser.parse_args()

    csv_path = Path(__file__).parent / "sample_leads.csv"
    leads = load_csv(csv_path)
    if args.dry_run:
        dry_run(leads)
    else:
        write_sheet(leads)


if __name__ == "__main__":
    main()
