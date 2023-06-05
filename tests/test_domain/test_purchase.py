import pytest

from src.domain.portfolio_event import EmployeePurchase

cases = [
    (None, 1.0),
    (25_000, None),
    (None, None),
    (-1, 1.0),
    (25_000, -1),
    (-1, -1)
]


@pytest.mark.parametrize("price_per_share,share_count", cases)
def test_invalid_employee_purchase(price_per_share, share_count):
    with pytest.raises(ValueError) as e:
        EmployeePurchase(price_per_share, share_count)
    assert str(e.value) == \
        "share_count must be a positive integer, price_per_share must be a positive float"
