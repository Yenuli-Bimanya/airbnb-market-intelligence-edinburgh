# COMPLETE PROJECT CONTEXT — Edinburgh Airbnb Market Intelligence
## For PDF Report Generation (paste this entire document into ChatGPT/Claude)

**Candidate:** Kasun Wijerathna  
**Assignment:** Expernetic Talent Assessment Program — Data Engineer Intern  
**Repository:** airbnb-market-intelligence-edinburgh  
**Branch:** feature/airbnb-implementation  
**Approach:** Single city (Edinburgh), depth-first, quality over quantity  

---

# 1. PROJECT SUMMARY (ONE PARAGRAPH)

I built an end-to-end Airbnb Market Intelligence solution for Edinburgh using public Inside Airbnb data (snapshot date: 2026-06-23). The project includes: (1) mandatory dataset familiarization, (2) a full Python data engineering pipeline with cleaning, validation, enrichment, and DuckDB star schema, (3) exploratory data analysis with business interpretations, (4) statistical hypothesis testing (H1–H5), (5) machine learning price prediction with three models, (6) NLP sentiment and topic analysis on guest reviews, (7) an interactive Plotly Dash dashboard, (8) unit tests, and (9) comprehensive documentation. I deliberately chose one city with exceptional depth rather than multiple cities superficially, per the assignment design philosophy.

---

# 2. BUSINESS CONTEXT

- **Role:** Data Engineer / Analyst for a hypothetical Airbnb market intelligence consultancy
- **Stakeholders:** Product managers, revenue strategists, operations leads
- **Goal:** Transform raw Inside Airbnb data into engineering artifacts, analytical insights, and business recommendations
- **City selected:** Edinburgh, Scotland, United Kingdom
- **Why Edinburgh:** Complete 7-file snapshot, manageable scope for deep analysis, strong assignment fit

---

# 3. TECHNOLOGY STACK

| Category | Tools Used |
|----------|------------|
| Language | Python 3.13 |
| Data processing | pandas, PyArrow |
| Configuration | PyYAML |
| Database / warehouse | DuckDB (local analytical SQL) |
| Statistics | scipy (Welch t-test, ANOVA, Pearson/Spearman) |
| Machine learning | scikit-learn (Ridge, Random Forest, Gradient Boosting) |
| Visualization (static) | matplotlib, seaborn |
| NLP | TextBlob (sentiment), sklearn TF-IDF + NMF (topics) |
| Dashboard | Plotly Dash, dash-bootstrap-components |
| Testing | pytest (12 unit tests, all passing) |
| Notebooks | Jupyter |
| Version control | Git, GitHub |
| AI assistance | Cursor AI / ChatGPT (disclosed in docs/ai_usage_disclosure.md) |

**NOT used (deliberately deferred):** SQL Server, SSIS, Power BI, Streamlit, Docker, cloud deployment, Airflow, BERT/LLM/RAG, multi-city processing.

---

# 4. DATA SOURCES

**Source:** Inside Airbnb (https://insideairbnb.com/)  
**Snapshot:** 2026-06-23  
**Location:** `data/raw/edinburgh/2026-06-23/`

| File | Description | Approximate size |
|------|-------------|------------------|
| listings.csv.gz | Detailed listings (primary) | 6,244 rows, 90 columns |
| listings.csv | Summary listings (comparison) | 6,258 rows, 19 columns |
| calendar.csv.gz | Daily availability per listing | 2,284,170 rows |
| reviews.csv.gz | Guest review comments | 676,263 rows |
| reviews.csv | Summary review metrics | — |
| neighbourhoods.csv | Neighbourhood lookup | 111 rows |
| neighbourhoods.geojson | Neighbourhood boundaries | GeoJSON polygons |

**Key data findings:**
- `id` is valid primary key in listing files
- `listing_id + date` is valid composite key in calendar
- 14 listings exist only in summary file, not detailed
- Summary reviews have 2,486 duplicate `listing_id + date` groups
- FK gaps: calendar 0.22% and reviews 0.09% unmatched to detailed listings
- **Critical:** raw `neighbourhood` column is 100% empty; `neighbourhood_cleansed` has 111 neighbourhoods (used everywhere in analytics)

---

# 5. REPOSITORY STRUCTURE

```
airbnb-market-intelligence-edinburgh/
├── config/config.yaml          # City, paths, file names
├── src/                        # Pipeline Python modules
│   ├── config.py
│   ├── extract_files.py
│   ├── profile_datasets.py
│   ├── cleaning.py
│   ├── validation.py
│   ├── transformations.py
│   ├── database.py
│   └── pipeline.py
├── sql/                        # DuckDB schema + queries
│   ├── create_schema.sql
│   ├── create_dimensions.sql
│   ├── create_facts.sql
│   └── analytical_queries.sql
├── notebooks/                  # 5 Jupyter notebooks (Sections 02–07)
├── dashboard/                  # Plotly Dash app
│   ├── app.py
│   └── assets/custom.css
├── tests/                      # pytest unit tests
├── data/raw/                   # Original downloads (gitignored)
├── data/interim/               # Extracted gzip CSVs (gitignored)
├── data/processed/             # Parquet outputs (gitignored)
├── data/metadata/              # Inventory, schema, validation reports
├── database/airbnb.duckdb      # DuckDB warehouse (gitignored)
├── reports/
│   ├── figures/                # 12 PNG charts
│   ├── tables/                 # 6 CSV result tables
│   └── screenshots/            # Dashboard screenshots for PDF
└── docs/                       # All documentation
```

---

# 6. SECTION 02 — DATASET FAMILIARIZATION (MANDATORY, COMPLETE)

**Notebook:** `notebooks/01_dataset_familiarization.ipynb`  
**Documentation:** `docs/data_dictionary.md`

**What I did:**
- Downloaded all 7 Edinburgh files from Inside Airbnb
- Extracted gzip files to interim CSV
- Documented row counts, column counts, file sizes in `data/metadata/dataset_inventory.csv`
- Documented schemas in `data/metadata/schema_report.csv`
- Inspected sample records for each dataset
- Inspected GeoJSON neighbourhood boundaries
- Compared detailed vs summary listings (14 summary-only listings)
- Validated primary keys (`id`) and composite keys (`listing_id + date`)
- Validated foreign-key relationships between calendar/reviews and listings
- Documented numerical ranges for price, coordinates, reviews
- Documented business domain context (listing, host, calendar, review entities)
- Documented columns needing special interpretation (price as string, availability as t/f)
- Documented dataset limitations (no true bookings, snapshot only, scraping artifacts)
- Recorded assumptions A1–A7 in data dictionary and `docs/assumptions.md`

---

# 7. SECTION 03 — DATA ENGINEERING (COMPLETE)

## 7.1 Pipeline orchestration

**Entry point:** `python -m src.pipeline`  
**Module:** `src/pipeline.py`

**Steps executed in order:**
1. `extract_files` — gzip → CSV (skipped if interim files exist)
2. `profile_datasets` — inventory + schema reports
3. `cleaning` — standardized parquet files
4. `validation` — validated parquet + validation report
5. `transformations` — enriched listings parquet
6. `database` — DuckDB star schema load

**Features:** logging, per-step timing, error handling, config-driven city paths

## 7.2 Configuration

**File:** `config/config.yaml`  
**Loader:** `src/config.py`  
- City: Edinburgh, snapshot 2026-06-23
- All paths parameterized for potential multi-city extension
- Pipeline settings: log level INFO, save parquet, fail_on_validation_error=false

## 7.3 Extraction (`src/extract_files.py`)

- Decompresses listings.csv.gz, calendar.csv.gz, reviews.csv.gz
- Output to `data/interim/edinburgh/2026-06-23/`

## 7.4 Profiling (`src/profile_datasets.py`)

- Generates `data/metadata/dataset_inventory.csv` (rows, columns, sizes)
- Generates `data/metadata/schema_report.csv` (dtypes, null counts, samples)
- Profiles all raw and interim files

## 7.5 Cleaning (`src/cleaning.py`)

**Key functions:**
- `clean_price()` — removes £/$ symbols, casts to float
- `normalize_text()` — trim whitespace, null empty strings
- `normalize_room_type()` — standardizes to Entire home/apt, Private room, etc.
- `parse_date_column()` — safe datetime parsing
- `standardize_available()` — calendar t/f → boolean

**Outputs:** `*_clean.parquet` for listings, calendar, reviews, neighbourhoods

## 7.6 Validation (`src/validation.py`)

**Listings rules:** missing_id, duplicate_id, invalid_price, invalid_latitude, invalid_longitude  
**Calendar rules:** missing_listing_id, missing_date, invalid_available  
**Reviews rules:** missing_review_id, missing_listing_id, missing_date, duplicate_review_id  

**Strategy:** Flag invalid records (e.g. `is_valid_price`) rather than silently delete all anomalies. Remove only true duplicates and null IDs.

**Output:** `data/metadata/validation_report.csv` + `*_validated.parquet`

## 7.7 Enrichment (`src/transformations.py`)

**Calendar features per listing:**
- calendar_days, unavailable_days, avg_minimum_nights
- `occupancy_proxy` = unavailable_days / calendar_days

**Review features per listing:**
- review_count_detailed, latest_review_date, first_review_date_detailed

**Neighbourhood features:**
- neighbourhood_listing_count, neighbourhood_median_price, neighbourhood_avg_rating
- Uses `neighbourhood_cleansed` as key

**Derived listing fields:**
- host_tenure_years (from hosts_time_as_host_years)
- price_per_bedroom
- review_frequency_per_year
- estimated_revenue_proxy (price × occupancy_proxy × 365)

**Output:** `listings_enriched.parquet` — 6,244 rows, 108 columns  
**Modelling subset:** 5,608 listings with valid prices

## 7.8 DuckDB star schema (`src/database.py` + `sql/`)

**Dimension tables:**
- dw.dim_date
- dw.dim_neighbourhood
- dw.dim_host
- dw.dim_listing

**Fact tables:**
- dw.fact_calendar
- dw.fact_reviews
- dw.fact_listing_performance

**Analytical SQL:** 5 business queries in `sql/analytical_queries.sql`:
1. Average price by neighbourhood
2. Top 10 hosts by listing count
3. Occupancy proxy by room type
4. Price vs review score correlation
5. Top neighbourhoods by review score

## 7.9 Unit tests (`tests/`)

12 pytest tests covering:
- clean_price, normalize_text, normalize_room_type, standardize_available
- validate_listings duplicate removal and price flagging
- build_calendar_features, build_review_features, build_neighbourhood_features
- add_derived_listing_fields

Run: `python -m pytest tests/ -v`

---

# 8. SECTION 04 — EXPLORATORY DATA ANALYSIS (COMPLETE)

**Notebook:** `notebooks/02_eda_edinburgh.ipynb`  
**Data source:** listings_enriched.parquet (5,608 valid-price listings)

**Charts produced (all saved to reports/figures/):**

| Figure | Analysis | Key finding |
|--------|----------|-------------|
| 01_median_price_by_neighbourhood.png | Median price top neighbourhoods | Strong location premium; Fairmilehead/central areas highest |
| 02_price_by_room_type.png | Price by room type | Entire home/apt commands premium over private room |
| 03_host_portfolio_distribution.png | Listings per host | Mix of single-property and small multi-listing hosts |
| 04_review_score_distribution.png | Review score histogram | Scores clustered 4.5–5.0 (rating inflation pattern) |
| 05_occupancy_proxy_by_room_type.png | Occupancy by room type | Shared/entire homes higher proxy than hotel rooms |
| 06_price_vs_review_score.png | Scatter price vs rating | Weak relationship; high price not always high rating |
| 07_listing_density_by_neighbourhood.png | Listing counts by area | Supply concentrated in tourist-heavy neighbourhoods |

**Every chart has a business interpretation cell** explaining implications for hosts, revenue managers, and market analysts.

**Not done in EDA:** Interactive geospatial map (used bar charts instead), deep seasonal time-series (partially covered in H5).

---

# 9. SECTION 05 — STATISTICAL ANALYSIS (COMPLETE)

**Notebook:** `notebooks/03_statistical_analysis.ipynb`  
**Output:** `reports/tables/hypothesis_test_summary.csv`

| Hypothesis | Question | Test | Result | Effect size | Significant? |
|------------|----------|------|--------|-------------|--------------|
| H1 | Entire home vs private room prices | Welch t-test | Entire home mean £337.12 vs Private £156.60 | Cohen's d = 0.60 | YES |
| H2 | Superhost vs non-superhost review scores | Welch t-test | Insufficient/sparse superhost data | — | NO |
| H3 | >10 reviews vs ≤10 reviews prices | Welch t-test | High-review £275.07 vs Low £311.41 | Cohen's d = -0.12 | YES |
| H4 | Neighbourhood price differences | One-way ANOVA | 80 neighbourhood groups | η² = 0.04 | YES |
| H5 | Weekend vs weekday differences | Welch t-test | Weekend min nights 3.75 vs weekday 3.82 | Cohen's d = -0.004 | YES |

**H5 important note:** Assignment asks weekend vs weekday pricing, but Edinburgh calendar lacks reliable daily price in this snapshot. I adapted H5 to compare **weekend vs weekday minimum nights** from calendar data. This is documented as a data limitation workaround.

**H2 important note:** Superhost comparison inconclusive due to sparse/missing superhost field data in usable modelling subset.

**Methodology:** Welch t-test chosen for unequal variances; effect sizes reported alongside p-values; business interpretation for each hypothesis.

**Not done:** Confidence intervals by neighbourhood, OLS regression with VIF, multi-city Bonferroni correction.

---

# 10. SECTION 06 — MACHINE LEARNING (COMPLETE)

**Notebook:** `notebooks/04_ml_price_prediction.ipynb`

**Problem:** Supervised regression — predict nightly listing price (GBP)  
**Target:** `price`  
**Filter:** `is_valid_price == True` → 5,608 listings  
**Train/test split:** 80/20 with random_state=42  
**Cross-validation:** 5-fold CV on training set  

**Features (14):**
- room_type, property_type (categorical)
- bedrooms, bathrooms, beds, accommodates
- review_scores_rating, number_of_reviews
- availability_365, occupancy_proxy
- host_tenure_years
- neighbourhood_median_price, neighbourhood_listing_count, neighbourhood_avg_rating

**Preprocessing pipeline:**
- ColumnTransformer with SimpleImputer + OneHotEncoder (categorical) + SimpleImputer (numeric)

**Models trained:**
1. Ridge Regression (alpha=1.0)
2. Random Forest Regressor
3. Gradient Boosting Regressor

**Results (`reports/tables/price_model_comparison.csv`):**

| Model | CV MAE | Test MAE | Test RMSE | Test R² |
|-------|--------|----------|-----------|---------|
| Gradient Boosting | 93.23 | 93.84 | 330.99 | 0.0848 |
| Ridge Regression | 94.31 | 94.04 | 320.05 | 0.1442 |
| Random Forest | 94.83 | 96.82 | 332.54 | 0.0761 |

**Best model by test MAE:** Gradient Boosting (~£94 average error)

**Explainability:** Random Forest feature importance (`reports/tables/price_model_feature_importance.csv`):
Top drivers: number_of_reviews, bedrooms, accommodates, neighbourhood_avg_rating, neighbourhood_median_price, host_tenure_years, review_scores_rating, bathrooms, occupancy_proxy

**Charts:**
- `08_price_model_residuals.png` — where model over/under-predicts
- `09_price_model_feature_importance.png` — top 15 price drivers

**Limitations:** Low R² (~0.08–0.14) means price driven by unobserved factors; no SHAP/LIME (used RF importance); no demand forecasting or clustering (Sec 6.2–6.3 not done).

---

# 11. SECTION 07 — NLP ON REVIEWS (COMPLETE)

**Notebook:** `notebooks/05_nlp_reviews.ipynb`  
**Data:** `reviews_validated.parquet` — 676,263 reviews with comments

**Sampling strategy (reproducible, random_state=42):**
- Sentiment: 20,000 review sample
- Topic modelling: 10,000 review sample
(Full 676k corpus too heavy for notebook topic modelling)

**Sentiment analysis:**
- Tool: TextBlob
- Outputs per review: polarity (-1 to +1), subjectivity (0 to 1)
- Labels: negative / neutral / positive based on polarity thresholds
- Finding: Guest language predominantly positive

**Sentiment vs rating:**
- Reviews have no per-review star rating in Inside Airbnb data
- Aggregated mean polarity per listing, joined with listing `review_scores_rating`
- Pearson correlation weak/unreliable on sample (documented honestly)
- Insight: text sentiment and star ratings measure different signals

**Topic modelling:**
- Method: TF-IDF vectorization + NMF (8 topics)
- Preprocessing: lowercase, remove punctuation, English stop words, min 3-letter tokens

**Topics discovered (`reports/tables/review_topic_summary.csv`):**

| Topic | Label | Top words | Reviews in sample |
|-------|-------|-----------|-------------------|
| 0 | City centre access | flat, city, walk, edinburgh, clean, centre | 2,459 |
| 1 | Host communication | great, host, communication, responsive | 1,383 |
| 2 | Highly recommended stays | recommend, highly, amazing, perfect | 1,235 |
| 3 | Value for money | value, money, accommodation, price | 591 |
| 4 | Non-English reviews | est, nous, bien, pour (French) | 1,440 |
| 5 | Apartment quality | apartment, perfect, lovely, beautiful | 1,275 |
| 6 | Room comfort and quietness | room, quiet, clean, helpful | 892 |
| 7 | Enjoyable experience | stay, enjoyed, lovely, wonderful | 725 |

**Charts:**
- `10_review_sentiment_distribution.png`
- `11_sentiment_vs_rating_scatter.png`
- `12_review_topic_distribution.png`

**Not done:** NER, BERTopic, LLM/RAG, Q&A interface, review quality classifier.

---

# 12. SECTION 08 — INTERACTIVE DASHBOARD (COMPLETE)

**Technology:** Plotly Dash (NOT Streamlit)  
**File:** `dashboard/app.py`  
**Styling:** `dashboard/assets/custom.css` (professional light theme, navy header)  
**Run:** `python dashboard/app.py` → http://127.0.0.1:8050

**KPI cards:**
- Listings analysed: 5,608
- Median price: £230/night
- Mean review score: 4.78/5
- Mean occupancy proxy: 58.86%

**Four tabs:**

1. **Market Explorer** — Filters for neighbourhood (neighbourhood_cleansed) and room type; 4 interactive charts (median price by neighbourhood, price boxplot by room type, price vs review scatter, occupancy by room type)

2. **Reviews & NLP** — Topic bar chart from NMF results + sentiment vs rating insight card

3. **ML Insights** — Model comparison bar chart + Random Forest feature importance

4. **Statistical Tests** — Full H1–H5 hypothesis results table

**Dashboard screenshots taken** for PDF (overview, market explorer filtered/unfiltered, NLP, ML, stats).

**Bug fixed:** Dashboard initially used empty `neighbourhood` column; fixed to use `neighbourhood_cleansed`.

---

# 13. DOCUMENTATION DELIVERED

| Document | Purpose |
|----------|---------|
| README.md | Setup, run instructions, project status |
| docs/data_dictionary.md | Full schema, assumptions, limitations |
| docs/completed_work.md | Everything completed Sec 02–08 |
| docs/incomplete_work.md | Honest list of what was not done |
| docs/architecture.md | Pipeline + warehouse architecture |
| docs/data_lineage.md | Source-to-output lineage |
| docs/assumptions.md | 10 project assumptions |
| docs/decision_log.md | 8 engineering decisions with trade-offs |
| docs/ai_usage_disclosure.md | AI tools, assisted sections, validation |
| reports/PDF_REPORT_OUTLINE.md | PDF section plan |

---

# 14. KEY ENGINEERING DECISIONS

1. **Python 3.13** — modern environment
2. **DuckDB over PostgreSQL/SQLite** — local analytical SQL, no server, Parquet-native
3. **Single-city Edinburgh depth-first** — quality over multi-city breadth
4. **Parquet over CSV** for processed data — performance and typing
5. **Plotly Dash over Streamlit** — more professional interactive analytics UI
6. **TextBlob + NMF over BERT/LLM** — interpretable, fast, assignment-appropriate
7. **neighbourhood_cleansed** — raw neighbourhood column empty in data
8. **Flag-and-retain validation** — transparency over silent deletion

---

# 15. KEY ASSUMPTIONS

- A1: Detailed listings is primary source for engineering
- A2: Summary listings for validation/comparison only
- A3: Calendar unavailable days = occupancy proxy (NOT confirmed bookings)
- A4: Orphan FK rows flagged, not silently removed
- A5: listing_id is standard join key
- A6: neighbourhood_cleansed used because neighbourhood is empty
- A7: Findings apply only to Edinburgh 2026-06-23 snapshot
- ML: Feature importance shows association not causation
- NLP: Sampled subsets for reproducibility and runtime

---

# 16. WHAT WAS NOT DONE (HONEST)

- Multi-city comparison
- Docker / cloud deployment / Airflow orchestration
- Incremental CDC processing
- Great Expectations / dbt
- Interactive geospatial map (Folium)
- SHAP/LIME explainability
- Demand forecasting, clustering segmentation
- NER, LLM, RAG, recommendation systems
- End-to-end pipeline integration test
- Final PDF report (being created now)

---

# 17. REPRODUCIBILITY INSTRUCTIONS

```powershell
cd airbnb-market-intelligence-edinburgh
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
# Place raw data in data/raw/edinburgh/2026-06-23/
python -m src.pipeline
python -m pytest tests/ -v
python dashboard/app.py
# Run notebooks with .venv kernel
```

---

# 18. GIT COMMIT HISTORY (CHRONOLOGICAL)

1. Initial commit
2. Edinburgh dataset setup and extraction
3. Profiling and schema samples
4. Primary key validation
5. Dataset familiarization notebook complete
6. Data dictionary and completed work
7. Config loader and refactor
8. Cleaning module
9. Validation rules
10. Listing enrichment
11. DuckDB star schema
12. Automated pipeline
13. EDA notebook
14. Statistical analysis notebook
15. ML notebook
16. ML + NLP notebooks with outputs
17. Documentation update Sec 02–07
18. Dash dashboard
19. Final docs, tests, dashboard polish

---

# 19. KEY NUMBERS TO USE IN PDF

| Metric | Value |
|--------|-------|
| City | Edinburgh |
| Snapshot | 2026-06-23 |
| Detailed listings | 6,244 |
| Valid-price listings | 5,608 |
| Calendar rows | 2,284,170 |
| Review comments | 676,263 |
| Neighbourhoods | 111 |
| Median price | £230 |
| Mean review score | 4.78 |
| Mean occupancy proxy | 58.86% |
| H1 entire home price | £337.12 |
| H1 private room price | £156.60 |
| Best ML test MAE | £93.84 (Gradient Boosting) |
| ML test R² | 0.0848 (Gradient Boosting) |
| Unit tests | 12 passing |

---

# 20. BUSINESS RECOMMENDATIONS (FOR PDF SECTION 11)

**For hosts:**
- Price entire homes at premium to private rooms (H1 proves significant gap)
- Benchmark against neighbourhood median price
- Focus on communication and cleanliness (top NLP themes)
- Use occupancy proxy for revenue planning, not as confirmed bookings

**For consultancy clients:**
- Use Dash dashboard for interactive neighbourhood filtering
- Combine structured ratings with NLP topics for quality monitoring
- Segment pricing models by room type (ML residuals vary by segment)

**For platform/policy:**
- High uniform ratings may indicate rating inflation
- Multilingual reviews need language-aware NLP in production

---

# 21. AI USAGE (FOR APPENDIX A)

- Tools: ChatGPT, Cursor AI
- Assisted: pipeline design, notebooks, dashboard, documentation
- Validation: all code executed locally, pytest run, manual notebook review
- Candidate modified: scope decisions, neighbourhood_cleansed fix, H5 adaptation
- Full disclosure in docs/ai_usage_disclosure.md

---

# 22. INSTRUCTIONS FOR CHATGPT/CLAUDE

Using ALL the information above, generate a professional PDF report for the Expernetic Data Engineer Intern assignment with these 15 sections + Appendix A:

1. Executive Summary (1 page, business-oriented)
2. Objectives & Scope (prioritization rationale)
3. Dataset Overview
4. Methodology
5. Engineering Approach (pipeline, star schema, decision log)
6. EDA Findings (with business interpretation for each figure)
7. Statistical Findings (H1–H5 with effect sizes)
8. Data Science Experiments (ML models, metrics, feature importance)
9. AI/ML Experiments (NLP sentiment + topics)
10. Visualizations (reference all 12 figures + 6 dashboard screenshots)
11. Business Recommendations
12. Cross-City Comparisons (N/A — explain single-city choice)
13. Limitations & Caveats
14. Future Improvements
15. Reflection
Appendix A: AI Usage Disclosure

**Requirements:** Minimum 20 pages, professional tone, readable by technical and non-technical stakeholders, numbered sections, figure captions, honest about limitations.

**Design philosophy to emphasize:** Quality over quantity. Depth-first Edinburgh approach. Exceptional depth in chosen sections over superficial coverage of all sections.
