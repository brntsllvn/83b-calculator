from dataclasses import dataclass
from enum import Enum

from src.events.portfolio_event import PortfolioEventType


class TaxType(Enum):
    def __str__(self):
        return str(self.value)
    INCOME = 1
    CAPITAL_GAINS_LONG_TERM = 2
    CAPITAL_GAINS_SHORT_TERM = 3
    REPURCHASE = 4
    ZERO = 10


@dataclass
class TaxEvent:
    time_idx: int
    taxable_dollars: float
    tax_type: TaxType
    tax_dollars: float


def get_tax_events(portfolio_events,
                   employee_purchase,
                   tax_event_data):
    filed_83b = get_filed_83b(portfolio_events)
    tax_events = []
    for portfolio_event in portfolio_events:
        pet = portfolio_event.portfolio_event_type
        tax_event = None
        if pet is PortfolioEventType.GRANT:
            continue
        elif pet is PortfolioEventType.PURCHASE:
            continue
        elif pet is PortfolioEventType.FILE_83B:
            tax_event = get_83b_taxable_event(
                portfolio_event,
                tax_event_data.share_price_process[0],
                employee_purchase,
                tax_event_data.marginal_income_tax_rate
            )
        elif pet is PortfolioEventType.VEST:
            tax_event = get_vest_taxable_event(
                filed_83b,
                portfolio_event,
                employee_purchase,
                tax_event_data.share_price_process,
                tax_event_data.marginal_income_tax_rate
            )
        elif pet is PortfolioEventType.REPURCHASE:
            print("NOT IMPLEMENTED")
        elif pet is PortfolioEventType.SALE:
            tax_event = get_sale_taxable_event(
                filed_83b,
                portfolio_event,
                portfolio_events,
                tax_event_data.share_price_process,
                tax_event_data.marginal_long_term_capital_gains_rate
            )
        else:
            raise "unknown portfolio event type"
        if tax_event is not None:
            tax_events.append(tax_event)
    return tax_events


def get_filed_83b(portfolio_events):
    for portfolio_event in portfolio_events:
        if portfolio_event.portfolio_event_type is PortfolioEventType.FILE_83B:
            return True
    return False


def get_83b_taxable_event(
        portfolio_event,
        price_per_share_at_grant,
        employee_purchase,
        merginal_income_tax_rate):
    employee_purchase_dollars = get_purchase_dollars(employee_purchase)
    taxable_dollars = 1.0 * price_per_share_at_grant * \
        portfolio_event.share_count - employee_purchase_dollars
    tax_dollars = 1.0 * taxable_dollars * merginal_income_tax_rate
    if tax_dollars > 0:
        return TaxEvent(portfolio_event.time_idx, taxable_dollars, TaxType.INCOME, tax_dollars)
    return None


def get_vest_taxable_event(
        filed_83b,
        portfolio_event,
        employee_purchase,
        share_price_process,
        merginal_income_tax_rate):
    if filed_83b:
        return None

    time_idx = portfolio_event.time_idx
    share_price = share_price_process[time_idx]
    employee_purchase_dollars = get_purchase_dollars(employee_purchase)
    taxable_dollars = 1.0 * share_price * \
        portfolio_event.share_count - employee_purchase_dollars
    tax_dollars = 1.0 * taxable_dollars * merginal_income_tax_rate
    return TaxEvent(time_idx, taxable_dollars, TaxType.INCOME, tax_dollars)


def get_sale_taxable_event(
        filed_83b,
        sale_portfolio_event,
        all_portfolio_events,
        share_price_process,
        marginal_long_term_capital_gains_rate):
    fair_market_value = 1.0 * \
        sale_portfolio_event.share_count * share_price_process[-1]
    if filed_83b:
        basis = 1.0 * sale_portfolio_event.share_count * share_price_process[0]
    else:
        basis = get_no_83b_basis(all_portfolio_events,
                                 share_price_process)

    taxable_dollars = fair_market_value - basis
    tax_dollars = 1.0 * taxable_dollars * marginal_long_term_capital_gains_rate
    return TaxEvent(
        sale_portfolio_event.time_idx,
        taxable_dollars,
        TaxType.CAPITAL_GAINS_LONG_TERM,
        tax_dollars)


def get_no_83b_basis(all_portfolio_events,
                     share_price_process):
    basis = 0
    for portfolio_event in all_portfolio_events:
        if portfolio_event.portfolio_event_type is PortfolioEventType.VEST:
            basis += 1.0 * portfolio_event.share_count * \
                share_price_process[portfolio_event.time_idx]
    return basis


def get_purchase_dollars(employee_purchase):
    if employee_purchase is None:
        raise Exception("Employee purchase is None")

    if employee_purchase.price_per_share is None:
        raise Exception("Employee purchase price per share is None")

    if employee_purchase.share_count is None:
        raise Exception("Employee purchase share count is None")

    return 1.0 * employee_purchase.price_per_share * employee_purchase.share_count


def get_tax_diff_process(number_of_events, yes_83b_tax_events, no_83b_tax_events):
    tax_diff_process = []
    for idx in range(0, number_of_events):
        tax_diff = _subtract_tax_events(
            idx, yes_83b_tax_events, no_83b_tax_events)
        tax_diff_process.append(tax_diff)
    return tax_diff_process


def _subtract_tax_events(time_idx, yes_83b_tax_events, no_83b_tax_events):
    yes_83b_tax_event = _find_tax_event_by_id(time_idx, yes_83b_tax_events)
    no_83b_tax_event = _find_tax_event_by_id(time_idx, no_83b_tax_events)
    return no_83b_tax_event.tax_dollars - yes_83b_tax_event.tax_dollars


def _find_tax_event_by_id(time_idx, tax_events):
    for tax_event in tax_events:
        if tax_event.time_idx == time_idx:
            return tax_event
    return TaxEvent(time_idx, 0.0, TaxType.ZERO, 0.0)
