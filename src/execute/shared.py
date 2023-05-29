from dataclasses import dataclass

from src.events.share_event import PortfolioEvent, PortfolioEventType
from src.events.tax_event import TaxEvent, TaxType
from src.state.lot import Lot
from src.execute.case_result import CaseResult


def run_case(marginal_income_tax_rate,
             marginal_long_term_capital_gains_rate,
             employee_purchase,
             vesting_schedule,
             share_price_process,
             employment_process,
             case_fn):
    case_result = case_fn(
        marginal_income_tax_rate,
        marginal_long_term_capital_gains_rate,
        employee_purchase,
        vesting_schedule,
        share_price_process,
        employment_process
    )
    if len(case_result.lots) != 0:
        sale_event, capital_gains_tax_event = get_sale_events(
            marginal_long_term_capital_gains_rate,
            share_price_process,
            case_result.lots)
        case_result.share_events.append(sale_event)
        case_result.tax_events.append(capital_gains_tax_event)
    return case_result


def get_portfolio(lots, liquidation_share_price):
    basis = 0
    value = 0
    share_count = 0
    for idx, lot in enumerate(lots):
        basis += lot.share_count * lot.basis_per_share
        value += lot.share_count * liquidation_share_price
        share_count += lot.share_count
    return value, basis, share_count


def get_sale_events(marginal_long_term_capital_gains_rate,
                    share_price_process,
                    lots):
    liquidate_time_idx = len(share_price_process) - 1
    liquidation_share_price = share_price_process[-1]
    portfolio_value, portfolio_basis, portfolio_share_count = \
        get_portfolio(lots, liquidation_share_price)

    sale_event = PortfolioEvent(
        liquidate_time_idx,
        PortfolioEventType.SALE,
        portfolio_share_count,
        liquidation_share_price,
        True
    )

    gain = 1.0 * (portfolio_value - portfolio_basis)
    capital_gains_tax = round(
        1.0 * gain * marginal_long_term_capital_gains_rate, 2)
    capital_gains_tax_event = TaxEvent(
        liquidate_time_idx,
        gain,
        TaxType.CAPITAL_GAINS_LONG_TERM,
        capital_gains_tax)
    return sale_event, capital_gains_tax_event


def get_repurchase_events(
        marginal_long_term_capital_gains_rate,
        repurchase_time_idx,
        share_grant_count,
        current_price_per_share,
        lots,
        employee_purchase):
    # Assume corp buys all shares at lesser of FMV and purchase price
    # TODO: add cases for FMV > purchase, FMV == purchase, FMV < puchase
    fair_market_value, portfolio_basis, portfolio_share_count = get_portfolio(
        lots, current_price_per_share)

    employee_purchase_price = \
        employee_purchase.price_per_share * employee_purchase.share_count
    repurchase_price = min([fair_market_value, employee_purchase_price])
    repurchase_price_per_share = min(
        [current_price_per_share, employee_purchase.price_per_share])

    repurchase_event = PortfolioEvent(
        repurchase_time_idx,
        PortfolioEventType.REPURCHASE,
        share_grant_count,
        repurchase_price_per_share,
        True)

    # TODO: add cases where holding period < 1 year
    taxable_dollars = repurchase_price - employee_purchase_price
    if taxable_dollars > 0:
        tax_dollars = 1.0 * taxable_dollars * marginal_long_term_capital_gains_rate
        repurchase_tax_event = TaxEvent(
            repurchase_time_idx,
            taxable_dollars,
            TaxType.CAPITAL_GAINS_LONG_TERM,
            tax_dollars
        )
        return repurchase_event, repurchase_tax_event
    return repurchase_event, None
