import pytest

from src.events.employment_event import EmployeePurchase
from src.events.tax_event import get_purchase_dollars

cases = [
    (1.0, 25_000, 25_000),
    (1.0, 0, 0),
    (0.0, 25_000, 0),
    (0.0, 0, 0)
]


@pytest.mark.parametrize("price_per_share,share_count,expected_purchase_dollars", cases)
def test_get_purchase_dollars(
        price_per_share,
        share_count,
        expected_purchase_dollars):
    assert get_purchase_dollars(
        EmployeePurchase(price_per_share, share_count)) == expected_purchase_dollars


def test_get_purchase_dollars_none():
    assert get_purchase_dollars(None) == 0.0
