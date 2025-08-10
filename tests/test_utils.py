from utils import coerce_numeric_fields


def test_coerce_numeric_fields_handles_strings_and_mixed_types():
    data = {
        "list_price": "500000",
        "strata_fee": 250.0,
        "note": "hi",
    }
    result = coerce_numeric_fields(
        data, ["list_price", "strata_fee", "property_tax"]
    )
    assert result["list_price"] == 500000
    assert result["strata_fee"] == 250
    assert "property_tax" not in result
    assert result["note"] == "hi"


def test_coerce_numeric_fields_non_numeric_unchanged():
    data = {"expected_rent": "abc"}
    result = coerce_numeric_fields(data, ["expected_rent"])
    assert result["expected_rent"] == "abc"
