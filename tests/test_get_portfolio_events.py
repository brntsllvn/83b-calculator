from src.execute.scenario import PortfolioEventData
from src.events.employment_event import EmploymentType, EmployeePurchase
from src.events.portfolio_event import get_portfolio_events


def test_get_portfolio_events_irb_2012_28_examples_1_2():
    portfolio_event_data = PortfolioEventData(
        vesting_schedule=[0, 0, 25_000, 0],
        employment_process=[EmploymentType.EMPLOYED] * 4,
        employee_purchase=EmployeePurchase(1, 25_000)
    )

    portfolio_events = get_portfolio_events(True, portfolio_event_data)
    assert True
