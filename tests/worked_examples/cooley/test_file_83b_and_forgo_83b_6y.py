from src.domain.portfolio_event import Grant, File83b, Vest, Sell
from src.domain.scenario import PortfolioEventData, TaxEventData, Metadata
from src.domain.purchase import EmployeePurchase
from src.domain.tax_event import Lot, IncomeTax, CapitalGains
from src.events.portfolio_event import get_portfolio_events
from src.events.tax_event import get_tax_events
from src.execute.scenario_runner import run_scenario

# https://www.cooleygo.com/what-is-a-section-83b-election/
# Example (1)

cooley_portfolio_event_data = PortfolioEventData(
    [0,	25_000,	25_000,	25_000,	25_000,	0],
    -1,
    EmployeePurchase(0, 0)
)

cooley_tax_event_data = TaxEventData(
    0.37,
    0.20,
    [0.01, 0.05, 0.25, 1.25, 2.45, 5.00]
)

metadata = Metadata(discount_rate=0.06)


def test_cooley_get_portfolio_events_file_83b():
    portfolio_events = get_portfolio_events(
        True, cooley_portfolio_event_data)
    assert len(portfolio_events) == 7
    assert portfolio_events[0] == Grant(0, 100_000, EmployeePurchase(0, 0))
    assert portfolio_events[1] == File83b(0, 100_000)
    assert portfolio_events[2] == Vest(1, 25_000)
    assert portfolio_events[3] == Vest(2, 25_000)
    assert portfolio_events[4] == Vest(3, 25_000)
    assert portfolio_events[5] == Vest(4, 25_000)
    assert portfolio_events[6] == Sell(5, 100_000)


def test_cooley_get_tax_events_file_83b():
    portfolio_events = get_portfolio_events(
        True, cooley_portfolio_event_data)
    tax_events = get_tax_events(
        portfolio_events,
        cooley_portfolio_event_data.employee_purchase,
        cooley_tax_event_data)
    assert len(tax_events) == 2
    assert tax_events[0] == IncomeTax(0, 1_000, 370, 0.37)
    assert tax_events[1] == CapitalGains(
        5, 499_000, 99_800, [Lot(0, 0.01, 100_000)], 0.20)


def test_cooley_get_portfolio_events_forgo_83b():
    portfolio_events = get_portfolio_events(
        False, cooley_portfolio_event_data)
    assert len(portfolio_events) == 6
    assert portfolio_events[0] == Grant(0, 100_000, EmployeePurchase(0, 0))
    assert portfolio_events[1] == Vest(1, 25_000)
    assert portfolio_events[2] == Vest(2, 25_000)
    assert portfolio_events[3] == Vest(3, 25_000)
    assert portfolio_events[4] == Vest(4, 25_000)
    assert portfolio_events[5] == Sell(5, 100_000)


def test_cooley_get_tax_events_forgo_83b():
    portfolio_events = get_portfolio_events(
        False, cooley_portfolio_event_data)
    tax_events = get_tax_events(
        portfolio_events,
        cooley_portfolio_event_data.employee_purchase,
        cooley_tax_event_data)
    assert len(tax_events) == 5
    assert tax_events[0] == IncomeTax(1, 1_250, 462.50, 0.37)
    assert tax_events[1] == IncomeTax(2, 6_250, 2_312.50, 0.37)
    assert tax_events[2] == IncomeTax(3, 31_250, 11_562.50, 0.37)
    assert tax_events[3] == IncomeTax(4, 61_250, 22_662.50, 0.37)
    assert tax_events[4] == CapitalGains(
        5, 400_000, 80_000,
        [
            Lot(1, 0.05, 25_000),
            Lot(2, 0.25, 25_000),
            Lot(3, 1.25, 25_000),
            Lot(4, 2.45, 25_000)
        ],
        0.20)


def test_value_of_83b():
    scenario_result = run_scenario(
        cooley_portfolio_event_data,
        cooley_tax_event_data,
        metadata)
    assert scenario_result.raw == 16_830.0
    assert scenario_result.npv == 14_987.65
