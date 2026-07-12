from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from src.config import load_config

#Removes $ and text, converts to float
def clean_price(value: object) -> float | None:
    """Convert listing price values to float."""

    if pd.isna(value):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    cleaned = re.sub(r"[^0-9.]", "", str(value))

    if not cleaned:
        return None

    return float(cleaned)

#Removes whitespace and converts empty strings to null
def normalize_text(value: object) -> str | None:
    """Trim whitespace and convert empty strings to null."""

    if pd.isna(value):
        return None

    text = str(value).strip()

    if not text:
        return None

    return text

#Standardizes room type labels
def normalize_room_type(value: object) -> str | None:
    """Standardize room type labels."""

    text = normalize_text(value)

    if text is None:
        return None

    mapping = {
        "entire home/apt": "Entire home/apt",
        "private room": "Private room",
        "shared room": "Shared room",
        "hotel room": "Hotel room",
    }

    return mapping.get(text.lower(), text)

#Standardizes property type labels
def normalize_property_type(value: object) -> str | None:
    """Standardize property type labels."""

    text = normalize_text(value)

    if text is None:
        return None

    return " ".join(text.split())

#Parses date-like columns safely
def parse_date_column(series: pd.Series) -> pd.Series:
    """Parse date-like columns safely."""

    return pd.to_datetime(series, errors="coerce")

#Converts calendar availability values to booleans
def standardize_available(value: object) -> bool | None:
    """Convert calendar availability values to booleans."""

    if pd.isna(value):
        return None

    if isinstance(value, bool):
        return value

    text = str(value).strip().lower()

    if text in {"t", "true", "1", "yes"}:
        return True

    if text in {"f", "false", "0", "no"}:
        return False

    return None

#Creates processed output folder for the selected city snapshot
def get_output_dir(config) -> Path:
    """Create processed output folder for the selected city snapshot."""

    output_dir = (
        config.paths.processed_data
        / config.city.name.lower()
        / config.city.snapshot_date
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

#Saves cleaned dataset as parquet or csv
def save_dataset(
    dataframe: pd.DataFrame,
    output_dir: Path,
    file_stem: str,
    save_parquet: bool,
) -> Path:
    """Save cleaned dataset as parquet or csv."""

    if save_parquet:
        output_path = output_dir / f"{file_stem}.parquet"
        dataframe.to_parquet(output_path, index=False)
    else:
        output_path = output_dir / f"{file_stem}.csv"
        dataframe.to_csv(output_path, index=False)

    return output_path

#Cleans the detailed listings dataset
def clean_listings(config) -> pd.DataFrame:
    """Clean the detailed listings dataset."""

    input_path = config.interim_file("listings_detailed_extracted")
    listings = pd.read_csv(input_path)

    listings["price"] = listings["price"].apply(clean_price)
    listings["room_type"] = listings["room_type"].apply(normalize_room_type)
    listings["property_type"] = listings["property_type"].apply(
        normalize_property_type
    )
    listings["neighbourhood"] = listings["neighbourhood"].apply(normalize_text)
    listings["neighbourhood_cleansed"] = listings["neighbourhood_cleansed"].apply(
        normalize_text
    )

    date_columns = [
        "host_since",
        "last_review",
        "first_review",
        "last_scraped",
        "calendar_last_scraped",
    ]

    for column in date_columns:
        if column in listings.columns:
            listings[column] = parse_date_column(listings[column])

    numeric_columns = [
        "latitude",
        "longitude",
        "bedrooms",
        "beds",
        "bathrooms",
        "accommodates",
        "minimum_nights",
        "maximum_nights",
        "availability_365",
        "number_of_reviews",
        "reviews_per_month",
    ]

    for column in numeric_columns:
        if column in listings.columns:
            listings[column] = pd.to_numeric(listings[column], errors="coerce")

    return listings

#Cleans the detailed calendar dataset
def clean_calendar(config) -> pd.DataFrame:
    """Clean the detailed calendar dataset."""

    input_path = config.interim_file("calendar_detailed_extracted")
    calendar = pd.read_csv(input_path)

    calendar["date"] = parse_date_column(calendar["date"])
    calendar["available"] = calendar["available"].apply(standardize_available)

    numeric_columns = ["minimum_nights", "maximum_nights"]

    for column in numeric_columns:
        if column in calendar.columns:
            calendar[column] = pd.to_numeric(calendar[column], errors="coerce")

    return calendar

#Cleans the detailed reviews dataset
def clean_reviews(config) -> pd.DataFrame:
    """Clean the detailed reviews dataset."""

    input_path = config.interim_file("reviews_detailed_extracted")
    reviews = pd.read_csv(input_path)

    reviews["date"] = parse_date_column(reviews["date"])
    reviews["comments"] = reviews["comments"].apply(normalize_text)
    reviews["reviewer_name"] = reviews["reviewer_name"].apply(normalize_text)

    return reviews

#Cleans the neighbourhoods lookup dataset
def clean_neighbourhoods(config) -> pd.DataFrame:
    """Clean the neighbourhoods lookup dataset."""

    input_path = config.raw_file("neighbourhoods")
    neighbourhoods = pd.read_csv(input_path)

    neighbourhoods["neighbourhood"] = neighbourhoods["neighbourhood"].apply(
        normalize_text
    )
    neighbourhoods["neighbourhood_group"] = neighbourhoods[
        "neighbourhood_group"
    ].apply(normalize_text)

    return neighbourhoods


#Runs all cleaning steps and saves processed outputs
def main() -> None:
    """Run all cleaning steps and save processed outputs."""

    config = load_config()
    output_dir = get_output_dir(config)

    cleaners = {
        "listings_clean": clean_listings,
        "calendar_clean": clean_calendar,
        "reviews_clean": clean_reviews,
        "neighbourhoods_clean": clean_neighbourhoods,
    }

    for output_name, cleaner in cleaners.items():
        print(f"Cleaning {output_name}...")
        cleaned_data = cleaner(config)

        output_path = save_dataset(
            dataframe=cleaned_data,
            output_dir=output_dir,
            file_stem=output_name,
            save_parquet=config.pipeline.save_parquet,
        )

        print(f"  rows: {len(cleaned_data):,}")
        print(f"  saved: {output_path}")

    print("\nData cleaning completed successfully.")


if __name__ == "__main__":
    main()