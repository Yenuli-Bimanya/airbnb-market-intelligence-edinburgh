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
- **Section 04:** Exploratory Data Analysis
  - `notebooks/02_eda_edinburgh.ipynb`
  - 7 charts in `reports/figures/`
- **Section 05:** Statistical analysis
  - `notebooks/03_statistical_analysis.ipynb`
  - Hypothesis summary in `reports/tables/hypothesis_test_summary.csv`
- **Section 06:** Machine learning (price prediction)
  - `notebooks/04_ml_price_prediction.ipynb`
  - Model outputs in `reports/tables/` and `reports/figures/`
- **Section 07:** NLP (review text analysis)
  - `notebooks/05_nlp_reviews.ipynb`
  - Sentiment and topic outputs in `reports/tables/` and `reports/figures/`



### Remaining

- Section 08: Plotly Dash dashboard (`dashboard/app.py`) — built, pending final testing and screenshots
- Final PDF report (`reports/`)
- Optional docs: `docs/architecture.md`, `docs/data_lineage.md`

See `docs/completed_work.md` and `docs/incomplete_work.md` for full details.

## Technology Stack

- Python 3.13
- pandas
- DuckDB
- PyYAML
- PyArrow
- scikit-learn
- matplotlib
- seaborn
- scipy
- TextBlob
- SQL
- Jupyter
- pytest



## Dataset


| Field         | Value                                      |
| ------------- | ------------------------------------------ |
| City          | Edinburgh                                  |
| Region        | Scotland                                   |
| Country       | United Kingdom                             |
| Snapshot date | 2026-06-23                                 |
| Source        | [Inside Airbnb](https://insideairbnb.com/) |




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



### 7. Run the Dash dashboard

```powershell
python -m pip install dash plotly dash-bootstrap-components
python dashboard/app.py
```

Open `http://127.0.0.1:8050` in your browser.

### 8. Run analytical SQL

```powershell
python -c "import duckdb; con=duckdb.connect('database/airbnb.duckdb'); print(con.execute(open('sql/analytical_queries.sql').read()).fetchdf())"
```



## Pipeline Outputs


| Output             | Location                                                        |
| ------------------ | --------------------------------------------------------------- |
| Dataset inventory  | `data/metadata/dataset_inventory.csv`                           |
| Schema report      | `data/metadata/schema_report.csv`                               |
| Validation report  | `data/metadata/validation_report.csv`                           |
| Cleaned datasets   | `data/processed/edinburgh/2026-06-23/*_clean.parquet`           |
| Validated datasets | `data/processed/edinburgh/2026-06-23/*_validated.parquet`       |
| Enriched listings  | `data/processed/edinburgh/2026-06-23/listings_enriched.parquet` |
| DuckDB warehouse   | `database/airbnb.duckdb`                                        |




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



## Analysis Notebooks


| Notebook                           | Section | Purpose                                  |
| ---------------------------------- | ------- | ---------------------------------------- |
| `01_dataset_familiarization.ipynb` | 02      | Schema, keys, data quality exploration   |
| `02_eda_edinburgh.ipynb`           | 04      | Market EDA with business interpretations |
| `03_statistical_analysis.ipynb`    | 05      | Hypothesis testing (H1–H5)               |
| `04_ml_price_prediction.ipynb`     | 06      | Price prediction models                  |
| `05_nlp_reviews.ipynb`             | 07      | Review sentiment and topic modelling     |


Run each notebook with the `.venv` kernel after executing `python -m src.pipeline`.

## Report Outputs


| Output type     | Location                        |
| --------------- | ------------------------------- |
| EDA figures     | `reports/figures/01`–`07_*.png` |
| ML figures      | `reports/figures/08`–`09_*.png` |
| NLP figures     | `reports/figures/10`–`12_*.png` |
| Analysis tables | `reports/tables/*.csv`          |




## Related Documentation

- `docs/data_dictionary.md` – dataset schemas and assumptions
- `docs/decision_log.md` – engineering decisions
- `docs/assumptions.md` – project assumptions
- `docs/completed_work.md` – completed work summary
- `docs/incomplete_work.md` – remaining work and deferred scope
- `docs/ai_usage_disclosure.md` – AI usage disclosure





