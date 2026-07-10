# Engineering Decision Log

## Decision 001: Python Version

**Decision:** Use Python 3.13.14.

**Reason:** It provides a modern Python environment with support for the planned data engineering and analytical libraries.

**Trade-off:** Newer Python versions may occasionally expose package compatibility issues, which will be tested during environment setup.

---

## Decision 002: Analytical Database

**Decision:** Use DuckDB.

**Options Considered:**

- SQLite
- PostgreSQL
- DuckDB

**Reason:** DuckDB supports analytical SQL, CSV and Parquet processing without requiring a separate database server.

**Trade-off:** DuckDB is appropriate for local analytical workloads but is not a distributed production data warehouse.

---

## Decision 003: Project Scope

**Decision:** Begin with one city and prioritize depth, reproducibility and data quality.

**Reason:** The assignment prioritizes quality and thoughtful scoping over attempting every optional task.

**Trade-off:** The findings may not generalize to other Airbnb markets.
