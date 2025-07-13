"""Financial models for DwellWell."""

from __future__ import annotations


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
