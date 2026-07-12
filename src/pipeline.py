from __future__ import annotations

import logging
import sys
import time
from collections.abc import Callable

from src.config import load_config
from src.database import main as build_database
from src.extract_files import main as extract_files
from src.profile_datasets import main as profile_datasets
from src.cleaning import main as clean_datasets
from src.validation import main as validate_datasets
from src.transformations import main as enrich_datasets


def setup_logging(log_level: str) -> None:
    """Configure pipeline logging."""

    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def run_step(step_name: str, step_function: Callable[[], None]) -> None:
    """Run one pipeline step with logging and error handling."""

    logger = logging.getLogger(__name__)
    logger.info("Starting step: %s", step_name)
    start_time = time.time()

    try:
        step_function()
    except Exception:
        logger.exception("Pipeline failed during step: %s", step_name)
        raise

    elapsed = round(time.time() - start_time, 2)
    logger.info("Completed step: %s in %ss", step_name, elapsed)


def extraction_required() -> bool:
    """Check whether gzip extraction still needs to run."""

    config = load_config()

    extracted_files = [
        config.interim_file("listings_detailed_extracted"),
        config.interim_file("calendar_detailed_extracted"),
        config.interim_file("reviews_detailed_extracted"),
    ]

    return not all(file_path.exists() for file_path in extracted_files)


def run_pipeline() -> None:
    """Execute the full data engineering pipeline."""

    config = load_config()
    setup_logging(config.pipeline.log_level)

    logger = logging.getLogger(__name__)
    logger.info(
        "Running Airbnb pipeline for %s (%s)",
        config.city.name,
        config.city.snapshot_date,
    )

    steps: list[tuple[str, Callable[[], None]]] = []

    if extraction_required():
        steps.append(("extract_files", extract_files))
    else:
        logger.info("Skipping extract_files because interim files already exist")

    steps.extend(
        [
            ("profile_datasets", profile_datasets),
            ("clean_datasets", clean_datasets),
            ("validate_datasets", validate_datasets),
            ("enrich_datasets", enrich_datasets),
            ("build_database", build_database),
        ]
    )

    for step_name, step_function in steps:
        run_step(step_name, step_function)

    logger.info("Pipeline completed successfully")


def main() -> None:
    """Pipeline entry point."""

    run_pipeline()


if __name__ == "__main__":
    main()