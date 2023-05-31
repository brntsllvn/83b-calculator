from dataclasses import dataclass

import numpy_financial as npf

from src.events.portfolio_event import PortfolioEvent, PortfolioEventType, get_portfolio_events
from src.events.tax_event import TaxEvent, TaxType, get_tax_events, get_tax_diff_process
from src.events.employment_event import EmploymentType


def run_scenario(scenario, metadata):
    file_83b_events = get_portfolio_events(
        True,
        scenario.share_price_process,
        scenario.vesting_schedule,
        scenario.employment_process,
        scenario.employee_purchase,
    )
    print(*file_83b_events, sep="\n", end="\n")
    file_83b_tax_events = get_tax_events(
        file_83b_events,
        scenario.share_price_process,
        scenario.employee_purchase,
        metadata.marginal_income_tax_rate,
        metadata.marginal_long_term_capital_gains_rate
    )
    print(*file_83b_tax_events, sep="\n", end="\n")

    forgo_83b_result = get_portfolio_events(
        False,
        scenario.share_price_process,
        scenario.vesting_schedule,
        scenario.employment_process,
        scenario.employee_purchase
    )
    print(*forgo_83b_result, sep="\n", end="\n")
    forgo_83b_tax_events = get_tax_events(
        forgo_83b_result,
        scenario.share_price_process,
        scenario.employee_purchase,
        metadata.marginal_income_tax_rate,
        metadata.marginal_long_term_capital_gains_rate
    )
    print(*forgo_83b_tax_events, sep="\n", end="\n")

    tax_diff_process = get_tax_diff_process(
        len(scenario.share_price_process),
        file_83b_tax_events,
        forgo_83b_tax_events)
    raw = sum(tax_diff_process)
    print(raw)

    npv = get_npv(tax_diff_process, metadata.discount_rate)
    print(npv)


def get_npv(tax_diff_process, discount_rate):
    npv = round(npf.npv(discount_rate, tax_diff_process), 2)
    return npv
