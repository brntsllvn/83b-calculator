import pytest

from src.events.employment_event import EmployeePurchase
from src.events.tax_event import get_purchase_dollars

cases = [
    (1.0, 25_000, 25_000.0),
    (1.0, 0, 0.0),
    (0.0, 25_000, 0.0),
    (0.0, 0, 0.0)
]


@pytest.mark.parametrize("price_per_share,share_count,expected_purchase_dollars", cases)
def test_get_purchase_dollars(
        price_per_share,
        share_count,
        expected_purchase_dollars):
    assert get_purchase_dollars(
        EmployeePurchase(price_per_share, share_count)) == expected_purchase_dollars


def test_get_purchase_dollars_none():
    with pytest.raises(Exception) as e:
        get_purchase_dollars(None)
    assert str(e.value) == "Employee purchase is None"


def test_get_purchase_dollars_price_is_none():
    with pytest.raises(Exception) as e:
        get_purchase_dollars(EmployeePurchase(None, 1))
    assert str(e.value) == "Employee purchase price per share is None"


def test_get_purchase_dollars_share_count_is_none():
    with pytest.raises(Exception) as e:
        get_purchase_dollars(EmployeePurchase(1, None))
    assert str(e.value) == "Employee purchase share count is None"
