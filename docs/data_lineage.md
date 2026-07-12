# Data Lineage

This document traces how Edinburgh Inside Airbnb source files flow through the
pipeline into analytical outputs and the dashboard.

Snapshot: **2026-06-23**  
City: **Edinburgh**

---

## Source to Processed Lineage

| Source file | Pipeline step | Output artifact |
|-------------|---------------|-----------------|
| `listings.csv.gz` | extract → clean → validate → enrich | `listings_clean.parquet`, `listings_validated.parquet`, `listings_enriched.parquet` |
| `calendar.csv.gz` | extract → clean → validate | `calendar_clean.parquet`, `calendar_validated.parquet` |
| `reviews.csv.gz` | extract → clean → validate | `reviews_clean.parquet`, `reviews_validated.parquet` |
| `listings.csv` | profile / comparison only | inventory + schema metadata |
| `reviews.csv` | profile / comparison only | inventory + schema metadata |
| `neighbourhoods.csv` | clean | `neighbourhoods_clean.parquet` |
| `neighbourhoods.geojson` | profile / familiarization | notebook + data dictionary references |

---

## Enrichment Joins

`src/transformations.py` enriches listings by joining:

| Feature table | Join key | Derived fields |
|---------------|----------|----------------|
| Calendar aggregates | `listing_id` | `occupancy_proxy`, `calendar_days`, `unavailable_days` |
| Review aggregates | `listing_id` | `review_count_detailed`, `latest_review_date` |
| Neighbourhood aggregates | `neighbourhood_cleansed` | `neighbourhood_median_price`, `neighbourhood_listing_count` |

---

## Warehouse Lineage

`src/database.py` loads validated/enriched parquet into DuckDB:

| Processed input | Warehouse target |
|-----------------|------------------|
| `listings_enriched.parquet` | `dw.dim_listing`, `dw.dim_host`, `dw.fact_listing_performance` |
| `calendar_validated.parquet` | `dw.fact_calendar` |
| `reviews_validated.parquet` | `dw.fact_reviews` |
| `neighbourhoods_clean.parquet` | `dw.dim_neighbourhood` |

---

## Notebook and Report Lineage

| Notebook / app | Primary inputs | Exported outputs |
|----------------|----------------|------------------|
| `02_eda_edinburgh.ipynb` | `listings_enriched.parquet`, DuckDB | `reports/figures/01`–`07_*.png` |
| `03_statistical_analysis.ipynb` | enriched listings / DuckDB | `reports/tables/hypothesis_test_summary.csv` |
| `04_ml_price_prediction.ipynb` | `listings_enriched.parquet` | `reports/tables/price_model_*.csv`, `reports/figures/08`–`09_*.png` |
| `05_nlp_reviews.ipynb` | `reviews_validated.parquet`, listings ratings | `reports/tables/review_*.csv`, `reports/figures/10`–`12_*.png` |
| `dashboard/app.py` | enriched listings + `reports/tables/*.csv` | interactive UI (no new data files) |

---

## Important Column Note: Neighbourhood

In the Edinburgh snapshot:

- `neighbourhood` is empty in the detailed listings file
- `neighbourhood_cleansed` contains the usable neighbourhood names

The enrichment step and dashboard therefore rely on `neighbourhood_cleansed`
for neighbourhood-level analysis.

---

## Validation Lineage

Validation rules in `src/validation.py` produce:

- row-level flags such as `is_valid_price`, `is_valid_date`
- `data/metadata/validation_report.csv` summarising rule failures and actions

Invalid records are flagged rather than silently dropped unless the rule
explicitly requires removal (for example duplicate IDs).
