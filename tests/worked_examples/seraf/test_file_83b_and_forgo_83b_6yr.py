from src.domain.portfolio_event import Grant, File83b, Vest
from src.domain.scenario import PortfolioEventData, TaxEventData, Metadata
from src.domain.purchase import EmployeePurchase
from src.domain.tax_event import IncomeTax
from src.domain.lot import Lot, get_portfolio_lots
from src.events.portfolio_event import get_portfolio_events
from src.events.tax_event import get_tax_events
from src.execute.scenario_runner import run_scenario

# https://seraf-investor.com/compass/article/seraf-toolbox-dealing-restricted-stock-model-irs-83b-election-form

portfolio_event_data = PortfolioEventData(
    [0,	25_000, 25_000, 25_000, 25_000],
    -1,
    EmployeePurchase(0, 0.0),
    -1
)

tax_event_data = TaxEventData(
    0.396,
    0.20,
    [0.05, 0.10, 0.15, 0.20, 0.25]
)

metadata = Metadata(discount_rate=0.06)


def test_get_portfolio_events_file_83b():
    portfolio_events = get_portfolio_events(
        True, portfolio_event_data)
    assert len(portfolio_events) == 6
    assert portfolio_events[0] == Grant(0, 100_000, EmployeePurchase(0, 0.0))
    assert portfolio_events[1] == File83b(0, 100_000)
    assert portfolio_events[2] == Vest(1, 25_000)
    assert portfolio_events[3] == Vest(2, 25_000)
    assert portfolio_events[4] == Vest(3, 25_000)
    assert portfolio_events[5] == Vest(4, 25_000)


def test_get_lots_file_83b():
    portfolio_events = get_portfolio_events(
        True, portfolio_event_data)
    portfolio_lots = get_portfolio_lots(
        True, portfolio_events, tax_event_data.share_price_process
    )
    assert len(portfolio_lots) == 1
    assert portfolio_lots[0] == Lot(0, 0.05, 100_000)


def test_get_tax_events_file_83b():
    portfolio_events = get_portfolio_events(
        True, portfolio_event_data)
    tax_events = get_tax_events(
        portfolio_events,
        portfolio_event_data.employee_purchase,
        tax_event_data)
    assert len(tax_events) == 1
    assert tax_events[0] == IncomeTax(0, 5_000, 1_980, 0.396)


def test_get_portfolio_events_forgo_83b():
    portfolio_events = get_portfolio_events(
        False, portfolio_event_data)
    assert len(portfolio_events) == 5
    assert portfolio_events[0] == Grant(0, 100_000, EmployeePurchase(0, 0.0))
    assert portfolio_events[1] == Vest(1, 25_000)
    assert portfolio_events[2] == Vest(2, 25_000)
    assert portfolio_events[3] == Vest(3, 25_000)
    assert portfolio_events[4] == Vest(4, 25_000)


def test_get_lots_forgo_83b():
    portfolio_events = get_portfolio_events(
        False, portfolio_event_data)
    portfolio_lots = get_portfolio_lots(
        False, portfolio_events, tax_event_data.share_price_process
    )
    assert len(portfolio_lots) == 4
    assert portfolio_lots[0] == Lot(1, 0.10, 25_000)
    assert portfolio_lots[1] == Lot(2, 0.15, 25_000)
    assert portfolio_lots[2] == Lot(3, 0.20, 25_000)
    assert portfolio_lots[3] == Lot(4, 0.25, 25_000)


def test_get_tax_events_forgo_83b():
    portfolio_events = get_portfolio_events(
        False, portfolio_event_data)
    tax_events = get_tax_events(
        portfolio_events,
        portfolio_event_data.employee_purchase,
        tax_event_data)
    assert len(tax_events) == 4
    assert tax_events[0] == IncomeTax(1, 25_000 * 0.10, 990, 0.396)
    assert tax_events[1] == IncomeTax(2, 25_000 * 0.15, 1_485, 0.396)
    assert tax_events[2] == IncomeTax(3, 25_000 * 0.20, 1_980, 0.396)
    assert tax_events[3] == IncomeTax(4, 25_000 * 0.25, 2_475, 0.396)


def test_value_of_83b():
    scenario_result = run_scenario(
        portfolio_event_data,
        tax_event_data,
        metadata)
    assert scenario_result.raw == 4_950.0
    assert scenario_result.npv == 3_898.48
