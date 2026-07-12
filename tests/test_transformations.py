import pandas as pd

from src.transformations import (
    add_derived_listing_fields,
    build_calendar_features,
    build_neighbourhood_features,
    build_review_features,
)


def test_build_calendar_features_calculates_occupancy_proxy():
    calendar = pd.DataFrame(
        {
            "listing_id": [10, 10, 10, 10],
            "date": pd.date_range("2026-01-01", periods=4),
            "available": [True, False, False, True],
            "minimum_nights": [2, 2, 3, 1],
        }
    )

    features = build_calendar_features(calendar)

    assert len(features) == 1
    assert features.loc[0, "calendar_days"] == 4
    assert features.loc[0, "unavailable_days"] == 2
    assert features.loc[0, "occupancy_proxy"] == 0.5


def test_build_review_features_aggregates_by_listing():
    reviews = pd.DataFrame(
        {
            "id": [1, 2],
            "listing_id": [10, 10],
            "date": pd.to_datetime(["2025-01-01", "2025-06-01"]),
        }
    )

    features = build_review_features(reviews)

    assert len(features) == 1
    assert features.loc[0, "review_count_detailed"] == 2


def test_build_neighbourhood_features_uses_cleansed_names():
    listings = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "neighbourhood_cleansed": ["Old Town", "Old Town", "Leith"],
            "price": [200.0, 300.0, 150.0],
            "review_scores_rating": [4.8, 4.9, 4.5],
        }
    )

    features = build_neighbourhood_features(listings)

    assert set(features["neighbourhood_key"]) == {"Old Town", "Leith"}
    assert features.loc[features["neighbourhood_key"] == "Old Town", "neighbourhood_listing_count"].iloc[0] == 2


def test_add_derived_listing_fields_calculates_price_per_bedroom():
    listings = pd.DataFrame(
        {
            "price": [200.0],
            "bedrooms": [2],
            "hosts_time_as_host_years": [4],
            "number_of_reviews": [20],
        }
    )

    enriched = add_derived_listing_fields(listings)

    assert enriched.loc[0, "price_per_bedroom"] == 100.0
    assert enriched.loc[0, "review_frequency_per_year"] == 5.0
