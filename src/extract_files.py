from __future__ import annotations

import gzip
import shutil
from pathlib import Path


from src.config import load_config

config = load_config()
RAW_DIR = config.paths.raw_data
OUTPUT_DIR = config.paths.interim_data

FILES_TO_EXTRACT = {
    config.files.listings_detailed_raw: config.files.listings_detailed_extracted,
    config.files.calendar_detailed_raw: config.files.calendar_detailed_extracted,
    config.files.reviews_detailed_raw: config.files.reviews_detailed_extracted,
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