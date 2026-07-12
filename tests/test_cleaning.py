import pandas as pd

from src.cleaning import (
    clean_price,
    normalize_room_type,
    normalize_text,
    standardize_available,
)


def test_clean_price_removes_currency_symbols():
    assert clean_price("$225.50") == 225.5
    assert clean_price("£1,200") == 1200.0


def test_clean_price_handles_missing_values():
    assert clean_price(None) is None
    assert clean_price(pd.NA) is None


def test_normalize_text_trims_and_nulls_empty_strings():
    assert normalize_text("  hello  ") == "hello"
    assert normalize_text("   ") is None


def test_normalize_room_type_standardizes_labels():
    assert normalize_room_type("entire home/apt") == "Entire home/apt"
    assert normalize_room_type("PRIVATE ROOM") == "Private room"


def test_standardize_available_parses_common_values():
    assert standardize_available("t") is True
    assert standardize_available("f") is False
    assert standardize_available(True) is True
    assert standardize_available("unknown") is None
