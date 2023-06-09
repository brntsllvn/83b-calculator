from src.domain.portfolio_event import Grant, File83b, Vest, Sell
from src.domain.scenario import PortfolioEventData, TaxEventData, Metadata
from src.domain.purchase import EmployeePurchase
from src.domain.tax_event import IncomeTax, CapitalGains
from src.domain.lot import Lot
from src.events.portfolio_event import get_portfolio_events
from src.events.tax_event import get_tax_events
# from src.execute.scenario_runner import run_scenario

# https://stripe.com/docs/atlas/83b-election
portfolio_event_data = PortfolioEventData(
    [0,	100_000, 100_000, 0],
    -1,
    EmployeePurchase(200_000, 0.0001),
    3
)

tax_event_data = TaxEventData(
    0.37,
    0.20,
    [0.0001, 0.50, 1.00, 2.00]
)

metadata = Metadata(discount_rate=0.06)


def test_get_portfolio_events_file_83b_with_purchase():
    portfolio_events = get_portfolio_events(
        True, portfolio_event_data)
    assert len(portfolio_events) == 5
    assert portfolio_events[0] == Grant(
        0, 200_000, EmployeePurchase(200_000, 0.0001))
    assert portfolio_events[1] == File83b(0, 200_000)
    assert portfolio_events[2] == Vest(1, 100_000)
    assert portfolio_events[3] == Vest(2, 100_000)
    assert portfolio_events[4] == Sell(3, 200_000)


# def test_get_portfolio_lots_file_83b_with_purchase():
#     portfolio_events = get_portfolio_events(
#         True, portfolio_event_data)
#     portfolio_lots =
#     lots = get_portfolio_lots
#     portfolio_lots = portfolio_events[4].portfolio_lots
#     assert len(portfolio_lots) == 1
#     assert portfolio_lots[0] == Lot(0, 0.0001, 200_000)

def test_get_tax_events_file_83b_with_purchase():
    portfolio_events = get_portfolio_events(
        True, portfolio_event_data)
    tax_events = get_tax_events(
        portfolio_events,
        portfolio_event_data.employee_purchase,
        tax_event_data)
    assert len(tax_events) == 2
    assert tax_events[0] == IncomeTax(0, 0, 0, 0.37)
    assert tax_events[1] == CapitalGains(
        3, 200_000 * 2 - 20, 79_996, [Lot(0, 0.0001, 200_000)], 0.20)


def test_get_portfolio_events_forgo_83b_with_purchase():
    portfolio_events = get_portfolio_events(
        False, portfolio_event_data)
    assert len(portfolio_events) == 4
    assert portfolio_events[0] == Grant(
        0, 200_000, EmployeePurchase(200_000, 0.0001))
    assert portfolio_events[1] == Vest(1, 100_000)
    assert portfolio_events[2] == Vest(2, 100_000)
    assert portfolio_events[3] == Sell(3, 200_000)


def test_get_tax_events_forgo_83b_with_purchase():
    portfolio_events = get_portfolio_events(
        False, portfolio_event_data)
    tax_events = get_tax_events(
        portfolio_events,
        portfolio_event_data.employee_purchase,
        tax_event_data)
    assert len(tax_events) == 3
    assert tax_events[0] == IncomeTax(1, 49_990, 49_990 * 0.37, 0.37)
    assert tax_events[1] == IncomeTax(2, 99_990, 99_990 * 0.37, 0.37)
    assert tax_events[2] == CapitalGains(
        3, 250_000, 50_000, [
            Lot(1, 0.50, 100_000),
            Lot(2, 1.00, 100_000)
        ], 0.20)


# def test_value_of_83b():
#     scenario_result = run_scenario(
#         portfolio_event_data,
#         tax_event_data,
#         metadata)
#     assert scenario_result.raw == 25_496.60
#     assert scenario_result.npv == 3_898.48
