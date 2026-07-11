# Completed Work Summary

This document records the work completed so far for the Expernetic Data
Engineering Intern assignment. The project focuses on Edinburgh using a single-
city, depth-first approach.

---

## Section 02: Dataset Familiarization (Mandatory)

**Status:** Complete


| Task                                                   | Status | Evidence                                                  |
| ------------------------------------------------------ | ------ | --------------------------------------------------------- |
| Download Edinburgh Inside Airbnb snapshot (2026-06-23) | Done   | `data/raw/edinburgh/2026-06-23/`                          |
| Extract gzip source files                              | Done   | `src/extract_files.py`                                    |
| Document file inventory (rows, columns, sizes)         | Done   | `data/metadata/dataset_inventory.csv`, notebook Section 1 |
| Document schemas for all 7 datasets                    | Done   | `data/metadata/schema_report.csv`, notebook Section 1     |
| Inspect representative sample records                  | Done   | `notebooks/01_dataset_familiarization.ipynb` Section 2    |
| Inspect GeoJSON neighbourhood boundaries               | Done   | Notebook geojson summary cell                             |
| Compare detailed vs summary listings coverage          | Done   | Notebook Section 3 (14 summary-only listings found)       |
| Validate primary and composite keys                    | Done   | Notebook key validation cells                             |
| Validate foreign-key relationships                     | Done   | Notebook relationship report                              |
| Document numerical ranges for key fields               | Done   | Notebook Section 5                                        |
| Document business domain context                       | Done   | Notebook Section 6                                        |
| Document columns requiring special interpretation      | Done   | Notebook Section 7, `docs/data_dictionary.md`             |
| Document dataset limitations                           | Done   | Notebook Section 8, `docs/data_dictionary.md`             |
| Document project assumptions                           | Done   | Notebook Section 9, `docs/assumptions.md`                 |
| Produce standalone data dictionary                     | Done   | `docs/data_dictionary.md`                                 |




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



## Project Setup and Documentation

**Status:** Complete


| Task                                            | Status | Evidence                                                 |
| ----------------------------------------------- | ------ | -------------------------------------------------------- |
| Initialise repository structure                 | Done   | `src/`, `data/`, `sql/`, `docs/`, `dashboard/`, `tests/` |
| Configure project settings                      | Done   | `config/config.yaml`                                     |
| Add `.gitignore` for data and environment files | Done   | `.gitignore`                                             |
| Record engineering decisions                    | Done   | `docs/decision_log.md`                                   |
| Record initial assumptions                      | Done   | `docs/assumptions.md`                                    |
| Record AI usage disclosure (initial)            | Done   | `docs/ai_usage_disclosure.md`                            |
| Create project README                           | Done   | `README.md`                                              |


---



## Profiling and Metadata Generation

**Status:** Complete


| Task                                    | Status | Evidence                                     |
| --------------------------------------- | ------ | -------------------------------------------- |
| Build dataset profiling script          | Done   | `src/profile_datasets.py`                    |
| Generate dataset inventory report       | Done   | `data/metadata/dataset_inventory.csv`        |
| Generate schema report                  | Done   | `data/metadata/schema_report.csv`            |
| Create dataset familiarization notebook | Done   | `notebooks/01_dataset_familiarization.ipynb` |


---



## Git History


| Commit    | Description                                                           |
| --------- | --------------------------------------------------------------------- |
| `e36ab5a` | Initial commit                                                        |
| `ebd014c` | Edinburgh dataset setup and extraction workflow                       |
| `f2ad304` | Dataset profiling and schema samples                                  |
| `8ca7375` | Primary key and listing coverage validation                           |
| `401e6d3` | Complete familiarization notebook with domain context and assumptions |


---



## Standard Achieved

The completed work meets the mandatory Section 02 requirements to a high
standard. Findings are supported by executable notebook code, reproducible
metadata outputs and written documentation suitable for inclusion in the final
assignment report.

### Next planned stage

Section 03: Data Engineering — cleaning, validation, enrichment, DuckDB
dimensional modelling and pipeline automation.