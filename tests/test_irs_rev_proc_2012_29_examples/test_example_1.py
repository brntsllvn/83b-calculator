from src.domain.portfolio_event import Grant, File83b, Vest, Sell
from src.domain.purchase import EmployeePurchase, EmployerPurchase
from src.events.portfolio_event import get_portfolio_events
from src.events.tax_event import TaxEvent, TaxType, get_tax_events

# https://www.irs.gov/irb/2012-28_IRB#RP-2012-29
# Example (1)


def test_get_portfolio_events_file_83b_with_purchase(portfolio_event_data_with_purchase):
    portfolio_events = get_portfolio_events(
        True, portfolio_event_data_with_purchase)
    assert len(portfolio_events) == 4
    assert portfolio_events[0] == Grant(0, 25_000, EmployeePurchase(25_000, 1))
    assert portfolio_events[1] == File83b(0, 25_000)
    assert portfolio_events[2] == Vest(2, 25_000)
    assert portfolio_events[3] == Sell(3, 25_000, EmployerPurchase(0, 0))


def test_get_tax_events_file_83b_with_purchase(
        portfolio_event_data_with_purchase,
        tax_event_data):
    portfolio_events = get_portfolio_events(
        True, portfolio_event_data_with_purchase)
    tax_events = get_tax_events(
        portfolio_events,
        portfolio_event_data_with_purchase.employee_purchase,
        tax_event_data)
    assert len(tax_events) == 1
    assert tax_events[0] == TaxEvent(
        3, 35_000, TaxType.CAPITAL_GAINS_LONG_TERM, 7_000)
