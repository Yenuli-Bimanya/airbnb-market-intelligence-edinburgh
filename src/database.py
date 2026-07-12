from __future__ import annotations

from pathlib import Path

import duckdb

from src.config import load_config


def get_processed_dir(config) -> Path:
    """Return processed data folder for the selected city snapshot."""

    return (
        config.paths.processed_data
        / config.city.name.lower()
        / config.city.snapshot_date
    )


def escape_path(file_path: Path) -> str:
    """Escape a file path for safe use inside SQL strings."""

    return str(file_path.resolve()).replace("'", "''")


def load_staging_tables(connection: duckdb.DuckDBPyConnection, processed_dir: Path) -> None:
    """Load processed parquet files into staging tables."""

    table_files = {
        "staging_listings": processed_dir / "listings_enriched.parquet",
        "staging_calendar": processed_dir / "calendar_validated.parquet",
        "staging_reviews": processed_dir / "reviews_validated.parquet",
        "staging_neighbourhoods": processed_dir / "neighbourhoods_clean.parquet",
    }

    for table_name, file_path in table_files.items():
        if not file_path.exists():
            raise FileNotFoundError(f"Missing processed file: {file_path}")

        escaped_path = escape_path(file_path)
        connection.execute(
            f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT * FROM read_parquet('{escaped_path}')
            """
        )
        print(f"Loaded {table_name} from {file_path.name}")


def run_sql_file(connection: duckdb.DuckDBPyConnection, sql_file: Path) -> None:
    """Execute all SQL statements in a file."""

    if not sql_file.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_file}")

    sql_text = sql_file.read_text(encoding="utf-8")
    connection.execute(sql_text)
    print(f"Executed {sql_file.name}")


def print_table_counts(connection: duckdb.DuckDBPyConnection) -> None:
    """Print row counts for warehouse tables."""

    tables = [
        "dw.dim_date",
        "dw.dim_neighbourhood",
        "dw.dim_host",
        "dw.dim_listing",
        "dw.fact_calendar",
        "dw.fact_reviews",
        "dw.fact_listing_performance",
    ]

    print("\nWarehouse table counts:")
    for table_name in tables:
        count = connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"  {table_name}: {count:,}")


def main() -> None:
    """Build the DuckDB star schema from processed pipeline outputs."""

    config = load_config()
    processed_dir = get_processed_dir(config)
    project_root = Path(__file__).resolve().parents[1]
    sql_dir = project_root / "sql"

    database_path = config.paths.database
    database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = duckdb.connect(str(database_path))

    try:
        print(f"Using database: {database_path}")

        run_sql_file(connection, sql_dir / "create_schema.sql")
        load_staging_tables(connection, processed_dir)
        run_sql_file(connection, sql_dir / "create_dimensions.sql")
        run_sql_file(connection, sql_dir / "create_facts.sql")

        print_table_counts(connection)
        print("\nDuckDB star schema created successfully.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()