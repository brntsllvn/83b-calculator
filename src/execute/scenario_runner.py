from src.events.portfolio_event import PortfolioEvent, PortfolioEventType, get_portfolio_events
from src.events.tax_event import TaxEvent, TaxType, get_tax_events, get_tax_diff_process
from src.execute.analytics import get_npv


def run_scenario(portfolio_event_data, tax_event_data, metadata):
    file_83b_tax_events = run_case(
        True, portfolio_event_data, tax_event_data)
    forgo_83b_tax_events = run_case(
        False, portfolio_event_data, tax_event_data)
    tax_diff_process = get_tax_diff_process(
        len(tax_event_data.share_price_process),
        file_83b_tax_events,
        forgo_83b_tax_events)
    raw = sum(tax_diff_process)
    print(raw)
    npv = get_npv(tax_diff_process, metadata.discount_rate)
    print(npv)


def run_case(file_83b_election, portfolio_event_data, tax_event_data):
    case_portfolio_events = get_portfolio_events(
        file_83b_election, portfolio_event_data)
    print(*case_portfolio_events, sep="\n", end="\n")

    case_tax_events = get_tax_events(
        case_portfolio_events,
        portfolio_event_data.employee_purchase,
        tax_event_data
    )
    print(*case_tax_events, sep="\n", end="\n")
    return case_tax_events
