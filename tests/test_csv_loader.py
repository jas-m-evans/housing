from io import StringIO
import pandas as pd


def test_csv_loader_types():
    csv = "address,list_price,bedrooms,bathrooms\n123 A St,500000,2,2"
    df = pd.read_csv(StringIO(csv))
    assert df['list_price'].dtype.kind in "iu"
    assert df['bedrooms'].dtype.kind in "iuf"
    assert df['bathrooms'].dtype.kind in "iuf"


def test_csv_loader_missing_optional_columns():
    csv = "address,list_price\n123 A St,500000"
    try:
        df = pd.read_csv(StringIO(csv))
    except Exception as exc:  # pragma: no cover - should not happen
        raise AssertionError(f"Reading CSV raised {exc}")
    assert 'address' in df.columns
    assert df['list_price'].iloc[0] == 500000
