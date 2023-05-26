from dataclasses import dataclass

import numpy_financial as npf

from src.events.share_event import ShareEvent, ShareEventType
from src.events.tax_event import TaxEvent, TaxType
from src.state.portfolio import Portfolio
from src.state.lot import Lot
from src.events.employment_event import EmploymentType


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
class EventsLots:
    share_events: [ShareEvent]
    lots: [Lot]
    tax_events: [TaxEvent]


@dataclass
class ScenarioResult:
    no_83b_events_and_lots: EventsLots
    yes_83b_events_and_lots: EventsLots
    election_83b_value: Election83bValue

# TODO: implement employment process


def run_scenario(scenario, metadata):
    yes_83b_scenario_result = run_83b_scenario(
        metadata.marginal_income_tax_rate,
        metadata.marginal_long_term_capital_gains_rate,
        scenario.employee_purchase,
        scenario.vesting_schedule,
        scenario.share_price_process)
    no_83b_scenario_result = run_no_83b_scenario(
        metadata.marginal_income_tax_rate,
        metadata.marginal_long_term_capital_gains_rate,
        scenario.employee_purchase,
        scenario.vesting_schedule,
        scenario.share_price_process)
    tax_diff_process = get_tax_diff_process(
        len(scenario.share_price_process),
        yes_83b_scenario_result.tax_events,
        no_83b_scenario_result.tax_events)
    raw = sum(tax_diff_process)
    npv = get_npv(tax_diff_process, metadata.discount_rate)
    election_83b_value = Election83bValue(tax_diff_process, raw, npv)
    scenario_result = ScenarioResult(
        no_83b_scenario_result,
        yes_83b_scenario_result,
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
    yes_83b_tax_event = get_tax_event(time_idx, yes_83b_tax_events)
    no_83b_tax_event = get_tax_event(time_idx, no_83b_tax_events)
    return no_83b_tax_event.tax_dollars - yes_83b_tax_event.tax_dollars


def get_tax_event(time_idx, tax_events):
    for tax_event in tax_events:
        if tax_event.time_idx == time_idx:
            return tax_event
    return TaxEvent(time_idx, 0.0, TaxType.ZERO, 0.0)


def run_83b_scenario(
        marginal_income_tax_rate,
        marginal_long_term_capital_gains_rate,
        employee_purchase,
        vesting_schedule,
        share_price_process):
    vesting_events, tax_events, lots = get_83b_events_and_lots(
        marginal_income_tax_rate,
        employee_purchase,
        vesting_schedule,
        share_price_process)
    if len(lots) != 0:
        capital_gains_tax_event = simulate_portfolio_liquidation(
            marginal_long_term_capital_gains_rate,
            share_price_process,
            lots)
        tax_events.append(capital_gains_tax_event)
    scenario_result = EventsLots(vesting_events, lots, tax_events)
    return scenario_result


def get_83b_events_and_lots(marginal_income_tax_rate,
                            employee_purchase,
                            vesting_schedule,
                            share_price_process):
    vesting_events = []
    tax_events = []
    lots = []
    for idx, count_vesting_shares in enumerate(vesting_schedule):
        share_grant_count = sum(vesting_schedule)
        basis_per_share = share_price_process[0]
        if idx == 0:
            employee_purchase_price = \
                employee_purchase.price_per_share * employee_purchase.share_count
            fair_market_value = round(
                1.0 * share_grant_count * basis_per_share, 2)
            taxable_income = fair_market_value - employee_purchase_price
            if taxable_income != 0:
                income_tax = round(1.0 * taxable_income *
                                   marginal_income_tax_rate, 2)
                income_tax_event = TaxEvent(
                    idx, taxable_income, TaxType.INCOME, income_tax)
                tax_events.append(income_tax_event)
        elif count_vesting_shares > 0:
            vesting_event = ShareEvent(
                idx,
                ShareEventType.VEST,
                count_vesting_shares,
                share_price_process[idx],
                False)
            vesting_events.append(vesting_event)
            lot = Lot(idx, count_vesting_shares, basis_per_share)
            lots.append(lot)
    return vesting_events, tax_events, lots


def run_no_83b_scenario(
        marginal_income_tax_rate,
        marginal_long_term_capital_gains_rate,
        employee_purchase,
        vesting_schedule,
        share_price_process):
    vesting_events, tax_events, lots = get_no_83b_events_and_lots(
        marginal_income_tax_rate,
        vesting_schedule,
        employee_purchase,
        share_price_process)
    if len(lots) != 0:
        capital_gains_tax_event = simulate_portfolio_liquidation(
            marginal_long_term_capital_gains_rate,
            share_price_process,
            lots)
        tax_events.append(capital_gains_tax_event)
    scenario_result = EventsLots(vesting_events, lots, tax_events)
    return scenario_result


def get_no_83b_events_and_lots(marginal_income_tax_rate,
                               vesting_schedule,
                               employee_purchase,
                               share_price_process):
    vesting_events = []
    tax_events = []
    lots = []
    for idx, count_vesting_shares in enumerate(vesting_schedule):
        if count_vesting_shares > 0:
            vesting_event = ShareEvent(
                idx,
                ShareEventType.VEST,
                count_vesting_shares,
                share_price_process[idx],
                True)
            vesting_events.append(vesting_event)

            price_per_share = share_price_process[idx]
            fair_market_value = count_vesting_shares * price_per_share
            employee_purchase_price = employee_purchase.price_per_share * \
                employee_purchase.share_count
            taxable_income = fair_market_value - employee_purchase_price
            income_tax = round(1.0 * taxable_income *
                               marginal_income_tax_rate, 2)
            if income_tax != 0:
                income_tax_event = TaxEvent(
                    idx, taxable_income, TaxType.INCOME, income_tax)
                tax_events.append(income_tax_event)

            lot = Lot(idx, count_vesting_shares, price_per_share)
            lots.append(lot)
    return vesting_events, tax_events, lots


def get_portfolio(lots, liquidation_share_price):
    portfolio_basis = 0
    portfolio_value = 0
    for idx, lot in enumerate(lots):
        portfolio_basis += lot.share_count * lot.basis_per_share
        portfolio_value += lot.share_count * liquidation_share_price
    return portfolio_value, portfolio_basis


def simulate_portfolio_liquidation(marginal_long_term_capital_gains_rate,
                                   share_price_process,
                                   lots):
    liquidate_time_idx = len(share_price_process) - 1
    liquidation_share_price = share_price_process[-1]
    portfolio_value, portfolio_basis = get_portfolio(
        lots, liquidation_share_price)
    gain = 1.0 * (portfolio_value - portfolio_basis)
    capital_gains_tax = round(
        1.0 * gain * marginal_long_term_capital_gains_rate, 2)
    capital_gains_tax_event = TaxEvent(
        liquidate_time_idx,
        gain,
        TaxType.CAPITAL_GAINS_LONG_TERM,
        capital_gains_tax)
    return capital_gains_tax_event
