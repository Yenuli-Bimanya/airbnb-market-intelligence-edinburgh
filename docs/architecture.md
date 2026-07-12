# System Architecture

This document describes the Edinburgh Airbnb Market Intelligence solution
architecture across ingestion, processing, storage, analytics, and presentation.

---

## High-Level Pipeline

```text
Inside Airbnb raw files (CSV / GeoJSON / gzip)
        |
        v
  src/extract_files.py
        |
        v
  data/interim/edinburgh/2026-06-23/
        |
        +--> src/profile_datasets.py --> data/metadata/
        |
        v
  src/cleaning.py --> *_clean.parquet
        |
        v
  src/validation.py --> *_validated.parquet + validation_report.csv
        |
        v
  src/transformations.py --> listings_enriched.parquet
        |
        v
  src/database.py + sql/create_*.sql --> database/airbnb.duckdb
        |
        +--> notebooks/ (EDA, stats, ML, NLP)
        |
        +--> reports/figures + reports/tables
        |
        v
  dashboard/app.py (Plotly Dash)
```

---

## Orchestration

`src/pipeline.py` runs the end-to-end workflow in order:

1. Extract gzip files
2. Profile datasets
3. Clean datasets
4. Validate datasets
5. Enrich listings
6. Build DuckDB warehouse

Configuration is centralised in `config/config.yaml` and loaded through
`src/config.py`.

---

## Storage Layers

| Layer | Purpose | Example path |
|-------|---------|--------------|
| Raw | Unmodified source files | `data/raw/edinburgh/2026-06-23/` |
| Interim | Extracted gzip CSV files | `data/interim/edinburgh/2026-06-23/` |
| Processed | Clean, validated, enriched parquet | `data/processed/edinburgh/2026-06-23/` |
| Metadata | Profiling and validation reports | `data/metadata/` |
| Warehouse | Analytical SQL database | `database/airbnb.duckdb` |
| Reports | Figures and tables for reporting | `reports/figures/`, `reports/tables/` |

---

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

SQL definitions live in:

- `sql/create_schema.sql`
- `sql/create_dimensions.sql`
- `sql/create_facts.sql`
- `sql/analytical_queries.sql`

---

## Analytics Layer

| Component | Role |
|-----------|------|
| `notebooks/02_eda_edinburgh.ipynb` | Exploratory market analysis |
| `notebooks/03_statistical_analysis.ipynb` | Hypothesis testing (H1–H5) |
| `notebooks/04_ml_price_prediction.ipynb` | Supervised price modelling |
| `notebooks/05_nlp_reviews.ipynb` | Review sentiment and topic modelling |
| `dashboard/app.py` | Interactive presentation layer |

---

## Design Principles

- **Single-city depth-first scope** for Edinburgh
- **Reproducible batch pipeline** driven by config and module entry points
- **Parquet intermediate format** for efficient downstream reads
- **Validation before enrichment** so downstream analytics use flagged, auditable data
- **Separation of batch analytics and dashboard presentation**
