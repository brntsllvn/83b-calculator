from dataclasses import dataclass

import numpy_financial as npf

from src.events.portfolio_event import PortfolioEvent, PortfolioEventType, get_portfolio_events
from src.events.tax_event import TaxEvent, TaxType, get_tax_events, get_tax_diff_process
from src.events.employment_event import EmploymentType


def run_scenario(portfolio_event_data, tax_event_data, metadata):
    file_83b_events = get_portfolio_events(True, portfolio_event_data)
    print(*file_83b_events, sep="\n", end="\n")

    file_83b_tax_events = get_tax_events(
        file_83b_events,
        portfolio_event_data.employee_purchase,
        tax_event_data
    )
    print(*file_83b_tax_events, sep="\n", end="\n")

    forgo_83b_result = get_portfolio_events(False, portfolio_event_data)
    print(*forgo_83b_result, sep="\n", end="\n")

    forgo_83b_tax_events = get_tax_events(
        forgo_83b_result,
        portfolio_event_data.employee_purchase,
        tax_event_data
    )
    print(*forgo_83b_tax_events, sep="\n", end="\n")

    tax_diff_process = get_tax_diff_process(
        len(tax_event_data.share_price_process),
        file_83b_tax_events,
        forgo_83b_tax_events)
    raw = sum(tax_diff_process)
    print(raw)

    npv = get_npv(tax_diff_process, metadata.discount_rate)
    print(npv)


def get_npv(tax_diff_process, discount_rate):
    npv = round(npf.npv(discount_rate, tax_diff_process), 2)
    return npv
