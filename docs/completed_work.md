# Completed Work Summary

This document records the work completed so far for the Expernetic Data
Engineering Intern assignment. The project focuses on Edinburgh using a single-
city, depth-first approach.

---

## Section 02: Dataset Familiarization (Mandatory)

**Status:** Complete

| Task | Status | Evidence |
|------|--------|----------|
| Download Edinburgh Inside Airbnb snapshot (2026-06-23) | Done | `data/raw/edinburgh/2026-06-23/` |
| Extract gzip source files | Done | `src/extract_files.py` |
| Document file inventory (rows, columns, sizes) | Done | `data/metadata/dataset_inventory.csv`, notebook Section 1 |
| Document schemas for all 7 datasets | Done | `data/metadata/schema_report.csv`, notebook Section 1 |
| Inspect representative sample records | Done | `notebooks/01_dataset_familiarization.ipynb` Section 2 |
| Inspect GeoJSON neighbourhood boundaries | Done | Notebook geojson summary cell |
| Compare detailed vs summary listings coverage | Done | Notebook Section 3 (14 summary-only listings found) |
| Validate primary and composite keys | Done | Notebook key validation cells |
| Validate foreign-key relationships | Done | Notebook relationship report |
| Document numerical ranges for key fields | Done | Notebook Section 5 |
| Document business domain context | Done | Notebook Section 6 |
| Document columns requiring special interpretation | Done | Notebook Section 7, `docs/data_dictionary.md` |
| Document dataset limitations | Done | Notebook Section 8, `docs/data_dictionary.md` |
| Document project assumptions | Done | Notebook Section 9, `docs/assumptions.md` |
| Produce standalone data dictionary | Done | `docs/data_dictionary.md` |

### Key findings recorded

- Edinburgh snapshot contains 7 source datasets across listings, calendar,
  reviews and neighbourhoods.
- Detailed listings: 6,244 rows and 90 columns.
- Summary listings: 6,258 rows and 19 columns.
- Calendar: 2,284,170 daily records.
- Detailed reviews: 676,263 records.
- `id` is a valid primary key in both listing files.
- `listing_id + date` is a valid composite key in the calendar file.
- Summary reviews contain 2,486 duplicate `listing_id + date` groups.
- Small referential integrity gaps exist between calendar/reviews and detailed
  listings (0.22% and 0.09% unmatched child rows).

---

## Section 03: Data Engineering (Recommended)

**Status:** Complete

| Task | Status | Evidence |
|------|--------|----------|
| Centralised configuration loader | Done | `src/config.py`, `config/config.yaml` |
| Gzip extraction workflow | Done | `src/extract_files.py` |
| Dataset profiling | Done | `src/profile_datasets.py`, `data/metadata/` |
| Data cleaning (listings, calendar, reviews, neighbourhoods) | Done | `src/cleaning.py` |
| Data validation rules and reporting | Done | `src/validation.py`, `data/metadata/validation_report.csv` |
| Listing enrichment and feature engineering | Done | `src/transformations.py`, `listings_enriched.parquet` |
| DuckDB star schema implementation | Done | `src/database.py`, `sql/create_*.sql` |
| Analytical SQL queries | Done | `sql/analytical_queries.sql` |
| Automated pipeline orchestration | Done | `src/pipeline.py` (`python -m src.pipeline`) |
| Automated tests for core modules | Done | `tests/test_cleaning.py`, `tests/test_validation.py`, `tests/test_transformations.py` |

### Pipeline outputs

| Output | Location |
|--------|----------|
| Cleaned datasets | `data/processed/edinburgh/2026-06-23/*_clean.parquet` |
| Validated datasets | `data/processed/edinburgh/2026-06-23/*_validated.parquet` |
| Enriched listings | `data/processed/edinburgh/2026-06-23/listings_enriched.parquet` |
| DuckDB warehouse | `database/airbnb.duckdb` |

### DuckDB star schema

**Dimension tables:** `dw.dim_date`, `dw.dim_neighbourhood`, `dw.dim_host`, `dw.dim_listing`

**Fact tables:** `dw.fact_calendar`, `dw.fact_reviews`, `dw.fact_listing_performance`

---

## Section 04: Exploratory Data Analysis (Recommended)

**Status:** Complete

| Task | Status | Evidence |
|------|--------|----------|
| Load analytics-ready data from pipeline outputs | Done | `notebooks/02_eda_edinburgh.ipynb` |
| Analyse price distributions by neighbourhood | Done | Chart `01_median_price_by_neighbourhood.png` |
| Compare prices across room types | Done | Chart `02_price_by_room_type.png` |
| Examine host portfolio concentration | Done | Chart `03_host_portfolio_distribution.png` |
| Explore review score patterns | Done | Chart `04_review_score_distribution.png` |
| Analyse occupancy proxy by room type | Done | Chart `05_occupancy_proxy_by_room_type.png` |
| Investigate price vs review score relationship | Done | Chart `06_price_vs_review_score.png` |
| Map listing density by neighbourhood | Done | Chart `07_listing_density_by_neighbourhood.png` |
| Provide business interpretations | Done | Interpretation cells in notebook |

### Key EDA insights

- Entire-home listings dominate the premium price segment.
- Neighbourhood location is a major driver of median nightly price.
- Review scores are generally high, with limited variance across listings.
- Occupancy proxy varies materially by room type and availability patterns.
- Host portfolio concentration suggests a mix of single-property and multi-listing operators.

---

## Section 05: Statistical Analysis (Recommended)

**Status:** Complete

| Task | Status | Evidence |
|------|--------|----------|
| Define and test market hypotheses | Done | `notebooks/03_statistical_analysis.ipynb` |
| H1: Entire home vs private room prices | Done | Welch t-test |
| H2: Superhost vs non-superhost review scores | Done | Welch t-test |
| H3: High-review vs low-review listing prices | Done | Welch t-test |
| H4: Neighbourhood price differences | Done | One-way ANOVA |
| H5: Weekend vs weekday calendar patterns | Done | Minimum nights comparison (calendar has no daily price) |
| Export hypothesis summary table | Done | `reports/tables/hypothesis_test_summary.csv` |
| Business interpretation per hypothesis | Done | Interpretation markdown cells |

---

## Section 06: Machine Learning — Price Prediction (Optional)

**Status:** Complete

| Task | Status | Evidence |
|------|--------|----------|
| Frame supervised regression problem | Done | `notebooks/04_ml_price_prediction.ipynb` |
| Engineer features from enriched listings | Done | 14 modelling features |
| Train Ridge Regression baseline | Done | Model comparison table |
| Train Random Forest regressor | Done | Model comparison table |
| Train Gradient Boosting regressor | Done | Model comparison table |
| Evaluate with cross-validation and hold-out test | Done | MAE, RMSE, R² metrics |
| Analyse residuals | Done | `reports/figures/08_price_model_residuals.png` |
| Analyse feature importance | Done | `reports/figures/09_price_model_feature_importance.png` |
| Export model outputs | Done | `reports/tables/price_model_comparison.csv`, `price_model_feature_importance.csv` |

### Key ML findings

- Gradient Boosting achieved the strongest overall performance among the three models tested.
- Location proxies, room configuration, and review performance are among the top price drivers.
- Model error is highest for premium and unusual listings, indicating segment-specific pricing effects.

---

## Section 07: NLP — Review Text Analysis (Optional)

**Status:** Complete

| Task | Status | Evidence |
|------|--------|----------|
| Load validated review comments from pipeline | Done | `notebooks/05_nlp_reviews.ipynb` |
| Score sentiment polarity and subjectivity | Done | TextBlob on 20,000-review sample |
| Compare text sentiment with listing ratings | Done | Listing-level aggregation + correlation |
| Discover review themes with TF-IDF + NMF | Done | 8 topics on 10,000-review sample |
| Export sentiment distribution chart | Done | `reports/figures/10_review_sentiment_distribution.png` |
| Export sentiment vs rating scatter chart | Done | `reports/figures/11_sentiment_vs_rating_scatter.png` |
| Export topic distribution chart | Done | `reports/figures/12_review_topic_distribution.png` |
| Export NLP summary tables | Done | `reports/tables/review_sentiment_summary.csv`, `review_sentiment_rating_correlation.csv`, `review_topic_summary.csv` |

### Key NLP findings

- Guest review language is predominantly positive in tone.
- Text sentiment correlates weakly with listing star ratings because they measure different signals.
- Recurring themes include location, host communication, cleanliness, value, and recommendation language.
- Multilingual reviews (for example French) appear as a separate topic cluster.

---

## Project Setup and Documentation

**Status:** Complete

| Task | Status | Evidence |
|------|--------|----------|
| Initialise repository structure | Done | `src/`, `data/`, `sql/`, `docs/`, `dashboard/`, `tests/` |
| Configure project settings | Done | `config/config.yaml` |
| Add `.gitignore` for data and environment files | Done | `.gitignore` |
| Record engineering decisions | Done | `docs/decision_log.md` |
| Record initial assumptions | Done | `docs/assumptions.md` |
| Record AI usage disclosure | Done | `docs/ai_usage_disclosure.md` |
| Create project README | Done | `README.md` |
| Create data dictionary | Done | `docs/data_dictionary.md` |

---

## Git History (Key Commits)

| Commit | Description |
|--------|-------------|
| `5ec668f` | ML and NLP analysis notebooks with report outputs |
| `aefbda6` | ML price prediction notebook and model outputs |
| `0814bb1` | Statistical hypothesis testing notebook |
| `cc44219` | Edinburgh EDA notebook with business interpretations |
| `af14aa8` | Automated pipeline and project documentation |
| `c5a5bb4` | DuckDB star schema and analytical warehouse tables |
| `30dc7ae` | Listing enrichment with calendar, review and neighbourhood features |
| `fd766be` | Data validation rules and validation report |
| `06be874` | Data cleaning module for listings, calendar and reviews |
| `401e6d3` | Dataset familiarization notebook with domain context |

---

## Standard Achieved

The completed work meets the mandatory Section 02 requirements and delivers strong
depth across Sections 03–07. The solution includes:

- A reproducible end-to-end data engineering pipeline
- A DuckDB dimensional model with analytical SQL
- Five analysis notebooks covering EDA, statistics, ML, and NLP
- Exported figures and tables ready for the final report
- Supporting documentation, assumptions, and decision records

### Next planned stage

Section 08: Streamlit dashboard, final PDF report, and remaining documentation
(`docs/incomplete_work.md`, architecture/lineage updates if required).
