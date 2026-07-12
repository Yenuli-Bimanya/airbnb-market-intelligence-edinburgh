# Engineering Decision Log

## Decision 001: Python Version

**Decision:** Use Python 3.13.14.

**Reason:** Modern Python environment with support for planned data engineering and
analytical libraries.

**Trade-off:** Newer Python versions may expose occasional package compatibility
issues.

---

## Decision 002: Analytical Database

**Decision:** Use DuckDB.

**Options Considered:** SQLite, PostgreSQL, DuckDB

**Reason:** DuckDB supports analytical SQL and Parquet processing without a
separate database server.

**Trade-off:** Suitable for local analytics, not a distributed production warehouse.

---

## Decision 003: Project Scope

**Decision:** Begin with one city and prioritize depth, reproducibility, and data
quality.

**Reason:** Assignment prioritizes thoughtful scoping over shallow multi-section
coverage.

**Trade-off:** Findings may not generalize to other Airbnb markets.

---

## Decision 004: Processed Data Format

**Decision:** Use Parquet for cleaned, validated, and enriched datasets.

**Reason:** Faster reads, smaller storage footprint, and consistent typing for
pandas/DuckDB.

**Trade-off:** Less human-readable than CSV for manual inspection.

---

## Decision 005: Dashboard Framework

**Decision:** Use Plotly Dash instead of Streamlit.

**Reason:** Better fit for multi-tab analytical dashboards, interactive Plotly
charts, and callback-based filtering.

**Trade-off:** More layout/callback code than Streamlit for equivalent functionality.

---

## Decision 006: NLP Approach

**Decision:** Use TextBlob for sentiment and TF-IDF + NMF for topic modelling on
sampled review subsets.

**Reason:** Interpretable, fast, and sufficient for assignment depth without
GPU/transformer infrastructure.

**Trade-off:** Less accurate than transformer models on sarcasm and multilingual
text.

---

## Decision 007: Neighbourhood Field for Analytics

**Decision:** Use `neighbourhood_cleansed` for neighbourhood charts and
aggregations.

**Reason:** Raw `neighbourhood` is empty in the Edinburgh snapshot.

**Trade-off:** Documentation must explain the difference to avoid confusion in
dashboard/report interpretation.

---

## Decision 008: Validation Strategy

**Decision:** Flag invalid records and retain audit rows in validation reports
rather than silently dropping all anomalies.

**Reason:** Preserves transparency for assignment review and debugging.

**Trade-off:** Downstream notebooks must filter on flags such as `is_valid_price`.
