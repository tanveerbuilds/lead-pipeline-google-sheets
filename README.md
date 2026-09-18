# lead-pipeline-google-sheets

> **Sample / demo build** — a minimal lead pipeline for Google Sheets: reads new leads from a CSV, removes duplicates by email, assigns a pipeline stage, and upserts them into a sheet. Built for learning and demonstration, not production use.

## What this sample demonstrates

- **Dedupe** — same email twice (even with different casing) becomes one lead
- **Staging** — every lead enters the pipeline with a stage: New, Contacted, Qualified, Proposal, Won, Lost
- **Two modes** — `--dry-run` prints what would happen (no credentials needed); full mode writes to a real sheet via gspread

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

- This is a **demonstration**, not a finished product: no conflict resolution UI, no field mapping config, no error retries.
- The service-account JSON is a secret — keep it in an environment variable or secret manager, never in the repo.
- In production this would run on a schedule or be triggered by a webhook when a new lead arrives.

## Tech

Python · gspread · Google Sheets API · CSV input
