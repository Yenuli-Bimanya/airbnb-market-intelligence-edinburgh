from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd


from src.config import load_config

config = load_config()

RAW_DIR = config.paths.raw_data
INTERIM_DIR = config.paths.interim_data
METADATA_DIR = config.paths.metadata

CSV_FILES = {
    "listings_detailed": config.interim_file("listings_detailed_extracted"),
    "calendar_detailed": config.interim_file("calendar_detailed_extracted"),
    "reviews_detailed": config.interim_file("reviews_detailed_extracted"),
    "listings_summary": config.raw_file("listings_summary"),
    "reviews_summary": config.raw_file("reviews_summary"),
    "neighbourhoods": config.raw_file("neighbourhoods"),
}

GEOJSON_FILE = config.raw_file("neighbourhoods_geojson")


def validate_files() -> None:
    """Confirm that every expected input file exists."""

    expected_files = list(CSV_FILES.values()) + [GEOJSON_FILE]

    missing_files = [
        file_path
        for file_path in expected_files
        if not file_path.exists()
    ]

    if missing_files:
        formatted_files = "\n".join(
            f"- {file_path}" for file_path in missing_files
        )

        raise FileNotFoundError(
            f"The following source files are missing:\n{formatted_files}"
        )


def duckdb_csv_source(file_path: Path) -> str:
    """Create a safe DuckDB CSV table expression."""

    escaped_path = file_path.as_posix().replace("'", "''")

    return (
        "read_csv_auto("
        f"'{escaped_path}', "
        "header=true, "
        "sample_size=200000"
        ")"
    )


def python_type_name(value: Any) -> str:
    """Return a readable Python type name for a GeoJSON property."""

    if value is None:
        return "NULL"

    return type(value).__name__


def profile_csv_files(
    connection: duckdb.DuckDBPyConnection,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Generate inventory and schema reports for all CSV datasets."""

    inventory_records: list[dict[str, Any]] = []
    schema_frames: list[pd.DataFrame] = []

    for dataset_name, file_path in CSV_FILES.items():
        print(f"Profiling {dataset_name}...")

        source = duckdb_csv_source(file_path)

        row_count = connection.execute(
            f"SELECT COUNT(*) FROM {source}"
        ).fetchone()[0]

        schema = connection.execute(
            f"DESCRIBE SELECT * FROM {source}"
        ).fetchdf()

        schema.insert(0, "dataset", dataset_name)
        schema_frames.append(schema)

        inventory_records.append(
            {
                "dataset": dataset_name,
                "file_name": file_path.name,
                "file_format": "CSV",
                "row_count": row_count,
                "column_count": len(schema),
                "size_bytes": file_path.stat().st_size,
                "size_mb": round(
                    file_path.stat().st_size / (1024**2),
                    2,
                ),
            }
        )

    inventory = pd.DataFrame(inventory_records)
    schema_report = pd.concat(schema_frames, ignore_index=True)

    return inventory, schema_report


def profile_geojson() -> tuple[dict[str, Any], pd.DataFrame]:
    """Generate inventory and property-schema details for the GeoJSON file."""

    print("Profiling neighbourhoods_geojson...")

    with GEOJSON_FILE.open(
        "r",
        encoding="utf-8",
    ) as geojson_file:
        geojson_data = json.load(geojson_file)

    features = geojson_data.get("features", [])

    property_types: dict[str, set[str]] = {}

    for feature in features:
        properties = feature.get("properties", {})

        for property_name, value in properties.items():
            property_types.setdefault(property_name, set()).add(
                python_type_name(value)
            )

    geometry_types = sorted(
        {
            feature.get("geometry", {}).get("type", "Unknown")
            for feature in features
        }
    )

    schema_records = [
        {
            "dataset": "neighbourhoods_geojson",
            "column_name": property_name,
            "column_type": ", ".join(sorted(types)),
            "null": "UNKNOWN",
            "key": None,
            "default": None,
            "extra": "GeoJSON property",
        }
        for property_name, types in sorted(property_types.items())
    ]

    schema_records.append(
        {
            "dataset": "neighbourhoods_geojson",
            "column_name": "geometry",
            "column_type": ", ".join(geometry_types),
            "null": "UNKNOWN",
            "key": None,
            "default": None,
            "extra": "GeoJSON geometry",
        }
    )

    inventory_record = {
        "dataset": "neighbourhoods_geojson",
        "file_name": GEOJSON_FILE.name,
        "file_format": "GeoJSON",
        "row_count": len(features),
        "column_count": len(property_types) + 1,
        "size_bytes": GEOJSON_FILE.stat().st_size,
        "size_mb": round(
            GEOJSON_FILE.stat().st_size / (1024**2),
            2,
        ),
    }

    return inventory_record, pd.DataFrame(schema_records)


def main() -> None:
    """Run dataset inventory and schema profiling."""

    validate_files()
    METADATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = duckdb.connect()

    try:
        inventory, schema_report = profile_csv_files(connection)

        geojson_inventory, geojson_schema = profile_geojson()

        inventory = pd.concat(
            [
                inventory,
                pd.DataFrame([geojson_inventory]),
            ],
            ignore_index=True,
        )

        schema_report = pd.concat(
            [
                schema_report,
                geojson_schema,
            ],
            ignore_index=True,
        )

        inventory_output = METADATA_DIR / "dataset_inventory.csv"
        schema_output = METADATA_DIR / "schema_report.csv"

        inventory.to_csv(inventory_output, index=False)
        schema_report.to_csv(schema_output, index=False)

        print("\nDataset inventory:")
        print(inventory.to_string(index=False))

        print(f"\nCreated: {inventory_output}")
        print(f"Created: {schema_output}")
        print("\nDataset profiling completed successfully.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()