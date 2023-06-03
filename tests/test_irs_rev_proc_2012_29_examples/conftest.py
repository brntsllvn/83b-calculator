import pytest

from src.execute.scenario import PortfolioEventData
from src.events.employment_event import EmployeePurchase
from src.execute.scenario import TaxEventData


@pytest.fixture
def purchase_portfolio_event_data():
    return PortfolioEventData(
        vesting_schedule=[0, 0, 25_000, 0],
        termination_idx=-1,
        employee_purchase=EmployeePurchase(1, 25_000)
    )


@pytest.fixture
def purchase_portfolio_event_data_with_termination(
        purchase_portfolio_event_data):
    return PortfolioEventData(
        vesting_schedule=purchase_portfolio_event_data.vesting_schedule,
        termination_idx=1,
        employee_purchase=purchase_portfolio_event_data.employee_purchase
    )


@pytest.fixture
def portfolio_event_data():
    return PortfolioEventData(
        vesting_schedule=[0, 0, 25_000, 0],
        termination_idx=-1,
        employee_purchase=EmployeePurchase(0, 0)
    )


@pytest.fixture
def tax_event_data():
    return TaxEventData(
        marginal_income_tax_rate=0.37,
        marginal_long_term_capital_gains_rate=0.20,
        share_price_process=[1, 1, 1.6, 2.4],
    )

@pytest.fixture
def portfolio_event_data_with_termination(portfolio_event_data):
    return PortfolioEventData(
        vesting_schedule=portfolio_event_data.vesting_schedule,
        termination_idx=1,
        employee_purchase=portfolio_event_data.employee_purchase
    )