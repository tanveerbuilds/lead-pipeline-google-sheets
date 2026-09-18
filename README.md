# lead-pipeline-google-sheets

> **Sample / demo build.** This is a small learning project for a lead pipeline in Google Sheets: it reads new leads from a CSV, removes duplicates by email, assigns each lead a pipeline stage, and upserts them into a sheet. Not production code.

## What it shows

* Dedupe: the same email twice (even with different casing) becomes one lead.
* Staging: every lead enters the pipeline with a stage: New, Contacted, Qualified, Proposal, Won, Lost.
* Two modes: dry run prints what would happen (no credentials needed), full mode writes to a real sheet via gspread.

## Project structure

```
.
├── pipeline.py        # Sample pipeline (dry-run by default)
├── sample_leads.csv   # Example leads, including one deliberate duplicate
└── README.md
```

## How to run the sample

```bash
pip install -r requirements.txt

# See what would happen, no credentials needed
python pipeline.py --dry-run

# Write to a real Google Sheet (service account JSON + sheet ID required)
export GOOGLE_SHEETS_CREDENTIALS=/path/to/service-account.json
export SHEET_ID=your_sheet_id
python pipeline.py
```

## Notes

* This is a **demonstration**, not a finished product. There is no conflict resolution UI, no field mapping config, and no error retries.
* The service account JSON is a secret. Keep it in an environment variable or secret manager, never in the repo.
* In production this would run on a schedule or get triggered by a webhook when a new lead arrives.

## Tech

Python · gspread · Google Sheets API · CSV input
