import pandas as pd

from src.validation import build_report_row, validate_listings


def test_build_report_row_calculates_failed_percentage():
    row = build_report_row(
        dataset="listings",
        rule_name="missing_id",
        rule_description="Listing id must not be null",
        total_rows=100,
        failed_rows=5,
        action="remove",
    )
    assert row["failed_percentage"] == 5.0


def test_validate_listings_removes_duplicate_ids():
    listings = pd.DataFrame(
        {
            "id": [1, 1, 2],
            "price": [100.0, 120.0, 200.0],
            "latitude": [55.95, 55.95, 55.96],
            "longitude": [-3.19, -3.19, -3.20],
        }
    )

    validated, report_rows = validate_listings(listings)

    assert len(validated) == 2
    assert validated["id"].is_unique
    assert any(row["rule_name"] == "duplicate_id" for row in report_rows)


def test_validate_listings_flags_invalid_prices_without_removing():
    listings = pd.DataFrame(
        {
            "id": [1, 2],
            "price": [150.0, None],
            "latitude": [55.95, 55.96],
            "longitude": [-3.19, -3.20],
        }
    )

    validated, report_rows = validate_listings(listings)

    assert len(validated) == 2
    assert "is_valid_price" in validated.columns
    assert validated.loc[validated["id"] == 2, "is_valid_price"].iloc[0] == False
    assert any(row["rule_name"] == "invalid_price" for row in report_rows)
