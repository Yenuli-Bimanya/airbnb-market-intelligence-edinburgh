# Incomplete Work Summary

This document records work that was **not completed** in the Edinburgh Airbnb
Market Intelligence project, with reasons and recommended next steps.

---

## Final Deliverables

**Status:** One major item remains

| Item | Status | What to do |
|------|--------|------------|
| PDF assignment report (20+ pages) | **Not started** | Compile findings into `reports/airbnb_market_intelligence_edinburgh.pdf` |
| Dashboard screenshots | **Not started** | Save 5 tab screenshots to `reports/screenshots/` for the report |

Everything else required for a strong submission is implemented in code,
notebooks, dashboard, and documentation.

---

## PDF Report Checklist (for after your break)

Use these sources:

| Report section | Source |
|----------------|--------|
| Executive summary | `docs/completed_work.md`, key notebook findings |
| Data sources & limitations | `docs/data_dictionary.md`, notebook 01 |
| Pipeline architecture | `docs/architecture.md`, `docs/data_lineage.md` |
| EDA findings | notebook 02 + `reports/figures/01`–`07_*.png` |
| Statistical analysis | notebook 03 + `reports/tables/hypothesis_test_summary.csv` |
| ML results | notebook 04 + figures `08`–`09` |
| NLP results | notebook 05 + figures `10`–`12` |
| Dashboard walkthrough | screenshots from `reports/screenshots/` |
| Incomplete work / future scope | this file |
| AI disclosure | `docs/ai_usage_disclosure.md` |

Suggested screenshot set:

1. Dashboard overview with KPI cards
2. Market Explorer with neighbourhood filter applied
3. Reviews & NLP tab
4. ML Insights tab
5. Statistical Tests tab

---

## Section 08: Interactive Dashboard

**Status:** Complete

| Item | Status |
|------|--------|
| Dash dashboard (`dashboard/app.py`) | Done |
| Custom styling (`dashboard/assets/custom.css`) | Done |
| Dashboard screenshots for report | Pending |

---

## Optional Enhancements (deliberately deferred)

| Item | Reason not implemented |
|------|------------------------|
| Multi-city comparison | Depth-first Edinburgh scope |
| Real-time / scheduled ingestion | Snapshot batch pipeline was sufficient |
| Production deployment (Docker, CI/CD) | Local reproducible project was the target |
| Transformer NLP (BERT, etc.) | TextBlob + TF-IDF/NMF chosen for speed and clarity |
| Full-corpus NLP on all 676k reviews | Sampled subsets used for runtime |
| SHAP / advanced ML explainability | Random Forest feature importance used |
| Geospatial interactive map layer | Neighbourhood charts used instead |
| Dashboard cloud deployment | Local demo sufficient for assignment |

---

## Testing Gaps

| Item | Current state |
|------|---------------|
| Unit tests for cleaning / validation / transformations | Implemented in `tests/` |
| End-to-end pipeline integration test | Not implemented |
| Dashboard automated tests | Not implemented |
| Notebook regression tests | Not implemented |

---

## Documentation Status

| Item | Current state |
|------|---------------|
| `docs/completed_work.md` | Updated through Section 08 |
| `docs/incomplete_work.md` | This document |
| `docs/architecture.md` | Completed |
| `docs/data_lineage.md` | Completed |
| `docs/assumptions.md` | Expanded |
| `docs/decision_log.md` | Expanded |
| `docs/ai_usage_disclosure.md` | Expanded through Section 08 |

---

## Summary

The project is submission-ready except for the **final PDF report** and
**dashboard screenshots**. No further code changes are required before those
two tasks.
