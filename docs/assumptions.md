# Assumptions Log

This document records assumptions made during data ingestion, transformation, analysis and modelling.

## Assumption 001: Calendar Availability

**Assumption:** An unavailable calendar date may represent a booking, a host block or another restriction.

**Decision:** The project will use the term `calendar-based occupancy proxy` rather than claiming that unavailable dates represent confirmed bookings.

**Impact:** Occupancy and revenue calculations must be interpreted as estimates, not actual Airbnb transactions.

## Assumption 002: Dataset Snapshot

**Assumption:** The selected dataset represents the Airbnb market at the published snapshot date.

**Impact:** Findings may not represent historical conditions or future market behaviour.
