from src.domain.portfolio_event import Grant, File83b, Vest, Sell, Repurchase, Forfeit
from src.domain.tax_event import IncomeTax, CapitalGains
from src.domain.lot import get_portfolio_lots


def get_tax_events(portfolio_events,
                   employee_purchase,
                   tax_event_data):
    filed_83b = get_filed_83b(portfolio_events)
    tax_events = []
    for portfolio_event in portfolio_events:
        tax_event = None
        if isinstance(portfolio_event, Grant) or \
                isinstance(portfolio_event, Forfeit):
            continue
        elif isinstance(portfolio_event, File83b):
            tax_event = get_83b_taxable_event(
                portfolio_event,
                tax_event_data.share_price_process[0],
                employee_purchase,
                tax_event_data.marginal_income_tax_rate
            )
        elif isinstance(portfolio_event, Vest):
            tax_event = get_vest_taxable_event(
                filed_83b,
                portfolio_event,
                employee_purchase,
                tax_event_data.share_price_process,
                tax_event_data.marginal_income_tax_rate
            )
        elif isinstance(portfolio_event, Sell) or \
                isinstance(portfolio_event, Repurchase):
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
        if isinstance(portfolio_event, File83b):
            return True
    return False


def get_83b_taxable_event(
        portfolio_event,
        price_per_share_at_grant,
        employee_purchase,
        marginal_income_tax_rate):
    employee_purchase_dollars = get_purchase_dollars(employee_purchase)
    taxable_dollars = round(1.0 * price_per_share_at_grant *
                            portfolio_event.share_count - employee_purchase_dollars, 2)
    tax_dollars = round(1.0 * taxable_dollars * marginal_income_tax_rate, 2)
    return IncomeTax(
        portfolio_event.time_idx, taxable_dollars, tax_dollars, marginal_income_tax_rate)


def get_vest_taxable_event(
        filed_83b,
        portfolio_event,
        employee_purchase,
        share_price_process,
        marginal_income_tax_rate):
    if filed_83b:
        return None

    time_idx = portfolio_event.time_idx
    share_price = share_price_process[time_idx]
    employee_purchase_per_share = employee_purchase.price_per_share
    # TODO: Handle the case when employee buys shares at a discount
    taxable_dollars = round(1.0 *
                            (share_price - employee_purchase_per_share) *
                            portfolio_event.share_count, 2)
    tax_dollars = round(1.0 * taxable_dollars * marginal_income_tax_rate, 2)
    return IncomeTax(time_idx, taxable_dollars, tax_dollars, marginal_income_tax_rate)


def get_sale_taxable_event(
        filed_83b,
        sale_portfolio_event,
        all_portfolio_events,
        share_price_process,
        marginal_long_term_capital_gains_rate):
    sell_time_idx = sale_portfolio_event.time_idx
    fair_market_value = 1.0 * \
        sale_portfolio_event.share_count * share_price_process[sell_time_idx]
    lots = get_portfolio_lots(
        filed_83b, all_portfolio_events, share_price_process)
    portfolio_basis = get_portfolio_basis(lots)
    taxable_dollars = round(fair_market_value - portfolio_basis, 2)
    tax_dollars = round(1.0 * taxable_dollars *
                        marginal_long_term_capital_gains_rate, 2)
    return CapitalGains(
        sale_portfolio_event.time_idx,
        taxable_dollars,
        tax_dollars,
        marginal_long_term_capital_gains_rate)


def get_portfolio_basis(lots):
    basis = 0
    for lot in lots:
        basis += lot.share_count * lot.basis_per_share
    return basis


def get_purchase_dollars(employee_purchase):
    return 1.0 * employee_purchase.price_per_share * employee_purchase.share_count


def get_tax_diff_process(number_of_events, yes_83b_tax_events, no_83b_tax_events):
    tax_diff_process = []
    for idx in range(0, number_of_events):
        tax_diff = _subtract_tax_events(
            idx, yes_83b_tax_events, no_83b_tax_events)
        tax_diff_process.append(tax_diff)
    return tax_diff_process


def _subtract_tax_events(time_idx, yes_83b_tax_events, no_83b_tax_events):
    yes_83b_tax_liability = _find_tax_liability_by_id(
        time_idx, yes_83b_tax_events)
    no_83b_tax_liability = _find_tax_liability_by_id(
        time_idx, no_83b_tax_events)
    # NOTE: we flip the sign since tax is a cash outflow
    return -1.0 * (yes_83b_tax_liability - no_83b_tax_liability)


def _find_tax_liability_by_id(time_idx, tax_events):
    for tax_event in tax_events:
        # TODO: check for multiple items with the same index
        # This could happen if someone vests and sells in the same year
        if tax_event.time_idx == time_idx:
            return tax_event.tax_liability_dollars
    return 0
