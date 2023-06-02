from src.execute.scenario import PortfolioEventData
from src.events.employment_event import EmployeePurchase
from src.events.portfolio_event import PortfolioEvent, PortfolioEventType, get_portfolio_events
from src.execute.scenario import TaxEventData

# https://www.irs.gov/irb/2012-28_IRB#RP-2012-29
# Example (6)


def test_get_portfolio_events_file_83b_with_termination():
    portfolio_event_data_example_6 = PortfolioEventData(
        vesting_schedule=[0, 0, 25_000, 0],
        termination_idx=1,
        employee_purchase=None
    )
    portfolio_events = get_portfolio_events(
        True, portfolio_event_data_example_6)
    assert len(portfolio_events) == 3
    assert portfolio_events[0] == PortfolioEvent(
        0, PortfolioEventType.GRANT, 25_000)
    assert portfolio_events[1] == PortfolioEvent(
        0, PortfolioEventType.FILE_83B, 25_000)
    assert portfolio_events[2] == PortfolioEvent(
        1, PortfolioEventType.REPURCHASE, 25_000)
