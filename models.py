"""Financial models for Dwelly."""

from __future__ import annotations

import numpy as np
import pandas as pd


def mortgage_payment(principal: int, annual_rate: float, amort_years: int = 25) -> int:
    """Return the monthly mortgage payment in CAD cents.

    Args:
        principal: Loan principal in CAD cents.
        annual_rate: Annual interest rate as a percentage (e.g., 5 for 5%).
        amort_years: Amortization period in years. Defaults to 25.

    Returns:
        Monthly payment in CAD cents.
    """
    months = amort_years * 12
    monthly_rate = (annual_rate / 100) / 12
    if monthly_rate == 0:
        payment = principal / months
    else:
        payment = (
            principal
            * monthly_rate
            * (1 + monthly_rate) ** months
            / ((1 + monthly_rate) ** months - 1)
        )
    return int(round(payment))


def cash_flow(*args, **kwargs):
    """Calculate monthly cash flow.

    TODO: implement in later iterations.
    """
    pass




# ---------------------------------------------------------------------------
# Monte Carlo Simulation
# ---------------------------------------------------------------------------

def simulate_property(
    price: int,
    rent: int,
    down_pct: float,
    annual_rate: float,
    strata_fee: int,
    property_tax: int,
    vacancy_pct: float,
    n_sim: int = 1000,
    horizon_years: int = 10,
) -> pd.DataFrame:
    """Simulate property cash flows and equity over time."""
    principal = int(round(price * (1 - down_pct / 100))) * 100
    monthly_payment_cents = mortgage_payment(principal, annual_rate)
    monthly_payment = monthly_payment_cents / 100

    months_total = horizon_years * 12
    monthly_rate = (annual_rate / 100) / 12
    payments = np.arange(1, months_total + 1)
    balance = principal * (
        (1 + monthly_rate) ** months_total - (1 + monthly_rate) ** payments
    ) / ((1 + monthly_rate) ** months_total - 1)
    balance = np.append(principal, balance[11::12]) / 100

    growth = np.random.normal(1.03, 0.02, size=(n_sim, horizon_years))
    price_paths = price * growth.cumprod(axis=1)

    rent_noise = np.random.normal(1.0, 0.05, size=(n_sim, horizon_years))
    annual_rent = rent * rent_noise * (1 - vacancy_pct / 100) * 12

    mortgage_yearly = monthly_payment * 12
    strata_yearly = strata_fee * 12

    net_cf = annual_rent - mortgage_yearly - strata_yearly - property_tax
    equity = price_paths - balance[1:]
    cumulative_cf = np.cumsum(net_cf, axis=1)

    years = np.arange(1, horizon_years + 1)

    df = pd.DataFrame(
        {
            "year": np.tile(years, n_sim),
            "sim": np.repeat(np.arange(n_sim), horizon_years),
            "net_cash_flow": net_cf.flatten(),
            "equity": equity.flatten(),
            "cumulative_cf": cumulative_cf.flatten(),
        }
    )
    df.attrs["monthly_mortgage"] = monthly_payment
    return df


def key_metrics(df: pd.DataFrame) -> dict[str, float]:
    """Return key metrics from simulation DataFrame."""
    first_year = df[df["year"] == 1]
    metrics = {
        "monthly_mortgage": float(df.attrs.get("monthly_mortgage", 0)),
        "p50_cash_flow": float(first_year["net_cash_flow"].median()),
        "p10_cash_flow": float(first_year["net_cash_flow"].quantile(0.1)),
        "p90_cash_flow": float(first_year["net_cash_flow"].quantile(0.9)),
        "p50_equity_year10": float(
            df[df["year"] == df["year"].max()]["equity"].median()
        ),
    }
    return metrics

