# Assumptions Log

This document records assumptions made during data ingestion, transformation,
analysis, and modelling.

## Assumption 001: Calendar Availability

**Assumption:** An unavailable calendar date may represent a booking, a host block,
or another restriction.

**Decision:** The project uses the term `calendar-based occupancy proxy` rather
than claiming unavailable dates are confirmed bookings.

**Impact:** Occupancy and revenue calculations must be interpreted as estimates.

## Assumption 002: Dataset Snapshot

**Assumption:** The selected dataset represents the Airbnb market at the published
snapshot date.

**Impact:** Findings may not represent historical conditions or future behaviour.

## Assumption 003: Primary Listing Source (A1)

**Assumption:** Detailed listings (`listings.csv.gz`) is the primary listing source
for downstream engineering.

**Impact:** Summary listings are used for comparison and validation only.

## Assumption 004: Occupancy Proxy (A3)

**Assumption:** Calendar unavailable days can be used as a practical occupancy
proxy at listing level.

**Impact:** H5 and dashboard occupancy metrics are calendar-based estimates.

## Assumption 005: Referential Integrity Handling (A4)

**Assumption:** Orphan child records are flagged rather than silently removed.

**Impact:** Small unmatched calendar/review rows remain visible in validation
reports.

## Assumption 006: Join Keys (A5)

**Assumption:** `listing_id` is the standard join key across calendar and review
files.

**Impact:** Enrichment and warehouse loads depend on consistent listing IDs.

## Assumption 007: Neighbourhood Names (A6)

**Assumption:** `neighbourhood_cleansed` is the usable neighbourhood field in the
Edinburgh snapshot because raw `neighbourhood` is empty.

**Impact:** EDA, enrichment, and dashboard neighbourhood charts use cleansed names.

## Assumption 008: Geographic Scope (A7)

**Assumption:** Findings apply only to Edinburgh at the 2026-06-23 snapshot date.

**Impact:** Results are not generalised to other cities or time periods.

## Assumption 009: ML Modelling Scope

**Assumption:** Price prediction models estimate nightly listing price from
observable listing attributes, not causal pricing effects.

**Impact:** Feature importance indicates association, not guaranteed revenue
uplift.

## Assumption 010: NLP Sampling

**Assumption:** Sentiment and topic modelling on sampled review subsets is
representative enough for assignment-level insight.

**Impact:** Full-corpus NLP was deferred for runtime and reproducibility.
