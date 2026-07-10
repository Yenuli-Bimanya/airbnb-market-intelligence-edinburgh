from __future__ import annotations

import gzip
import shutil
from pathlib import Path


RAW_DIR = Path("data/raw/edinburgh/2026-06-23")
OUTPUT_DIR = Path("data/interim/edinburgh/2026-06-23")

FILES_TO_EXTRACT = {
    "listings.csv.gz": "listings_detailed.csv",
    "calendar.csv.gz": "calendar_detailed.csv",
    "reviews.csv.gz": "reviews_detailed.csv",
}


def extract_gzip_file(source: Path, destination: Path) -> None:
    """Extract a gzip file while preserving the original raw file."""

    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")

    destination.parent.mkdir(parents=True, exist_ok=True)

    with gzip.open(source, "rb") as compressed_file:
        with destination.open("wb") as extracted_file:
            shutil.copyfileobj(compressed_file, extracted_file)

    print(f"Extracted: {source.name} -> {destination.name}")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for source_name, destination_name in FILES_TO_EXTRACT.items():
        extract_gzip_file(
            source=RAW_DIR / source_name,
            destination=OUTPUT_DIR / destination_name,
        )

    print("\nAll detailed gzip files were extracted successfully.")


if __name__ == "__main__":
    main()