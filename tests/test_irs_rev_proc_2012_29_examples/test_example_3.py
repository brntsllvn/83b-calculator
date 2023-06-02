from src.events.portfolio_event import PortfolioEvent, PortfolioEventType, get_portfolio_events
from src.events.tax_event import TaxEvent, TaxType, get_tax_events

# https://www.irs.gov/irb/2012-28_IRB#RP-2012-29
# Example (3)


def test_get_portfolio_events_file_83b_with_purchase_and_termination(
        purchase_portfolio_event_data_with_termination):
    portfolio_events = get_portfolio_events(
        True, purchase_portfolio_event_data_with_termination)
    assert len(portfolio_events) == 4
    assert portfolio_events[0] == PortfolioEvent(
        0, PortfolioEventType.GRANT, 25_000)
    assert portfolio_events[1] == PortfolioEvent(
        0, PortfolioEventType.PURCHASE, 25_000)
    assert portfolio_events[2] == PortfolioEvent(
        0, PortfolioEventType.FILE_83B, 25_000)
    assert portfolio_events[3] == PortfolioEvent(
        1, PortfolioEventType.REPURCHASE, 25_000)


def test_get_tax_events_file_83b_with_purchase_and_termination(
        purchase_portfolio_event_data_with_termination,
        tax_event_data):
    portfolio_events = get_portfolio_events(
        True, purchase_portfolio_event_data_with_termination)
    tax_events = get_tax_events(
        portfolio_events,
        purchase_portfolio_event_data_with_termination.employee_purchase,
        tax_event_data)
    assert len(tax_events) == 0
