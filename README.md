# Airbnb Market Intelligence Pipeline

## Project Overview

This project builds a reproducible data engineering and analytics pipeline using public Inside Airbnb data for Edinburgh.

The solution ingests, profiles, validates, cleans, transforms, and models Airbnb market data before producing analytical insights, statistical findings, and an interactive dashboard.

## Project Objectives

- Build a repeatable data ingestion pipeline
- Profile and validate raw datasets
- Clean and standardize Airbnb data
- Create analytics-ready enriched datasets
- Implement a dimensional model in DuckDB
- Perform exploratory and statistical analysis
- Build an interactive Streamlit dashboard
- Document assumptions, decisions, and limitations

## Current Status

### Completed

- **Section 02:** Dataset familiarization
  - `notebooks/01_dataset_familiarization.ipynb`
  - `docs/data_dictionary.md`
- **Section 03:** Data engineering pipeline
  - Config loader (`src/config.py`)
  - Gzip extraction (`src/extract_files.py`)
  - Dataset profiling (`src/profile_datasets.py`)
  - Data cleaning (`src/cleaning.py`)
  - Data validation (`src/validation.py`)
  - Data enrichment (`src/transformations.py`)
  - DuckDB star schema (`src/database.py`, `sql/create_*.sql`)
  - Automated orchestration (`src/pipeline.py`)

### In Progress

- Section 04: Exploratory Data Analysis
- Section 05: Statistical analysis
- Streamlit dashboard
- Final PDF report

## Technology Stack

- Python 3.13
- pandas
- DuckDB
- PyYAML
- PyArrow
- SQL
- Jupyter
- pytest

## Dataset

| Field | Value |
|---|---|
| City | Edinburgh |
| Region | Scotland |
| Country | United Kingdom |
| Snapshot date | 2026-06-23 |
| Source | [Inside Airbnb](https://insideairbnb.com/) |

## Repository Structure

- `config/` – project configuration
- `data/raw/` – original unmodified source files
- `data/interim/` – extracted gzip files
- `data/processed/` – cleaned, validated, and enriched datasets
- `data/metadata/` – profiling and validation reports
- `database/` – local DuckDB analytical database
- `notebooks/` – exploration, statistics, and modelling
- `src/` – reusable pipeline source code
- `sql/` – database schema and analytical SQL
- `dashboard/` – Streamlit application
- `tests/` – automated tests
- `reports/` – figures, tables, and final report
- `docs/` – assumptions, decisions, lineage, and disclosures

## Setup Instructions

### 1. Create virtual environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Download Edinburgh dataset

Download the Edinburgh files from [Inside Airbnb](https://insideairbnb.com/get-the-data/) and place them in:

```text
data/raw/edinburgh/2026-06-23/
```

Required files:

- `listings.csv.gz`
- `calendar.csv.gz`
- `reviews.csv.gz`
- `listings.csv`
- `reviews.csv`
- `neighbourhoods.csv`
- `neighbourhoods.geojson`

### 4. Run the full pipeline

```powershell
python -m src.pipeline
```

This executes the following steps in order:

1. Extract gzip files (skipped if interim files already exist)
2. Profile datasets
3. Clean datasets
4. Validate datasets
5. Enrich listings
6. Build DuckDB star schema

### 5. Run individual pipeline steps (optional)

```powershell
python -m src.extract_files
python -m src.profile_datasets
python -m src.cleaning
python -m src.validation
python -m src.transformations
python -m src.database
```

### 6. Run analytical SQL

```powershell
python -c "import duckdb; con=duckdb.connect('database/airbnb.duckdb'); print(con.execute(open('sql/analytical_queries.sql').read()).fetchdf())"
```

## Pipeline Outputs

| Output | Location |
|---|---|
| Dataset inventory | `data/metadata/dataset_inventory.csv` |
| Schema report | `data/metadata/schema_report.csv` |
| Validation report | `data/metadata/validation_report.csv` |
| Cleaned datasets | `data/processed/edinburgh/2026-06-23/*_clean.parquet` |
| Validated datasets | `data/processed/edinburgh/2026-06-23/*_validated.parquet` |
| Enriched listings | `data/processed/edinburgh/2026-06-23/listings_enriched.parquet` |
| DuckDB warehouse | `database/airbnb.duckdb` |

## DuckDB Star Schema

### Dimension tables

- `dw.dim_date`
- `dw.dim_neighbourhood`
- `dw.dim_host`
- `dw.dim_listing`

### Fact tables

- `dw.fact_calendar`
- `dw.fact_reviews`
- `dw.fact_listing_performance`

## Related Documentation

- `docs/data_dictionary.md` – dataset schemas and assumptions
- `docs/decision_log.md` – engineering decisions
- `docs/assumptions.md` – project assumptions
- `docs/completed_work.md` – completed work summary
- `docs/ai_usage_disclosure.md` – AI usage disclosure

## Author

Kasun Wijerathna
