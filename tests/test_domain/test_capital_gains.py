import pytest
from src.domain.tax_event import CapitalGains, Lot


@pytest.mark.parametrize(
    "lots1, lots2, expected",
    [
        # Testing identical lots
        (
            [Lot(1, 100.0, 5), Lot(2, 200.0, 10)],
            [Lot(1, 100.0, 5), Lot(2, 200.0, 10)],
            True,
        ),
        # Testing different lot order
        (
            [Lot(1, 100.0, 5), Lot(2, 200.0, 10)],
            [Lot(2, 200.0, 10), Lot(1, 100.0, 5)],
            False,
        ),
        # Testing differing basis_per_share in lot
        (
            [Lot(1, 100.0, 5)],
            [Lot(1, 101.0, 5)],
            False,
        ),
        # Testing differing share_count in lot
        (
            [Lot(1, 100.0, 5)],
            [Lot(1, 100.0, 6)],
            False,
        ),
        # Testing different lengths
        (
            [Lot(1, 100.0, 5)],
            [Lot(1, 100.0, 5), Lot(2, 200.0, 10)],
            False,
        ),
        # Testing None cases
        (None, None, True),
        ([Lot(1, 100.0, 5)], None, False),
        (None, [Lot(1, 100.0, 5)], False),
        # Testing empty list cases
        ([], [], True),
        ([Lot(1, 100.0, 5)], [], False),
        ([], [Lot(1, 100.0, 5)], False),
    ],
)
def test_CapitalGains_eq_lot(lots1, lots2, expected):
    c1 = CapitalGains(1, 1000.0, 200.0, lots1, 0.2)
    c2 = CapitalGains(1, 1000.0, 200.0, lots2, 0.2)

    assert (c1 == c2) is expected
