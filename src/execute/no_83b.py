from src.execute.shared import Result
from src.events.share_event import ShareEvent, ShareEventType
from src.events.tax_event import TaxEvent, TaxType
from src.state.lot import Lot
from src.execute.shared import get_liquidation_events


def run_no_83b_scenario(
        marginal_income_tax_rate,
        marginal_long_term_capital_gains_rate,
        employee_purchase,
        vesting_schedule,
        share_price_process):
    share_events, tax_events, lots = _get_events_and_lots(
        marginal_income_tax_rate,
        vesting_schedule,
        employee_purchase,
        share_price_process)
    if len(lots) != 0:
        sale_event, capital_gains_tax_event = get_liquidation_events(
            marginal_long_term_capital_gains_rate,
            share_price_process,
            lots)
        share_events.append(sale_event)
        tax_events.append(capital_gains_tax_event)
    scenario_result = Result(share_events, lots, tax_events)
    return scenario_result


def _get_events_and_lots(marginal_income_tax_rate,
                         vesting_schedule,
                         employee_purchase,
                         share_price_process):
    share_events = []
    tax_events = []
    lots = []

    share_grant_count = sum(vesting_schedule)
    basis_per_share = share_price_process[0]

    grant_event = ShareEvent(
        0,
        ShareEventType.GRANT,
        share_grant_count,
        basis_per_share,
        False
    )
    share_events.append(grant_event)

    if employee_purchase.share_count > 0:
        purchase_event = ShareEvent(
            0,
            ShareEventType.PURCHASE,
            employee_purchase.share_count,
            employee_purchase.price_per_share,
            False
        )
        share_events.append(purchase_event)

    lots, vesting_events, tax_events = \
        _calculate_lots_and_events(marginal_income_tax_rate,
                                   vesting_schedule,
                                   share_price_process,
                                   employee_purchase,
                                   basis_per_share)

    share_events.extend(vesting_events)
    return share_events, tax_events, lots


def _calculate_lots_and_events(marginal_income_tax_rate,
                               vesting_schedule,
                               share_price_process,
                               employee_purchase,
                               basis_per_share):

    vesting_events = []
    lots = []
    tax_events = []
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
    return lots, vesting_events, tax_events
