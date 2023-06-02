from src.execute.scenario import PortfolioEventData
from src.events.employment_event import EmployeePurchase
from src.events.portfolio_event import PortfolioEvent, PortfolioEventType, get_portfolio_events
from src.execute.scenario import TaxEventData

portfolio_event_data_examples_5 = PortfolioEventData(
    vesting_schedule=[0, 0, 25_000, 0],
    termination_idx=-1,
    employee_purchase=None
)


# https://www.irs.gov/irb/2012-28_IRB#RP-2012-29
# Example (5)
def test_get_portfolio_events_forgo_83b():
    portfolio_events = get_portfolio_events(
        False, portfolio_event_data_examples_5)
    assert len(portfolio_events) == 3
    assert portfolio_events[0] == PortfolioEvent(
        0, PortfolioEventType.GRANT, 25_000)
    assert portfolio_events[1] == PortfolioEvent(
        2, PortfolioEventType.VEST, 25_000)
    assert portfolio_events[2] == PortfolioEvent(
        3, PortfolioEventType.SALE, 25_000)
