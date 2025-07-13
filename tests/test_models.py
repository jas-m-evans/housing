from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from models import mortgage_payment


def test_mortgage_payment_known_value():
    principal = 400_000 * 100  # 400k CAD in cents
    payment = mortgage_payment(principal, annual_rate=5.0, amort_years=25)
    assert payment == 233_836
