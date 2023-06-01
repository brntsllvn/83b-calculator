from src.execute.scenario import PortfolioEventData
from src.events.employment_event import EmployeePurchase
from src.events.portfolio_event import PortfolioEvent, PortfolioEventType, get_portfolio_events


portfolio_event_data_examples_1_2 = PortfolioEventData(
    vesting_schedule=[0, 0, 25_000, 0],
    termination_idx=-1,
    employee_purchase=EmployeePurchase(1, 25_000)
)


# https://www.irs.gov/irb/2012-28_IRB#RP-2012-29
# Example (1)
def test_get_portfolio_events_file_83b_with_purchase():
    portfolio_events = get_portfolio_events(
        True, portfolio_event_data_examples_1_2)
    assert len(portfolio_events) == 5
    assert portfolio_events[0] == PortfolioEvent(
        0, PortfolioEventType.GRANT, 25_000)
    assert portfolio_events[1] == PortfolioEvent(
        0, PortfolioEventType.PURCHASE, 25_000)
    assert portfolio_events[2] == PortfolioEvent(
        0, PortfolioEventType.FILE_83B, 25_000)
    assert portfolio_events[3] == PortfolioEvent(
        2, PortfolioEventType.VEST, 25_000)
    assert portfolio_events[4] == PortfolioEvent(
        3, PortfolioEventType.SALE, 25_000)


# https://www.irs.gov/irb/2012-28_IRB#RP-2012-29
# Example (2)
def test_get_portfolio_events_forgo_83b_with_purchase():
    portfolio_events = get_portfolio_events(
        False, portfolio_event_data_examples_1_2)
    assert len(portfolio_events) == 4
    assert portfolio_events[0] == PortfolioEvent(
        0, PortfolioEventType.GRANT, 25_000)
    assert portfolio_events[1] == PortfolioEvent(
        0, PortfolioEventType.PURCHASE, 25_000)
    assert portfolio_events[2] == PortfolioEvent(
        2, PortfolioEventType.VEST, 25_000)
    assert portfolio_events[3] == PortfolioEvent(
        3, PortfolioEventType.SALE, 25_000)


# https://www.irs.gov/irb/2012-28_IRB#RP-2012-29
# Example (3)
def test_get_portfolio_events_file_83b_with_purchase_and_termination():
    portfolio_event_data_example_3 = PortfolioEventData(
        vesting_schedule=[0, 0, 25_000, 0],
        termination_idx=1,
        employee_purchase=EmployeePurchase(1, 25_000)
    )
    portfolio_events = get_portfolio_events(
        True, portfolio_event_data_example_3)
    assert len(portfolio_events) == 4
    assert portfolio_events[0] == PortfolioEvent(
        0, PortfolioEventType.GRANT, 25_000)
    assert portfolio_events[1] == PortfolioEvent(
        0, PortfolioEventType.PURCHASE, 25_000)
    assert portfolio_events[2] == PortfolioEvent(
        0, PortfolioEventType.FILE_83B, 25_000)
    assert portfolio_events[3] == PortfolioEvent(
        1, PortfolioEventType.REPURCHASE, 25_000)


portfolio_event_data_examples_4_5 = PortfolioEventData(
    vesting_schedule=[0, 0, 25_000, 0],
    termination_idx=-1,
    employee_purchase=None
)


# https://www.irs.gov/irb/2012-28_IRB#RP-2012-29
# Example (4)
def test_get_portfolio_events_file_83b():
    portfolio_events = get_portfolio_events(
        True, portfolio_event_data_examples_4_5)
    assert len(portfolio_events) == 4
    assert portfolio_events[0] == PortfolioEvent(
        0, PortfolioEventType.GRANT, 25_000)
    assert portfolio_events[1] == PortfolioEvent(
        0, PortfolioEventType.FILE_83B, 25_000)
    assert portfolio_events[2] == PortfolioEvent(
        2, PortfolioEventType.VEST, 25_000)
    assert portfolio_events[3] == PortfolioEvent(
        3, PortfolioEventType.SALE, 25_000)


# https://www.irs.gov/irb/2012-28_IRB#RP-2012-29
# Example (5)
def test_get_portfolio_events_forgo_83b():
    portfolio_events = get_portfolio_events(
        False, portfolio_event_data_examples_4_5)
    assert len(portfolio_events) == 3
    assert portfolio_events[0] == PortfolioEvent(
        0, PortfolioEventType.GRANT, 25_000)
    assert portfolio_events[1] == PortfolioEvent(
        2, PortfolioEventType.VEST, 25_000)
    assert portfolio_events[2] == PortfolioEvent(
        3, PortfolioEventType.SALE, 25_000)


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
