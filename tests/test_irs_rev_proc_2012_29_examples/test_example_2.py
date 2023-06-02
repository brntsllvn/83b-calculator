from src.execute.scenario import PortfolioEventData
from src.events.employment_event import EmployeePurchase
from src.events.portfolio_event import PortfolioEvent, PortfolioEventType, get_portfolio_events
from src.events.tax_event import TaxEvent, TaxType, get_tax_events
from src.execute.scenario import TaxEventData

portfolio_event_data_examples_2 = PortfolioEventData(
    vesting_schedule=[0, 0, 25_000, 0],
    termination_idx=-1,
    employee_purchase=EmployeePurchase(1, 25_000)
)

tax_event_data_examples_2 = TaxEventData(
    marginal_income_tax_rate=0.37,
    marginal_long_term_capital_gains_rate=0.20,
    share_price_process=[1, 1, 1.6, 2.4],
)

# https://www.irs.gov/irb/2012-28_IRB#RP-2012-29
# Example (2)


def test_get_portfolio_events_forgo_83b_with_purchase():
    portfolio_events = get_portfolio_events(
        False, portfolio_event_data_examples_2)
    assert len(portfolio_events) == 4
    assert portfolio_events[0] == PortfolioEvent(
        0, PortfolioEventType.GRANT, 25_000)
    assert portfolio_events[1] == PortfolioEvent(
        0, PortfolioEventType.PURCHASE, 25_000)
    assert portfolio_events[2] == PortfolioEvent(
        2, PortfolioEventType.VEST, 25_000)
    assert portfolio_events[3] == PortfolioEvent(
        3, PortfolioEventType.SALE, 25_000)


def test_get_tax_events_forgo_83b_with_purchase():
    portfolio_events = get_portfolio_events(
        False, portfolio_event_data_examples_2)
    tax_events = get_tax_events(
        portfolio_events,
        portfolio_event_data_examples_2.employee_purchase,
        tax_event_data_examples_2)
    assert len(tax_events) == 2
    assert tax_events[0] == TaxEvent(
        2, 15_000, TaxType.INCOME, 5_550)
    assert tax_events[1] == TaxEvent(
        3, 20_000, TaxType.CAPITAL_GAINS_LONG_TERM, 4_000)
