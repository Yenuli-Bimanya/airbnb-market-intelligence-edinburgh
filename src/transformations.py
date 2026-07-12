from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import load_config


def get_processed_dir(config) -> Path:
    """Return the processed data folder for the selected city snapshot."""

    return (
        config.paths.processed_data
        / config.city.name.lower()
        / config.city.snapshot_date
    )


def load_processed_dataset(processed_dir: Path, file_stem: str) -> pd.DataFrame:
    """Load a processed parquet dataset."""

    file_path = processed_dir / f"{file_stem}.parquet"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Processed file not found: {file_path}. Run earlier pipeline steps first."
        )

    return pd.read_parquet(file_path)

#Occupancy proxy and calendar stats per listing
def build_calendar_features(calendar: pd.DataFrame) -> pd.DataFrame:
    """Create listing-level calendar aggregates."""

    calendar_features = (
        calendar.groupby("listing_id", as_index=False)
        .agg(
            calendar_days=("date", "count"),
            unavailable_days=("available", lambda s: int((~s).sum())),
            avg_minimum_nights=("minimum_nights", "mean"),
        )
    )

    calendar_features["occupancy_proxy"] = (
        calendar_features["unavailable_days"] / calendar_features["calendar_days"]
    ).round(4)

    return calendar_features

#Review counts, dates, and scores per listing
def build_review_features(reviews: pd.DataFrame) -> pd.DataFrame:
    """Create listing-level review aggregates."""

    review_features = (
        reviews.groupby("listing_id", as_index=False)
        .agg(
            review_count_detailed=("id", "count"),
            latest_review_date=("date", "max"),
            first_review_date_detailed=("date", "min"),
        )
    )

    return review_features

#Median price, listing count, avg rating per neighbourhood
def build_neighbourhood_features(listings: pd.DataFrame) -> pd.DataFrame:
    """Create neighbourhood-level market aggregates."""

    neighbourhood_column = (
        "neighbourhood_cleansed"
        if "neighbourhood_cleansed" in listings.columns
        else "neighbourhood"
    )

    working = listings.copy()
    working[neighbourhood_column] = working[neighbourhood_column].astype("string")

    neighbourhood_features = (
        working.groupby(neighbourhood_column, as_index=False)
        .agg(
            neighbourhood_listing_count=("id", "count"),
            neighbourhood_median_price=("price", "median"),
            neighbourhood_avg_rating=("review_scores_rating", "mean"),
        )
    )

    neighbourhood_features = neighbourhood_features.rename(
        columns={neighbourhood_column: "neighbourhood_key"}
    )

    return neighbourhood_features

#Host tenure, price per bedroom, review frequency per year
def add_derived_listing_fields(listings: pd.DataFrame) -> pd.DataFrame:
    """Add calculated listing-level business fields."""

    enriched = listings.copy()

    if "hosts_time_as_host_years" in enriched.columns:
        enriched["host_tenure_years"] = pd.to_numeric(
            enriched["hosts_time_as_host_years"],
            errors="coerce",
        )
    else:
        enriched["host_tenure_years"] = pd.NA

    enriched["price_per_bedroom"] = enriched["price"] / enriched["bedrooms"].replace(
        {0: pd.NA}
    )

    if "number_of_reviews" in enriched.columns and "host_tenure_years" in enriched.columns:
        review_frequency = (
            enriched["number_of_reviews"]
            / enriched["host_tenure_years"].replace({0: pd.NA})
        )
        enriched["review_frequency_per_year"] = pd.to_numeric(
            review_frequency,
            errors="coerce",
        ).round(4)

    return enriched

#Join all feature tables onto the listings master table
def enrich_listings(
    listings: pd.DataFrame,
    calendar_features: pd.DataFrame,
    review_features: pd.DataFrame,
    neighbourhood_features: pd.DataFrame,
) -> pd.DataFrame:
    """Join all feature tables onto the listings master table."""

    enriched = listings.copy()
    enriched["id"] = enriched["id"].astype("int64")

    calendar_features = calendar_features.copy()
    calendar_features["listing_id"] = calendar_features["listing_id"].astype("int64")

    review_features = review_features.copy()
    review_features["listing_id"] = review_features["listing_id"].astype("int64")

    enriched = enriched.merge(
        calendar_features,
        how="left",
        left_on="id",
        right_on="listing_id",
    )

    enriched = enriched.merge(
        review_features,
        how="left",
        left_on="id",
        right_on="listing_id",
        suffixes=("", "_review"),
    )

    neighbourhood_column = (
        "neighbourhood_cleansed"
        if "neighbourhood_cleansed" in enriched.columns
        else "neighbourhood"
    )

    enriched["neighbourhood_key"] = enriched[neighbourhood_column].astype("string")

    enriched = enriched.merge(
        neighbourhood_features,
        how="left",
        on="neighbourhood_key",
    )

    enriched["estimated_revenue_proxy"] = (
        enriched["price"] * enriched["occupancy_proxy"] * 365
    ).round(2)

    drop_columns = [
        column
        for column in ["listing_id", "listing_id_review", "neighbourhood_key"]
        if column in enriched.columns
    ]
    enriched = enriched.drop(columns=drop_columns)

    return enriched


def save_enriched_dataset(
    dataframe: pd.DataFrame,
    processed_dir: Path,
) -> Path:
    """Save the enriched listings master table."""

    output_path = processed_dir / "listings_enriched.parquet"
    dataframe.to_parquet(output_path, index=False)
    return output_path


def main() -> None:
    """Run enrichment and create the listings master table."""

    config = load_config()
    processed_dir = get_processed_dir(config)

    listings = load_processed_dataset(processed_dir, "listings_validated")
    calendar = load_processed_dataset(processed_dir, "calendar_validated")
    reviews = load_processed_dataset(processed_dir, "reviews_validated")

    listings = add_derived_listing_fields(listings)

    calendar_features = build_calendar_features(calendar)
    review_features = build_review_features(reviews)
    neighbourhood_features = build_neighbourhood_features(listings)

    listings_enriched = enrich_listings(
        listings=listings,
        calendar_features=calendar_features,
        review_features=review_features,
        neighbourhood_features=neighbourhood_features,
    )

    output_path = save_enriched_dataset(listings_enriched, processed_dir)

    print(f"Enriched listings rows: {len(listings_enriched):,}")
    print(f"Enriched listings columns: {len(listings_enriched.columns)}")
    print(f"Created: {output_path}")
    print("\nSample enriched fields:")
    print(
        listings_enriched[
            [
                "id",
                "price",
                "occupancy_proxy",
                "review_count_detailed",
                "neighbourhood_median_price",
                "price_per_bedroom",
                "estimated_revenue_proxy",
            ]
        ]
        .head()
        .to_string(index=False)
    )
    print("\nData enrichment completed successfully.")


if __name__ == "__main__":
    main()