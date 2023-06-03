from src.events.portfolio_event import PortfolioEvent, PortfolioEventType, get_portfolio_events
from src.events.tax_event import TaxEvent, TaxType, get_tax_events


# https://www.irs.gov/irb/2012-28_IRB#RP-2012-29
# Example (4)

def test_get_portfolio_events_file_83b(portfolio_event_data):
    portfolio_events = get_portfolio_events(
        True, portfolio_event_data)
    assert len(portfolio_events) == 4
    assert portfolio_events[0] == PortfolioEvent(
        0, PortfolioEventType.GRANT, 25_000)
    assert portfolio_events[1] == PortfolioEvent(
        0, PortfolioEventType.FILE_83B, 25_000)
    assert portfolio_events[2] == PortfolioEvent(
        2, PortfolioEventType.VEST, 25_000)
    assert portfolio_events[3] == PortfolioEvent(
        3, PortfolioEventType.SALE, 25_000)


def test_get_tax_events_file_83b(
        portfolio_event_data,
        tax_event_data):
    portfolio_events = get_portfolio_events(
        True, portfolio_event_data)
    tax_events = get_tax_events(
        portfolio_events,
        portfolio_event_data.employee_purchase,
        tax_event_data)
    assert len(tax_events) == 2
    assert tax_events[0] == TaxEvent(
        0, 25_000, TaxType.INCOME, 9_250)
    assert tax_events[1] == TaxEvent(
        3, 35_000, TaxType.CAPITAL_GAINS_LONG_TERM, 7_000)