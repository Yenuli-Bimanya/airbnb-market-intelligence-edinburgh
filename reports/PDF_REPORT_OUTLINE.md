# Edinburgh Airbnb Market Intelligence — Final PDF Report Outline

**Assignment:** Expernetic Talent Assessment Program — Data Engineer Intern  
**Candidate:** Kasun Wijerathna  
**City:** Edinburgh (single-city, depth-first)  
**Snapshot:** 2026-06-23  
**Target length:** Minimum 20 pages (aim for 24–28 pages)

Use this document as your writing plan. Copy sections into Word/Google Docs, insert figures/screenshots, export as PDF to:

`reports/airbnb_market_intelligence_edinburgh.pdf`

---

## How to score highly (rubric alignment)

| Rubric dimension | Weight | How your report should prove it |
|------------------|--------|----------------------------------|
| Problem Solving | 30% | Clear prioritization, trade-offs, why Edinburgh-only |
| Data Engineering Quality | 25% | Pipeline, star schema, validation, lineage |
| Statistical Thinking | 20% | H1–H5 with tests, effect sizes, assumptions |
| Analytical Storytelling | 20% | Business interpretation after every chart |
| Data Science & ML | 15% | 3 models, CV, residuals, feature importance |
| AI/ML Experimentation | 10% | NLP sentiment + topics; honest limits |
| Code Quality | 20% | Reproducibility, tests, modular `src/` |
| Communication | 20% | Non-technical executive summary |
| Creativity & Initiative | 20% | Dash dashboard as Open Innovation (Sec 08) |
| Prioritization | 15% | Completed vs incomplete work with rationale |
| Professionalism | 15% | TOC, page numbers, consistent formatting |
| AI Usage Disclosure | 10% | Appendix A — transparent and detailed |

**Key message for evaluators:** You chose depth over breadth. One city, end-to-end, production-style pipeline, four analysis notebooks, dashboard, and honest scope boundaries.

---

## Report structure (matches Assignment Section 12 exactly)

| # | Section | Suggested pages | Your evidence |
|---|---------|-----------------|---------------|
| 1 | Executive Summary | 1 | Write last |
| 2 | Objectives & Scope | 1–2 | Edinburgh focus, prioritization |
| 3 | Dataset Overview | 2–3 | Notebook 01, data dictionary |
| 4 | Methodology | 1–2 | Overall analytical approach |
| 5 | Engineering Approach | 3–4 | Pipeline, DuckDB, decisions |
| 6 | EDA Findings | 3–4 | Notebook 02, figures 01–07 |
| 7 | Statistical Findings | 2–3 | Notebook 03, hypothesis table |
| 8 | Data Science Experiments | 2–3 | Notebook 04, ML figures |
| 9 | AI/ML Experiments | 2–3 | Notebook 05, NLP figures |
| 10 | Visualizations | 1–2 | Figure gallery + dashboard screenshots |
| 11 | Business Recommendations | 1–2 | Actionable for hosts/consultancy |
| 12 | Cross-City Comparisons | 0.5 | N/A — explain why skipped |
| 13 | Limitations & Caveats | 1–2 | Data + method limits |
| 14 | Future Improvements | 1 | From incomplete_work.md |
| 15 | Reflection | 1 | Prioritization lessons |
| A | AI Usage Disclosure | 2–3 | docs/ai_usage_disclosure.md |
| | **Total** | **24–28** | |

---

## Section 1 — Executive Summary (1 page)

**Write this LAST** after all other sections are done.

### Draft content (adapt and tighten)

This report presents an end-to-end Airbnb market intelligence solution for **Edinburgh** using Inside Airbnb snapshot data (2026-06-23). The project delivers a reproducible data engineering pipeline, a DuckDB dimensional warehouse, exploratory and statistical analysis, machine learning price models, NLP review analysis, and an interactive Plotly Dash dashboard.

**Key findings:**

1. **Pricing:** Entire-home listings command significantly higher prices than private rooms (H1, Cohen's d ≈ 0.60). Neighbourhood location is a major price driver.
2. **Market structure:** Review scores are consistently high (mean ≈ 4.78/5), suggesting rating inflation or a mature, quality-focused market.
3. **Demand proxy:** Occupancy proxy is highest for shared rooms and entire homes; hotel rooms show lower estimated occupancy.
4. **ML:** Gradient Boosting achieved the lowest test MAE (~£94/night) among three models, with review count, bedrooms, and neighbourhood features among top drivers.
5. **NLP:** Guest reviews are predominantly positive. Recurring themes include location, host communication, cleanliness, and value. Text sentiment and star ratings measure different signals.

**Recommendations for a market intelligence consultancy:**

- Price entire-home inventory using neighbourhood benchmarks and room configuration.
- Coach hosts on communication and cleanliness — dominant review themes.
- Use calendar-based occupancy proxy for revenue estimation, not as confirmed bookings.
- Deploy the Dash dashboard for stakeholder self-serve exploration.

**Scope note:** Single-city depth-first approach per assignment design philosophy (quality over quantity).

---

## Section 2 — Objectives & Scope (1–2 pages)

### 2.1 Business context (from assignment Section 01)

- Role: Data Engineer/Analyst for hypothetical Airbnb market intelligence consultancy
- Stakeholders: product managers, revenue strategists, operations leads
- Goal: Transform Inside Airbnb raw data into engineering artifacts, insights, and recommendations

### 2.2 Project objectives

| Objective | Addressed in |
|-----------|--------------|
| Repeatable ingestion pipeline | `src/pipeline.py` |
| Data profiling and validation | `src/profile_datasets.py`, `src/validation.py` |
| Analytics-ready enriched data | `src/transformations.py` |
| Dimensional analytical model | DuckDB + `sql/create_*.sql` |
| EDA with business interpretation | `notebooks/02_eda_edinburgh.ipynb` |
| Statistical hypothesis testing | `notebooks/03_statistical_analysis.ipynb` |
| ML price prediction | `notebooks/04_ml_price_prediction.ipynb` |
| NLP on reviews | `notebooks/05_nlp_reviews.ipynb` |
| Interactive dashboard | `dashboard/app.py` (Open Innovation — Assignment Sec 08) |

### 2.3 Prioritization rationale (CRITICAL for full marks)

**Chosen strategy:** 1 city (Edinburgh), depth-first.

**Why:**

- Assignment explicitly states quality beats superficial multi-section coverage
- Edinburgh snapshot is complete (7 files, 6,244 listings, 676k reviews)
- Depth allows production-style pipeline + warehouse + 4 notebooks + dashboard

**Deferred (honest list — ties to Section 13 & incomplete_work.md):**

- Multi-city harmonization
- Cloud deployment, Docker, CDC, 50-city scale (Sec 03.6)
- LLM/RAG, NER, recommendation systems (Sec 07.2–7.3)
- Demand forecasting, clustering segmentation (Sec 06.2–6.3)
- Interactive geospatial map (used neighbourhood bar charts instead)

---

## Section 3 — Dataset Overview (2–3 pages)

**Maps to Assignment Section 02 (Mandatory)**

### 3.1 Data source

- Inside Airbnb: https://insideairbnb.com/
- Download page, data dictionary, behind-the-data methodology (cite URLs)
- Edinburgh, Scotland, UK — snapshot 2026-06-23

### 3.2 Files used (all 7)

| File | Rows (approx) | Role |
|------|---------------|------|
| listings.csv.gz | 6,244 | Primary listing attributes |
| listings.csv | 6,258 | Summary comparison |
| calendar.csv.gz | 2,284,170 | Daily availability |
| reviews.csv.gz | 676,263 | Review text |
| reviews.csv | — | Summary metrics |
| neighbourhoods.csv | 111 | Neighbourhood lookup |
| neighbourhoods.geojson | 111 | Spatial boundaries |

### 3.3 Schema and relationships

- **PK:** `id` in listings; `listing_id + date` in calendar
- **FK gaps:** calendar 0.22%, reviews 0.09% unmatched to detailed listings
- **Key limitation:** `neighbourhood` column empty; use `neighbourhood_cleansed`
- **Duplicates:** 2,486 duplicate groups in summary reviews

### 3.4 Domain context

| Entity | Business meaning |
|--------|------------------|
| Listing | Short-term rental property offered on Airbnb |
| Host | Supplier managing one or more listings |
| Calendar row | Daily availability/price snapshot |
| Review | Guest feedback; demand and quality signal |

### 3.5 Assumptions (reference docs/assumptions.md A1–A10)

Include table of assumptions before analysis proceeds.

### 3.6 Figures/tables to include

- Dataset inventory excerpt from `data/metadata/dataset_inventory.csv`
- Schema excerpt from `data/metadata/schema_report.csv`
- Optional: ER diagram listing → calendar → reviews

---

## Section 4 — Methodology (1–2 pages)

### 4.1 Overall approach

```text
Familiarize → Engineer → Model → Analyze → Experiment → Present
```

1. **Understand data** (notebook 01, data dictionary)
2. **Build pipeline** (extract, profile, clean, validate, enrich, load)
3. **Warehouse** (DuckDB star schema)
4. **EDA** (patterns + business interpretation)
5. **Statistics** (formal hypothesis tests)
6. **ML** (supervised price regression)
7. **NLP** (sentiment + topic modelling on samples)
8. **Dashboard** (stakeholder-facing synthesis)

### 4.2 Tooling choices

| Layer | Tool | Rationale |
|-------|------|-----------|
| Processing | pandas, PyArrow | Standard Python analytics |
| Config | YAML | City-agnostic pipeline |
| Warehouse | DuckDB | Local analytical SQL, no server |
| Stats | scipy, Welch t-test, ANOVA | Appropriate for group comparisons |
| ML | scikit-learn | Ridge, RF, Gradient Boosting |
| NLP | TextBlob, TF-IDF, NMF | Interpretable, fast |
| Dashboard | Plotly Dash | Interactive multi-tab analytics |
| Tests | pytest | 12 unit tests |

### 4.3 Reproducibility

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m src.pipeline
python -m pytest tests/ -v
python dashboard/app.py
```

---

## Section 5 — Engineering Approach (3–4 pages)

**Maps to Assignment Section 03 (Recommended) — highest weight area**

### 5.1 Pipeline design (3.1–3.5)

**Include architecture diagram** from `docs/architecture.md`:

```text
raw → extract → profile → clean → validate → enrich → DuckDB → notebooks/dashboard
```

| Step | Module | Output |
|------|--------|--------|
| Extract | `src/extract_files.py` | interim CSV |
| Profile | `src/profile_datasets.py` | inventory, schema reports |
| Clean | `src/cleaning.py` | `*_clean.parquet` |
| Validate | `src/validation.py` | `*_validated.parquet`, validation_report |
| Enrich | `src/transformations.py` | `listings_enriched.parquet` |
| Load | `src/database.py` | `airbnb.duckdb` |
| Orchestrate | `src/pipeline.py` | full ETL |

### 5.2 Address each assignment bullet honestly

| Assignment requirement | Your status | What to write |
|------------------------|-------------|---------------|
| Repeatable ingestion | ✅ Done | Config-driven `config.yaml` |
| Profiling (nulls, cardinality) | ✅ Done | `dataset_inventory.csv`, `schema_report.csv` |
| Duplicate detection | ✅ Done | Notebook 01 + validation rules |
| Outlier identification | ✅ Done | Profiling + validation price bounds |
| Domain validation | ✅ Done | Lat/long bounds, price range, FK checks |
| Price standardization | ✅ Done | `clean_price()` removes £, $ |
| Date parsing | ✅ Done | `parse_date_column()` |
| Text normalization | ✅ Done | room type, property type |
| Missing value strategy | ✅ Done | Flag vs remove documented |
| Enrichment joins | ✅ Done | Calendar, reviews, neighbourhood aggregates |
| Derived fields | ✅ Done | occupancy_proxy, price_per_bedroom, host_tenure |
| Star schema | ✅ Done | 4 dims + 3 facts |
| Analytical SQL | ✅ Done | `sql/analytical_queries.sql` |
| Automated pipeline | ✅ Done | `python -m src.pipeline` |
| Logging & error handling | ✅ Done | `src/pipeline.py` |
| Incremental processing | ⚠️ Partial | Describe approach; snapshot batch for assignment |
| Metadata management | ✅ Done | `data/metadata/` timestamps in reports |
| Data lineage | ✅ Done | `docs/data_lineage.md` |
| Cloud/Docker/CDC (3.6) | ❌ Deferred | 1 paragraph in Future Improvements |

### 5.3 Star schema (include diagram)

**Dimensions:** dim_date, dim_neighbourhood, dim_host, dim_listing  
**Facts:** fact_calendar, fact_reviews, fact_listing_performance

### 5.4 Engineering Decision Log (required by assignment)

Summarize from `docs/decision_log.md` — at minimum:

- DuckDB vs PostgreSQL/SQLite
- Edinburgh single-city scope
- Parquet over CSV
- Dash over Streamlit
- TextBlob + NMF for NLP
- neighbourhood_cleansed for analytics

Format each as: **Options → Decision → Reason → Trade-off**

### 5.5 Production considerations (brief)

- What would change for 50 cities: orchestration (Airflow), partitioned calendar, cloud warehouse
- Current: local batch, suitable for assignment reproducibility

---

## Section 6 — EDA Findings (3–4 pages)

**Maps to Assignment Section 04**

### Required: business interpretation for EVERY figure

| Figure | File | Finding | Business meaning |
|--------|------|---------|------------------|
| Fig 6.1 | `01_median_price_by_neighbourhood.png` | Price varies by area | Location-based pricing strategy |
| Fig 6.2 | `02_price_by_room_type.png` | Entire homes premium | Product mix affects revenue |
| Fig 6.3 | `03_host_portfolio_distribution.png` | Few multi-listing hosts | Market not dominated by mega-hosts |
| Fig 6.4 | `04_review_score_distribution.png` | Scores clustered high | Rating inflation; small differentiation |
| Fig 6.5 | `05_occupancy_proxy_by_room_type.png` | Occupancy differs by type | Capacity planning varies |
| Fig 6.6 | `06_price_vs_review_score.png` | Weak price-rating link | Quality doesn't always command premium |
| Fig 6.7 | `07_listing_density_by_neighbourhood.png` | Supply concentrated | Competition hotspots |

### Address assignment EDA subsections

| Subsection | Covered? | Notes |
|------------|----------|-------|
| 4.1 Summary stats & distributions | ✅ | All 7 charts |
| 4.2 Geographic/spatial | ⚠️ Partial | Bar charts, not interactive map — explain |
| 4.3 Temporal/seasonal | ⚠️ Limited | H5 uses calendar; no full seasonal price chart |
| 4.4 Host/supply-side | ✅ | Host portfolio chart |
| 4.5 Review/demand-side | ✅ | Price vs review, occupancy proxy |

**Honest note:** Temporal deep-dive and interactive maps deferred; neighbourhood analysis covers spatial pricing gradients.

---

## Section 7 — Statistical Findings (2–3 pages)

**Maps to Assignment Section 05**

### 7.1 Hypothesis results table (include full table)

| ID | Result | Test | Effect size | Business interpretation |
|----|--------|------|-------------|-------------------------|
| H1 | ✅ Significant | Welch t-test | d = 0.60 | Entire homes ~£337 vs private ~£157 |
| H2 | ❌ Not significant | Welch t-test | N/A | Superhost data too sparse in snapshot |
| H3 | ✅ Significant | Welch t-test | d = -0.12 | High-review listings slightly cheaper |
| H4 | ✅ Significant | ANOVA | η² = 0.04 | Neighbourhood prices differ |
| H5 | ✅ Significant | Welch t-test | d = -0.004 | Weekend min nights slightly lower |

### 7.2 H5 methodology note (important)

Assignment asks weekend vs weekday **pricing**. Edinburgh calendar in this snapshot lacks reliable daily price for H5. You adapted to **weekend vs weekday minimum nights** — document this clearly as a data limitation workaround.

### 7.3 Statistical methodology (assignment requires)

For each test document:

- **Why this test** (e.g., Welch for unequal variances)
- **Assumptions** (normality, independence — note large n)
- **Violations handled** (Welch instead of Student's t)
- **Practical vs statistical significance** (H3 significant but small effect)
- **Non-technical interpretation** paragraph

### 7.4 Section 5.2–5.3 (partial coverage — be honest)

| Requirement | Status |
|-------------|--------|
| Confidence intervals | ⚠️ Add 1 paragraph if time; or note as future work |
| Correlation matrix | ⚠️ Refer to EDA price vs rating; ML feature importance |
| OLS regression | ⚠️ Ridge regression in ML section covers this |
| VIF / multicollinearity | ❌ Not done — note in limitations |
| Multi-city comparisons | N/A |

---

## Section 8 — Data Science Experiments (2–3 pages)

**Maps to Assignment Section 06**

### 8.1 Price prediction (6.1) — fully covered

| Requirement | Your work |
|-------------|-----------|
| Problem framing | Predict nightly price (GBP) |
| Feature engineering | 14 features from enriched listings |
| 3 model families | Ridge, Random Forest, Gradient Boosting |
| Cross-validation | 5-fold CV MAE |
| Metrics | MAE, RMSE, R² |
| Residual analysis | `08_price_model_residuals.png` |
| Explainability | RF feature importance (not SHAP — note trade-off) |

### 8.2 Model comparison table (include)

| Model | CV MAE | Test MAE | Test RMSE | Test R² |
|-------|--------|----------|-----------|---------|
| Gradient Boosting | 93.23 | 93.84 | 330.99 | 0.085 |
| Ridge Regression | 94.31 | 94.04 | 320.05 | 0.144 |
| Random Forest | 94.83 | 96.82 | 332.54 | 0.076 |

### 8.3 Top price drivers

From `price_model_feature_importance.csv`:

1. number_of_reviews
2. bedrooms
3. accommodates
4. neighbourhood_avg_rating
5. neighbourhood_median_price

### 8.4 ML documentation standard (assignment 6.x box)

- Problem framing ✅
- Feature engineering rationale ✅
- Model selection rationale ✅
- Validation strategy ✅
- Failure modes: low R², premium listing errors ✅
- Improvements: more features, SHAP, segment models ✅

### 8.5 Not done (state briefly)

- 6.2 Demand forecasting
- 6.3 Clustering segmentation
- 6.4 Cross-neighbourhood bias testing (mention as future work)

---

## Section 9 — AI/ML Experiments (2–3 pages)

**Maps to Assignment Section 07**

### 9.1 NLP on reviews (7.1) — covered

| Requirement | Status |
|-------------|--------|
| Sentiment analysis | ✅ TextBlob polarity/subjectivity |
| Correlate with ratings | ✅ Listing-level aggregation |
| Topic modelling | ✅ TF-IDF + NMF, 8 topics |
| NER | ❌ Deferred |
| Review quality classifier | ❌ Deferred |
| Language patterns | ⚠️ French topic cluster identified |

### 9.2 NLP findings

- Topics: city centre access, host communication, cleanliness, value, recommendations
- Sentiment predominantly positive
- Weak correlation between text sentiment and star ratings
- Sampling: 20k sentiment, 10k topics (justify reproducibility)

### 9.3 Not done (7.2–7.4)

- LLM summaries, RAG, Q&A interface — deferred
- Recommendation systems — deferred
- Generative AI pricing advisor — deferred
- **Write:** "Well-documented scope boundary; NLP depth chosen over LLM experimentation"

---

## Section 10 — Visualizations (1–2 pages)

**Dedicated figure gallery with numbered captions**

### Static figures (from notebooks)

- Figures 6.1–6.7 (EDA)
- Figures 8.1–8.2 (ML)
- Figures 9.1–9.3 (NLP)

### Dashboard screenshots (from your captures)

- Fig 10.1: Overview + KPIs
- Fig 10.2: Market Explorer (unfiltered)
- Fig 10.3: Market Explorer (filtered)
- Fig 10.4: Reviews & NLP tab
- Fig 10.5: ML Insights tab
- Fig 10.6: Statistical Tests tab

**Caption format:** "Figure 10.X: [Title]. [One-sentence interpretation]."

---

## Section 11 — Business Recommendations (1–2 pages)

### For hosts

1. **Price by product type:** Entire homes can command ~2× private room rates (H1).
2. **Location matters:** Use neighbourhood median price benchmarks (EDA, ML).
3. **Invest in communication:** NLP shows host responsiveness as recurring theme.
4. **Maintain cleanliness:** Top review topic cluster across listings.

### For revenue managers / consultancy

1. Use **occupancy proxy** for revenue estimation — label as estimate, not bookings.
2. Deploy **Dash dashboard** for neighbourhood and room-type filtering.
3. Combine **structured ratings + text sentiment** for quality monitoring.
4. Segment pricing models by property type — ML residuals show segment errors.

### For platform/policy analysts

1. High review scores with limited variance may indicate rating inflation.
2. Small FK gaps (0.22%) should be monitored in production pipelines.
3. Multilingual reviews require language-aware NLP in production.

---

## Section 12 — Cross-City Comparisons (0.5 page)

**Not applicable — but MUST include per assignment structure**

Single-city Edinburgh study by design. Multi-city would require:

- Schema harmonization across cities
- Unified cross-city master dataset
- ANOVA with multiple comparison correction

Deferred to prioritize pipeline depth and analytical quality per assignment guidance.

---

## Section 13 — Limitations & Caveats (1–2 pages)

### Data limitations

- Snapshot only (2026-06-23) — not longitudinal
- No true booking counts or revenue
- Calendar occupancy is proxy, not confirmed bookings
- `neighbourhood` empty; cleansed names used
- H5 adapted to minimum nights (no daily calendar price)
- H2 inconclusive (superhost field sparse)
- Inside Airbnb scraping artifacts

### Method limitations

- ML low R² (~0.08) — price driven by unobserved factors
- NLP on samples, not full 676k corpus
- TextBlob less accurate than transformers
- No SHAP/LIME — RF importance only
- No geospatial interactive maps

### Scope limitations

- Local pipeline, not cloud production
- No Docker/incremental CDC
- No LLM/RAG experiments

---

## Section 14 — Future Improvements (1 page)

1. Multi-city pipeline with config-driven harmonization
2. Incremental ingestion + Airflow orchestration
3. Great Expectations data quality framework
4. SHAP explainability for ML
5. BERTopic / transformer NLP with language detection
6. Interactive Folium/GeoPandas neighbourhood map
7. Docker-compose for full reproducibility
8. Cloud deployment (Dash on Render/Heroku)
9. Demand forecasting from calendar time series
10. Automated weekly PDF report generation

---

## Section 15 — Reflection (1 page)

### What went well

- Depth-first Edinburgh strategy matched assignment philosophy
- End-to-end pipeline → warehouse → notebooks → dashboard tells coherent story
- Documenting decisions and incomplete work builds interviewer trust

### Trade-offs made

- Chose 4 deep sections over 8 shallow ones
- Dash dashboard over cloud deployment
- TextBlob over BERT for interpretability

### Lessons learned

- Always validate column usability (`neighbourhood` vs `neighbourhood_cleansed`)
- Flag-and-retain validation beats silent deletion
- Business interpretation matters as much as code

### What I would do differently

- Add temporal EDA earlier
- Run SHAP on ML model
- Save dashboard screenshots during development

---

## Appendix A — AI Usage Disclosure (2–3 pages)

Copy and expand from `docs/ai_usage_disclosure.md`. Must include per Assignment Section 10:

| Disclosure item | Include |
|-----------------|---------|
| AI tools used | ChatGPT, Cursor AI |
| AI-assisted sections | List by section (02–08) |
| Key prompts | 3–5 example prompts in appendix |
| Output validation | Local execution, pytest, manual review |
| Modifications made | neighbourhood fix, scope decisions |
| Critical assessment | Rejected multi-city shallow approach |

---

## Mandatory deliverables checklist (Assignment Section 11)

| Deliverable | Location | In PDF? |
|-------------|----------|---------|
| Source code | GitHub repo | Reference + structure diagram |
| Reproducibility instructions | README.md | Section 4.3 |
| Professional PDF report | This document | The deliverable itself |
| Assumptions log | docs/assumptions.md | Section 3.5 |
| Decisions log | docs/decision_log.md | Section 5.4 |
| Completed work summary | docs/completed_work.md | Sections 2, 15 |
| Incomplete work summary | docs/incomplete_work.md | Sections 13, 14 |
| AI usage disclosure | Appendix A | Appendix A |

### Optional deliverables you HAVE (highlight these)

- ✅ Jupyter notebooks (5)
- ✅ Interactive dashboard (Dash)
- ✅ Architecture diagram content (docs/architecture.md)
- ✅ Unit tests (12 passing)

---

## Formatting requirements (Assignment Section 12)

- [ ] PDF format
- [ ] Minimum 20 pages
- [ ] Professional typography (Arial/Calibri 11pt body, 14pt headings)
- [ ] Numbered sections matching this outline
- [ ] Page numbers
- [ ] Table of contents
- [ ] Numbered figures with captions
- [ ] Consistent heading styles

---

## Quick copy-paste figure list for TOC

```
List of Figures
Figure 6.1  Median Price by Neighbourhood
Figure 6.2  Price Distribution by Room Type
...
Figure 10.1 Dashboard Overview
Figure 10.2 Market Explorer (All Filters)
...
```

---

## Submission final checklist

- [ ] PDF saved to `reports/airbnb_market_intelligence_edinburgh.pdf`
- [ ] Screenshots in `reports/screenshots/`
- [ ] GitHub repo pushed with README
- [ ] All notebooks runnable
- [ ] `python -m src.pipeline` works
- [ ] `python dashboard/app.py` works
- [ ] `pytest` passes
