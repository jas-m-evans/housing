import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))

from models import simulate_property, key_metrics


def test_simulation_shape_and_metrics():
    np.random.seed(0)
    n_sim = 100
    horizon = 5
    df = simulate_property(
        price=500_000,
        rent=2000,
        down_pct=20.0,
        annual_rate=5.0,
        strata_fee=300,
        property_tax=2000,
        vacancy_pct=2.0,
        n_sim=n_sim,
        horizon_years=horizon,
    )
    assert df.shape == (n_sim * horizon, 5)

    metrics = key_metrics(df)
    expected_keys = {
        "monthly_mortgage",
        "p50_cash_flow",
        "p10_cash_flow",
        "p90_cash_flow",
        "p50_equity_year10",
    }
    assert expected_keys <= metrics.keys()
    for value in metrics.values():
        assert isinstance(value, (int, float))

