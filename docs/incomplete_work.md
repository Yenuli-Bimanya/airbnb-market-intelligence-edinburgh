# Incomplete Work Summary

This document records work that was **not completed** in the Edinburgh Airbnb
Market Intelligence project, with reasons and recommended next steps. It is
provided to meet the assignment requirement for honest scope reporting.

---

## Section 08: Interactive Dashboard

**Status:** Not started

| Item | Reason skipped / deferred | Recommended next step |
|------|---------------------------|----------------------|
| Streamlit dashboard (`dashboard/app.py`) | Prioritised pipeline depth and analytical notebooks first | Build a 4–5 page Streamlit app using DuckDB and `reports/` outputs |
| Dashboard deployment | Local-only scope for this assignment | Deploy to Streamlit Community Cloud if demo hosting is required |

---

## Final Deliverables

**Status:** Partially complete

| Item | Reason skipped / deferred | Recommended next step |
|------|---------------------------|----------------------|
| PDF assignment report (20+ pages) | Analysis notebooks completed first; report writing deferred | Compile EDA, stats, ML, and NLP outputs into `reports/` PDF |
| Architecture diagram document | Not yet authored | Add pipeline + warehouse diagram to `docs/architecture.md` |
| Data lineage document | Not yet authored | Document source-to-dashboard flow in `docs/data_lineage.md` |
| Dashboard screenshots for report | Dashboard not built yet | Capture after Streamlit app is complete |

---

## Advanced / Out-of-Scope Enhancements

These items were intentionally excluded to preserve depth on the Edinburgh
single-city workflow.

| Item | Reason not implemented |
|------|------------------------|
| Multi-city comparison (e.g. Edinburgh vs Glasgow) | Assignment strategy was depth-first on one city |
| Real-time or scheduled ingestion (Airflow, cron, cloud functions) | Snapshot-based batch pipeline was sufficient for scope |
| Production-grade orchestration (Docker, CI/CD deployment) | Local reproducible pipeline was the target |
| Transformer-based NLP (BERT, sentiment transformers) | TextBlob + TF-IDF/NMF chosen for interpretability and speed |
| Full-corpus NLP on all 676k reviews | Sampled subsets used for notebook performance and reproducibility |
| Language-specific NLP pipelines | Only basic multilingual topic noise identified; no language detection added |
| SHAP or advanced model explainability | Random Forest feature importance used instead |
| XGBoost / neural price models | sklearn Ridge, Random Forest, and Gradient Boosting were sufficient |
| Geospatial interactive maps in dashboard | EDA includes neighbourhood charts but not interactive map layer |
| RAG / LLM Q&A over reviews | Out of scope for this assignment phase |

---

## Testing and Engineering Gaps

| Item | Current state | Why incomplete |
|------|---------------|----------------|
| End-to-end pipeline integration test | Partial unit tests only | Time prioritised on pipeline + analysis deliverables |
| Dashboard tests | None | Dashboard not yet implemented |
| Notebook regression tests | None | Manual notebook execution used |
| Data quality monitoring in production | None | Local analytical project, not production deployment |

---

## Documentation Gaps

| Item | Current state |
|------|---------------|
| `docs/completed_work.md` | Updated through Section 07 |
| `docs/incomplete_work.md` | This document |
| `README.md` | Updated to reflect current project status |
| `docs/architecture.md` | Not created |
| `docs/data_lineage.md` | Not created |

---

## Summary

The project delivers strong coverage of Sections 02–07 with a reproducible
pipeline, dimensional warehouse, and four analysis notebooks (EDA, statistics,
ML, NLP). The main remaining deliverables are the **Streamlit dashboard** and
the **final PDF report**. Advanced production and multi-city features were
deliberately deferred to maintain quality and depth on the Edinburgh use case.
