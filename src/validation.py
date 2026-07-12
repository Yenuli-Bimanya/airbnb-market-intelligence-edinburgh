from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import load_config


# Edinburgh geographic bounds used for basic coordinate validation
LATITUDE_MIN = 55.85
LATITUDE_MAX = 56.05
LONGITUDE_MIN = -3.50
LONGITUDE_MAX = -3.00

PRICE_MIN = 0
PRICE_MAX = 10000


def get_processed_dir(config) -> Path:
    """Return the processed data folder for the selected city snapshot."""

    return (
        config.paths.processed_data
        / config.city.name.lower()
        / config.city.snapshot_date
    )


def load_processed_dataset(processed_dir: Path, file_stem: str) -> pd.DataFrame:
    """Load a cleaned parquet dataset."""

    file_path = processed_dir / f"{file_stem}.parquet"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Processed file not found: {file_path}. Run cleaning first."
        )

    return pd.read_parquet(file_path)


def build_report_row(
    dataset: str,
    rule_name: str,
    rule_description: str,
    total_rows: int,
    failed_rows: int,
    action: str,
) -> dict[str, object]:
    """Create one validation report record."""

    failed_percentage = round((failed_rows / total_rows) * 100, 4) if total_rows else 0.0

    return {
        "dataset": dataset,
        "rule_name": rule_name,
        "rule_description": rule_description,
        "total_rows": total_rows,
        "failed_rows": failed_rows,
        "failed_percentage": failed_percentage,
        "action": action,
    }


def validate_listings(listings: pd.DataFrame) -> tuple[pd.DataFrame, list[dict[str, object]]]:
    """Validate listing records and return validated data plus report rows."""

    report_rows: list[dict[str, object]] = []
    total_rows = len(listings)

    missing_id_mask = listings["id"].isna()
    report_rows.append(
        build_report_row(
            dataset="listings",
            rule_name="missing_id",
            rule_description="Listing id must not be null",
            total_rows=total_rows,
            failed_rows=int(missing_id_mask.sum()),
            action="remove",
        )
    )
    listings = listings[~missing_id_mask].copy()

    duplicate_mask = listings["id"].duplicated(keep=False)
    duplicate_count = int(duplicate_mask.sum())
    report_rows.append(
        build_report_row(
            dataset="listings",
            rule_name="duplicate_id",
            rule_description="Duplicate listing ids should be removed, keeping first record",
            total_rows=len(listings),
            failed_rows=duplicate_count,
            action="remove_duplicates_keep_first",
        )
    )
    listings = listings.drop_duplicates(subset=["id"], keep="first").copy()

    invalid_price_mask = (
        listings["price"].isna()
        | (listings["price"] < PRICE_MIN)
        | (listings["price"] > PRICE_MAX)
    )
    report_rows.append(
        build_report_row(
            dataset="listings",
            rule_name="invalid_price",
            rule_description="Price must be between 0 and 10000",
            total_rows=len(listings),
            failed_rows=int(invalid_price_mask.sum()),
            action="flag",
        )
    )
    listings["is_valid_price"] = ~invalid_price_mask

    invalid_latitude_mask = (
        listings["latitude"].isna()
        | (listings["latitude"] < LATITUDE_MIN)
        | (listings["latitude"] > LATITUDE_MAX)
    )
    report_rows.append(
        build_report_row(
            dataset="listings",
            rule_name="invalid_latitude",
            rule_description="Latitude must fall within Edinburgh bounds",
            total_rows=len(listings),
            failed_rows=int(invalid_latitude_mask.sum()),
            action="flag",
        )
    )
    listings["is_valid_latitude"] = ~invalid_latitude_mask

    invalid_longitude_mask = (
        listings["longitude"].isna()
        | (listings["longitude"] < LONGITUDE_MIN)
        | (listings["longitude"] > LONGITUDE_MAX)
    )
    report_rows.append(
        build_report_row(
            dataset="listings",
            rule_name="invalid_longitude",
            rule_description="Longitude must fall within Edinburgh bounds",
            total_rows=len(listings),
            failed_rows=int(invalid_longitude_mask.sum()),
            action="flag",
        )
    )
    listings["is_valid_longitude"] = ~invalid_longitude_mask

    listings["is_valid_location"] = (
        listings["is_valid_latitude"] & listings["is_valid_longitude"]
    )

    return listings, report_rows


def validate_calendar(calendar: pd.DataFrame) -> tuple[pd.DataFrame, list[dict[str, object]]]:
    """Validate calendar records and return validated data plus report rows."""

    report_rows: list[dict[str, object]] = []
    total_rows = len(calendar)

    missing_listing_id_mask = calendar["listing_id"].isna()
    report_rows.append(
        build_report_row(
            dataset="calendar",
            rule_name="missing_listing_id",
            rule_description="Calendar listing_id must not be null",
            total_rows=total_rows,
            failed_rows=int(missing_listing_id_mask.sum()),
            action="remove",
        )
    )
    calendar = calendar[~missing_listing_id_mask].copy()

    missing_date_mask = calendar["date"].isna()
    report_rows.append(
        build_report_row(
            dataset="calendar",
            rule_name="missing_date",
            rule_description="Calendar date must not be null",
            total_rows=len(calendar),
            failed_rows=int(missing_date_mask.sum()),
            action="remove",
        )
    )
    calendar = calendar[~missing_date_mask].copy()

    invalid_available_mask = calendar["available"].isna()
    report_rows.append(
        build_report_row(
            dataset="calendar",
            rule_name="invalid_available",
            rule_description="Calendar availability must be True or False",
            total_rows=len(calendar),
            failed_rows=int(invalid_available_mask.sum()),
            action="flag",
        )
    )
    calendar["is_valid_available"] = ~invalid_available_mask

    return calendar, report_rows


def validate_reviews(reviews: pd.DataFrame) -> tuple[pd.DataFrame, list[dict[str, object]]]:
    """Validate review records and return validated data plus report rows."""

    report_rows: list[dict[str, object]] = []
    total_rows = len(reviews)

    missing_review_id_mask = reviews["id"].isna()
    report_rows.append(
        build_report_row(
            dataset="reviews",
            rule_name="missing_review_id",
            rule_description="Review id must not be null",
            total_rows=total_rows,
            failed_rows=int(missing_review_id_mask.sum()),
            action="remove",
        )
    )
    reviews = reviews[~missing_review_id_mask].copy()

    missing_listing_id_mask = reviews["listing_id"].isna()
    report_rows.append(
        build_report_row(
            dataset="reviews",
            rule_name="missing_listing_id",
            rule_description="Review listing_id must not be null",
            total_rows=len(reviews),
            failed_rows=int(missing_listing_id_mask.sum()),
            action="remove",
        )
    )
    reviews = reviews[~missing_listing_id_mask].copy()

    missing_date_mask = reviews["date"].isna()
    report_rows.append(
        build_report_row(
            dataset="reviews",
            rule_name="missing_date",
            rule_description="Review date must not be null",
            total_rows=len(reviews),
            failed_rows=int(missing_date_mask.sum()),
            action="flag",
        )
    )
    reviews["is_valid_date"] = ~missing_date_mask

    duplicate_review_id_mask = reviews["id"].duplicated(keep=False)
    report_rows.append(
        build_report_row(
            dataset="reviews",
            rule_name="duplicate_review_id",
            rule_description="Duplicate review ids should be removed, keeping first record",
            total_rows=len(reviews),
            failed_rows=int(duplicate_review_id_mask.sum()),
            action="remove_duplicates_keep_first",
        )
    )
    reviews = reviews.drop_duplicates(subset=["id"], keep="first").copy()

    return reviews, report_rows


def save_validated_dataset(
    dataframe: pd.DataFrame,
    processed_dir: Path,
    file_stem: str,
) -> Path:
    """Save validated dataset to the processed folder."""

    output_path = processed_dir / f"{file_stem}.parquet"
    dataframe.to_parquet(output_path, index=False)
    return output_path


def main() -> None:
    """Run validation checks and save report plus validated datasets."""

    config = load_config()
    processed_dir = get_processed_dir(config)
    metadata_dir = config.paths.metadata
    metadata_dir.mkdir(parents=True, exist_ok=True)

    listings = load_processed_dataset(processed_dir, "listings_clean")
    calendar = load_processed_dataset(processed_dir, "calendar_clean")
    reviews = load_processed_dataset(processed_dir, "reviews_clean")

    listings_validated, listings_report = validate_listings(listings)
    calendar_validated, calendar_report = validate_calendar(calendar)
    reviews_validated, reviews_report = validate_reviews(reviews)

    validation_report = pd.DataFrame(
        listings_report + calendar_report + reviews_report
    )

    report_output = metadata_dir / "validation_report.csv"
    validation_report.to_csv(report_output, index=False)

    listings_output = save_validated_dataset(
        listings_validated, processed_dir, "listings_validated"
    )
    calendar_output = save_validated_dataset(
        calendar_validated, processed_dir, "calendar_validated"
    )
    reviews_output = save_validated_dataset(
        reviews_validated, processed_dir, "reviews_validated"
    )

    print("Validation report:")
    print(validation_report.to_string(index=False))

    print(f"\nCreated: {report_output}")
    print(f"Created: {listings_output}")
    print(f"Created: {calendar_output}")
    print(f"Created: {reviews_output}")
    print("\nData validation completed successfully.")


if __name__ == "__main__":
    main()