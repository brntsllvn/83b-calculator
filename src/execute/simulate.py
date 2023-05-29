from dataclasses import dataclass

import numpy_financial as npf

from src.events.share_event import PortfolioEvent, PortfolioEventType
from src.events.tax_event import TaxEvent, TaxType
from src.state.lot import Lot
from src.events.employment_event import EmploymentType
from src.execute.cases.yes_83b import execute_yes_83b
from src.execute.cases.no_83b import execute_no_83b
from src.execute.shared import CaseResult, run_case


@dataclass
class ScenarioMetadata:
    marginal_income_tax_rate: float
    marginal_long_term_capital_gains_rate: float
    discount_rate: float


@dataclass
class EmployeePurchase:
    price_per_share: float
    share_count: int


@dataclass
class Scenario:
    vesting_schedule: [int]
    share_price_process: [float]
    employment_process: [EmploymentType]
    employee_purchase: EmployeePurchase = EmployeePurchase(0, 0,)


@dataclass
class Election83bValue:
    tax_diff_process: [float]
    raw_dollars: float
    npv_dollars: float


@dataclass
class ScenarioResult:
    no_83b_result: CaseResult
    yes_83b_result: CaseResult
    election_83b_value: Election83bValue

# TODO: implement employment process


def run_scenario(scenario, metadata):
    yes_83b_case_result = run_case(
        metadata.marginal_income_tax_rate,
        metadata.marginal_long_term_capital_gains_rate,
        scenario.employee_purchase,
        scenario.vesting_schedule,
        scenario.share_price_process,
        scenario.employment_process,
        execute_yes_83b
    )
    no_83b_case_result = run_case(
        metadata.marginal_income_tax_rate,
        metadata.marginal_long_term_capital_gains_rate,
        scenario.employee_purchase,
        scenario.vesting_schedule,
        scenario.share_price_process,
        scenario.employment_process,
        execute_no_83b
    )
    tax_diff_process = get_tax_diff_process(
        len(scenario.share_price_process),
        yes_83b_case_result.tax_events,
        no_83b_case_result.tax_events)
    raw = sum(tax_diff_process)
    npv = get_npv(tax_diff_process, metadata.discount_rate)
    election_83b_value = Election83bValue(tax_diff_process, raw, npv)
    scenario_result = ScenarioResult(
        no_83b_case_result,
        yes_83b_case_result,
        election_83b_value)
    return scenario_result


def get_npv(tax_diff_process, discount_rate):
    npv = round(npf.npv(discount_rate, tax_diff_process), 2)
    return npv


def get_tax_diff_process(number_of_events, yes_83b_tax_events, no_83b_tax_events):
    tax_diff_process = []
    for idx in range(0, number_of_events):
        tax_diff = subtract_tax_events(
            idx, yes_83b_tax_events, no_83b_tax_events)
        tax_diff_process.append(tax_diff)
    return tax_diff_process


def subtract_tax_events(time_idx, yes_83b_tax_events, no_83b_tax_events):
    yes_83b_tax_event = find_tax_event_by_id(time_idx, yes_83b_tax_events)
    no_83b_tax_event = find_tax_event_by_id(time_idx, no_83b_tax_events)
    return no_83b_tax_event.tax_dollars - yes_83b_tax_event.tax_dollars


def find_tax_event_by_id(time_idx, tax_events):
    for tax_event in tax_events:
        if tax_event.time_idx == time_idx:
            return tax_event
    return TaxEvent(time_idx, 0.0, TaxType.ZERO, 0.0)
