from src.domain.portfolio_event import Grant, File83b, Vest, Sell
from src.domain.purchase import EmployeePurchase
from src.events.portfolio_event import get_portfolio_events
from src.domain.tax_event import IncomeTax, CapitalGains
from src.domain.lot import Lot
from src.events.tax_event import get_tax_events

# https://www.irs.gov/irb/2012-28_IRB#RP-2012-29
# Example (1)


def test_get_portfolio_events_file_83b_with_purchase(
        portfolio_event_data_with_purchase):
    portfolio_events = get_portfolio_events(
        True, portfolio_event_data_with_purchase)
    assert len(portfolio_events) == 4
    assert portfolio_events[0] == Grant(
        0, 25_000, EmployeePurchase(25_000, 1.0))
    assert portfolio_events[1] == File83b(0, 25_000)
    assert portfolio_events[2] == Vest(2, 25_000)
    assert portfolio_events[3] == Sell(3, 25_000)


def test_get_tax_events_file_83b_with_purchase(
        portfolio_event_data_with_purchase,
        tax_event_data):
    portfolio_events = get_portfolio_events(
        True, portfolio_event_data_with_purchase)
    tax_events = get_tax_events(
        portfolio_events,
        portfolio_event_data_with_purchase.employee_purchase,
        tax_event_data)
    assert len(tax_events) == 2
    assert tax_events[0] == IncomeTax(0, 0, 0, 0.37)
    assert tax_events[1] == CapitalGains(
        3, 35_000, 7_000, [Lot(0, 1, 25_000)], 0.20)
