from events.vesting_event import VestingEvent
from events.tax_event import TaxEvent, TaxType
from state.portfolio import Portfolio
from state.lot import Lot


def run_scenario(
        marginal_income_tax_rate, marginal_long_term_capital_gains_rate, vesting_schedule, share_price_process):
    yes_83b_tax_events = run_83b_scenario(
        marginal_income_tax_rate, marginal_long_term_capital_gains_rate, vesting_schedule, share_price_process)
    no_83b_tax_events = run_no_83b_scenario(
        marginal_income_tax_rate, marginal_long_term_capital_gains_rate, vesting_schedule, share_price_process)
    tax_diff_process = get_tax_diff_process(
        len(share_price_process), yes_83b_tax_events, no_83b_tax_events)
    return tax_diff_process


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
    return no_83b_tax_event.tax_amount - yes_83b_tax_event.tax_amount


def get_tax_event(time_idx, tax_events):
    for tax_event in tax_events:
        if tax_event.time_idx == time_idx:
            return tax_event
    return TaxEvent(time_idx, TaxType.PLACEHOLDER, 0.0)


def run_83b_scenario(
        marginal_income_tax_rate, marginal_long_term_capital_gains_rate, vesting_schedule, share_price_process):
    vesting_events, tax_events, lots = get_83b_events_and_lots(
        marginal_income_tax_rate, vesting_schedule, share_price_process)
    capital_gains_tax_event = liquidate_portfolio(
        marginal_long_term_capital_gains_rate, len(share_price_process) - 1, lots)
    tax_events.append(capital_gains_tax_event)
    return tax_events


def get_83b_events_and_lots(marginal_income_tax_rate, vesting_schedule, share_price_process):
    vesting_events = []
    tax_events = []
    lots = []
    for idx, count_vesting_shares in enumerate(vesting_schedule):
        price_per_share = share_price_process[0]
        if idx == 0:
            total_share_grant = sum(vesting_schedule)
            income_tax = round(1.0 * total_share_grant *
                               price_per_share * marginal_income_tax_rate, 2)
            income_tax_event = TaxEvent(idx, TaxType.INCOME, income_tax)
            tax_events.append(income_tax_event)
        elif count_vesting_shares > 0:
            vesting_event = VestingEvent(idx, count_vesting_shares)
            vesting_events.append(vesting_event)
            lot = Lot(idx, count_vesting_shares, price_per_share)
            lots.append(lot)
    return vesting_events, tax_events, lots


def run_no_83b_scenario(
        marginal_income_tax_rate, marginal_long_term_capital_gains_rate, vesting_schedule, share_price_process):
    vesting_events, tax_events, lots = get_no_83b_events_and_lots(
        marginal_income_tax_rate, vesting_schedule, share_price_process)
    capital_gains_tax_event = liquidate_portfolio(
        marginal_long_term_capital_gains_rate, len(share_price_process) - 1, lots)
    tax_events.append(capital_gains_tax_event)
    return tax_events


def get_no_83b_events_and_lots(marginal_income_tax_rate, vesting_schedule, share_price_process):
    vesting_events = []
    tax_events = []
    lots = []
    for idx, count_vesting_shares in enumerate(vesting_schedule):
        if count_vesting_shares > 0:
            vesting_event = VestingEvent(idx, count_vesting_shares)
            vesting_events.append(vesting_event)

            price_per_share = share_price_process[idx]
            income_tax = round(1.0 * count_vesting_shares *
                               price_per_share * marginal_income_tax_rate, 2)
            income_tax_event = TaxEvent(idx, TaxType.INCOME, income_tax)
            tax_events.append(income_tax_event)

            lot = Lot(idx, count_vesting_shares, price_per_share)
            lots.append(lot)
    return vesting_events, tax_events, lots


def get_portfolio(lots, last_share_price):
    portfolio_basis = 0
    portfolio_value = 0
    for idx, lot in enumerate(lots):
        portfolio_basis += lot.share_count * lot.basis_per_share
        portfolio_value += lot.share_count * last_share_price
    return portfolio_value, portfolio_basis


def liquidate_portfolio(marginal_long_term_capital_gains_rate, liquidate_time_idx, lots):
    portfolio_value, portfolio_basis = get_portfolio(lots, liquidate_time_idx)
    capital_gains_tax = round(
        1.0 * (portfolio_value - portfolio_basis) * marginal_long_term_capital_gains_rate, 2)
    capital_gains_tax_event = TaxEvent(
        liquidate_time_idx, TaxType.CAPITAL_GAINS_LONG_TERM, capital_gains_tax)
    return capital_gains_tax_event
