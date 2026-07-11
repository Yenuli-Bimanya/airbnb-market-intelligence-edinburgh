# Edinburgh Inside Airbnb Data Dictionary

## Dataset Overview

| Field | Value |
|---|---|
| City | Edinburgh |
| Region | Scotland |
| Country | United Kingdom |
| Snapshot date | 2026-06-23 |
| Source | [Inside Airbnb](https://insideairbnb.com/) |
| Official data dictionary | [Google Sheets](https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/) |

This document summarises the Edinburgh dataset used in the project. Detailed
exploration, sample records and validation checks are recorded in
`notebooks/01_dataset_familiarization.ipynb`.

---

## 1. File Inventory

| Dataset | File | Format | Rows | Columns | Size (MB) |
|---|---|---|---:|---:|---:|
| Detailed listings | `listings_detailed.csv` | CSV | 6,244 | 90 | 16.47 |
| Calendar | `calendar_detailed.csv` | CSV | 2,284,170 | 5 | 75.15 |
| Detailed reviews | `reviews_detailed.csv` | CSV | 676,263 | 6 | 198.04 |
| Summary listings | `listings.csv` | CSV | 6,258 | 19 | 1.14 |
| Summary reviews | `reviews.csv` | CSV | 676,263 | 2 | 14.42 |
| Neighbourhoods | `neighbourhoods.csv` | CSV | 111 | 2 | 0.00 |
| Neighbourhood boundaries | `neighbourhoods.geojson` | GeoJSON | 111 features | 3 | 0.31 |

### File locations

| Stage | Path |
|---|---|
| Raw data | `data/raw/edinburgh/2026-06-23/` |
| Extracted interim data | `data/interim/edinburgh/2026-06-23/` |
| Profiling outputs | `data/metadata/` |

---

## 2. Business Entities

| Entity | Source file(s) | Description |
|---|---|---|
| Listing | `listings_detailed.csv`, `listings.csv` | A property or room offered for short-term rental. Includes price, location, room type, availability and host attributes. |
| Host | `listings_detailed.csv` | The person or organisation managing one or more listings. |
| Review | `reviews_detailed.csv`, `reviews.csv` | Guest feedback linked to a listing. |
| Calendar day | `calendar_detailed.csv` | Daily availability, price and minimum-night information for a listing. |
| Neighbourhood | `neighbourhoods.csv`, `neighbourhoods.geojson` | Geographic subdivision of Edinburgh used for spatial analysis. |

---

## 3. Schema Summary by File

### 3.1 Detailed listings (`listings_detailed.csv`)

Primary key: `id`

| Column | Type | Notes |
|---|---|---|
| `id` | BIGINT | Listing identifier |
| `listing_url` | VARCHAR | Airbnb listing URL |
| `scrape_id` | BIGINT | Scrape batch identifier |
| `last_scraped` | DATE | Date the listing was scraped |
| `source` | VARCHAR | Data source label |
| `name` | VARCHAR | Listing title |
| `description` | VARCHAR | Full listing description |
| `neighborhood_overview` | VARCHAR | Neighbourhood description |
| `picture_url` | VARCHAR | Main listing image URL |
| `host_id` | BIGINT | Host identifier |
| `host_name` | VARCHAR | Host display name |
| `host_since` | VARCHAR | Host registration date |
| `host_is_superhost` | BOOLEAN | Superhost status |
| `host_response_rate` | VARCHAR | Host response rate |
| `host_acceptance_rate` | VARCHAR | Host acceptance rate |
| `neighbourhood` | VARCHAR | Neighbourhood label |
| `neighbourhood_cleansed` | VARCHAR | Standardised neighbourhood name |
| `latitude` | DOUBLE | Listing latitude |
| `longitude` | DOUBLE | Listing longitude |
| `property_type` | VARCHAR | Property category |
| `room_type` | VARCHAR | Entire home, private room, shared room, etc. |
| `accommodates` | BIGINT | Guest capacity |
| `bedrooms` | BIGINT | Bedroom count |
| `beds` | BIGINT | Bed count |
| `bathrooms` | DOUBLE | Bathroom count |
| `amenities` | VARCHAR | Amenities list |
| `price` | VARCHAR | Nightly price stored as text |
| `minimum_nights` | BIGINT | Minimum stay requirement |
| `maximum_nights` | BIGINT | Maximum stay requirement |
| `availability_365` | BIGINT | Available days in next 365 days |
| `number_of_reviews` | BIGINT | Total review count |
| `reviews_per_month` | DOUBLE | Average monthly review count |
| `review_scores_rating` | DOUBLE | Overall review score |
| `review_scores_accuracy` | DOUBLE | Accuracy sub-score |
| `review_scores_cleanliness` | DOUBLE | Cleanliness sub-score |
| `review_scores_checkin` | DOUBLE | Check-in sub-score |
| `review_scores_communication` | DOUBLE | Communication sub-score |
| `review_scores_location` | DOUBLE | Location sub-score |
| `review_scores_value` | DOUBLE | Value sub-score |
| `estimated_occupancy_l365d` | BIGINT | Estimated occupancy over 365 days |
| `estimated_revenue_l365d` | BIGINT | Estimated annual revenue |
| `license` | VARCHAR | Short-term rental licence reference |
| `instant_bookable` | VARCHAR | Instant booking flag |

The full 90-column schema is available in `data/metadata/schema_report.csv`.

### 3.2 Calendar (`calendar_detailed.csv`)

Composite key: `listing_id`, `date`

| Column | Type | Notes |
|---|---|---|
| `listing_id` | BIGINT | Foreign key to listings |
| `date` | DATE | Calendar date |
| `available` | BOOLEAN | Availability flag |
| `minimum_nights` | BIGINT | Minimum nights for that date |
| `maximum_nights` | BIGINT | Maximum nights for that date |

### 3.3 Detailed reviews (`reviews_detailed.csv`)

Primary key: `id`

| Column | Type | Notes |
|---|---|---|
| `listing_id` | BIGINT | Foreign key to listings |
| `id` | BIGINT | Review identifier |
| `date` | DATE | Review date |
| `reviewer_id` | BIGINT | Reviewer identifier |
| `reviewer_name` | VARCHAR | Reviewer display name |
| `comments` | VARCHAR | Review text |

### 3.4 Summary listings (`listings.csv`)

Primary key: `id`

| Column | Type | Notes |
|---|---|---|
| `id` | BIGINT | Listing identifier |
| `name` | VARCHAR | Listing title |
| `host_id` | BIGINT | Host identifier |
| `host_name` | VARCHAR | Host display name |
| `neighbourhood_group` | VARCHAR | Neighbourhood group |
| `neighbourhood` | VARCHAR | Neighbourhood label |
| `latitude` | DOUBLE | Listing latitude |
| `longitude` | DOUBLE | Listing longitude |
| `room_type` | VARCHAR | Room category |
| `price` | BIGINT | Nightly price as numeric |
| `minimum_nights` | BIGINT | Minimum stay requirement |
| `number_of_reviews` | BIGINT | Total review count |
| `last_review` | DATE | Most recent review date |
| `reviews_per_month` | DOUBLE | Average monthly review count |
| `availability_365` | BIGINT | Available days in next 365 days |
| `license` | VARCHAR | Licence reference |

### 3.5 Summary reviews (`reviews.csv`)

Candidate key: `listing_id`, `date` (not unique)

| Column | Type | Notes |
|---|---|---|
| `listing_id` | BIGINT | Foreign key to listings |
| `date` | DATE | Review date |

### 3.6 Neighbourhoods (`neighbourhoods.csv`)

| Column | Type | Notes |
|---|---|---|
| `neighbourhood_group` | VARCHAR | Neighbourhood group, often empty in Edinburgh |
| `neighbourhood` | VARCHAR | Neighbourhood name |

### 3.7 Neighbourhood boundaries (`neighbourhoods.geojson`)

| Field | Type | Notes |
|---|---|---|
| `neighbourhood` | string | Neighbourhood name |
| `neighbourhood_group` | null/string | Often empty |
| `geometry` | MultiPolygon | Neighbourhood boundary geometry |

---

## 4. Primary and Foreign Key Map

| Dataset | Key type | Key column(s) | Validation result |
|---|---|---|---|
| Detailed listings | Primary key | `id` | Valid: no nulls, no duplicates |
| Summary listings | Primary key | `id` | Valid: no nulls, no duplicates |
| Calendar | Composite key | `listing_id`, `date` | Valid: no nulls, no duplicate groups |
| Detailed reviews | Primary key | `id` | Valid: no nulls, no duplicates |
| Summary reviews | Candidate key | `listing_id`, `date` | Not unique: 2,486 duplicate groups |

### Relationships

| Parent | Child | Join condition | Cardinality |
|---|---|---|---|
| Detailed listings | Calendar | `listings.id = calendar.listing_id` | One-to-many |
| Detailed listings | Detailed reviews | `listings.id = reviews_detailed.listing_id` | One-to-many |
| Summary listings | Summary reviews | `listings.id = reviews.listing_id` | One-to-many |
| Neighbourhoods | Listings | `neighbourhoods.neighbourhood = listings.neighbourhood` | One-to-many |

### Referential integrity findings

| Relationship | Unmatched child rows | Percentage |
|---|---|---:|
| Calendar → detailed listings | 5,110 | 0.22% |
| Calendar → summary listings | 0 | 0.00% |
| Detailed reviews → detailed listings | 642 | 0.09% |
| Detailed reviews → summary listings | 0 | 0.00% |

---

## 5. Key Numerical Ranges

Ranges below were computed from the Edinburgh snapshot during dataset
familiarization.

| Field | Dataset | Minimum | Maximum |
|---|---|---:|---:|
| Latitude | Detailed listings | 55.86 | 55.99 |
| Longitude | Detailed listings | -3.44 | -3.10 |
| Price | Detailed listings | Cleaned from text | Cleaned from text |
| Price | Summary listings | 5 | 12,042 |
| Availability (365 days) | Detailed listings | 0 | 365 |
| Review count | Detailed listings | 0 | 1,773 |
| Minimum nights | Detailed listings | 1 | 1,125 |

---

## 6. Columns Requiring Special Interpretation

| Column | Dataset | Reason |
|---|---|---|
| `price` | Detailed listings | Stored as text; requires cleaning before analysis |
| `price` | Summary listings | Numeric but may differ from detailed listing prices |
| `available` | Calendar | `f` = unavailable, `t` = available; unavailable does not always mean booked |
| `availability_365` | Listings | Available days, not confirmed occupancy |
| `reviews_per_month` | Listings | Derived metric; may be missing for inactive listings |
| `estimated_occupancy_l365d` | Listings | Inside Airbnb estimate, not confirmed bookings |
| `estimated_revenue_l365d` | Listings | Estimate based on calendar and price signals |
| `license` | Listings | Sparse regulatory field |
| `neighbourhood_group` | Listings / neighbourhoods | Often empty in Edinburgh |
| `date` | Summary reviews | Not a strict unique key because duplicate groups exist |

---

## 7. Dataset Limitations

1. The dataset represents a single scrape date and is not a full historical time series.
2. Scraping artifacts may cause missing values and file-level mismatches.
3. Summary listings contain 6,258 rows while detailed listings contain 6,244 rows.
4. Fourteen listings appear only in the summary listings file.
5. Calendar and review records contain orphan listing IDs when joined to detailed listings.
6. Calendar unavailable days may represent bookings, host blocks or other restrictions.
7. Summary reviews contain duplicate `listing_id` + `date` combinations.
8. The dataset does not include true booking counts or guest identities.

---

## 8. Project Assumptions

| ID | Assumption |
|---|---|
| A1 | Detailed listings is the primary listing source for downstream engineering |
| A2 | Summary listings are used for validation and comparison only |
| A3 | Calendar unavailable days are treated as a calendar-based occupancy proxy |
| A4 | Orphan child records are flagged rather than silently removed |
| A5 | `listing_id` is the standard join key across calendar and review files |
| A6 | Neighbourhood names are matched to `neighbourhoods.csv` and GeoJSON boundaries |
| A7 | Findings apply only to Edinburgh at the 2026-06-23 snapshot date |

---

## 9. Source File Selection for Pipeline

| Pipeline use case | Preferred file |
|---|---|
| Rich listing attributes | `listings_detailed.csv` |
| Quick listing checks | `listings.csv` |
| Daily availability and pricing | `calendar_detailed.csv` |
| Review text analysis | `reviews_detailed.csv` |
| Review volume trends | `reviews.csv` |
| Spatial segmentation | `neighbourhoods.csv`, `neighbourhoods.geojson` |

---

## 10. Related Project Artifacts

| Artifact | Location |
|---|---|
| Dataset familiarization notebook | `notebooks/01_dataset_familiarization.ipynb` |
| Profiling script | `src/profile_datasets.py` |
| Dataset inventory report | `data/metadata/dataset_inventory.csv` |
| Full schema report | `data/metadata/schema_report.csv` |
| Assumptions log | `docs/assumptions.md` |
| Engineering decision log | `docs/decision_log.md` |
