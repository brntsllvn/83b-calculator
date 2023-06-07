import pytest

from src.execute.analytics import calculate_npv

@pytest.mark.parametrize(
    "cash_flows, discount_rate, expected, test_case",
    [
        ([100, 100, 100, 100, 100], 0.05, 454.60, "All Positive Cash Flows"),
        ([-100, -100, -100, -100, -100], 0.05, -454.60, "All Negative Cash Flows"),
        ([None, None, None, None, None], 0.05, TypeError, "Cash Flows as None"),
        (["😀", "😃", "😄", "😁", "😆"], 0.05, TypeError, "Emoji Cash Flows"),
        (["100", "200", "300", "400", "500"], 0.05, TypeError, "String Cash Flows"),
        (["", "", "", "", ""], 0.05, TypeError, "Empty String Cash Flows"),
        ([-100, 200, -300, 400, -500], 0.05, -247.45, "Alternating Negative and Positive Cash Flows"),
        ([100, -200, 300, -400, 500], 0.05, 247.45, "Alternating Positive and Negative Cash Flows"),
        ([-100, -200, 300, 400, 500], 0.05, 738.52, "Starts Negative, Ends Positive"),
        ([100, 200, -300, -400, -500], 0.05, -738.52, "Starts Positive, Ends Negative"),
    ],
)
def test_npv(cash_flows, discount_rate, expected, test_case):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected, match="Invalid input"):
            calculate_npv(cash_flows, discount_rate)
    else:
        assert pytest.approx(calculate_npv(cash_flows, discount_rate), 0.01) == expected, f"Failed for test case: {test_case}"
