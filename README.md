# LeadGen Tender Intelligence (India-focused)

This project is a starter implementation for healthcare-focused tender lead generation across India procurement sources.

## What it does

- Collects tenders from configured sources (API, CSV export, or HTML scraper adapters).
- Normalizes data into a common schema.
- Scores tenders against your business profile (keywords, states, tender value, closing window).
- Exports ranked leads to CSV for outreach.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py run --days-ahead 30 --min-score 0.4
```

Output:
- `data/out/leads.csv`
- `data/out/leads.json`

## Configure your targeting

Edit `config/business_profile.json`:
- `include_keywords`: medicines/products/services you supply.
- `exclude_keywords`: out-of-scope categories.
- `preferred_states`: geographic focus.
- `min_tender_value_inr` and `max_tender_value_inr`.

## Source adapters

Implemented adapters:
- `mock_cppt` (sample dataset for local testing)
- `csv_drop` (ingest CSV exports from portals)

Planned adapters:
- `gem_cppp_scraper` (browser automation when API unavailable)
- `state_portal_scrapers`

## Legal & compliance

Before scraping any website:
- Review Terms of Use / robots policy.
- Respect rate limits and anti-bot constraints.
- Store source URLs and timestamps for audit.

