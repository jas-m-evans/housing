from models import mortgage_payment


def test_mortgage_payment_positive():
    price = 750000
    down = 0.2
    rate = 0.05
    principal_cents = int(price * (1 - down) * 100)
    annual_rate_pct = rate * 100
    payment = mortgage_payment(principal=principal_cents, annual_rate=annual_rate_pct)
    assert payment > 10000
