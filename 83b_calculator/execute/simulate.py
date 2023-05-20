from events.vesting_event import VestingEvent
from events.tax_event import TaxEvent, TaxType
from state.portfolio import Portfolio
from state.lot import Lot


def run_scenario(marginal_income_tax_rate,
                 marginal_long_term_capital_gains_rate,
                 filed_83b_election,
                 vesting_schedule,
                 share_price_process):

    vesting_events = []
    tax_events = []
    lots = []
    if filed_83b_election:
        # TODO
        return 1
    else:
        # vesting
        for idx, count_vesting_shares in enumerate(vesting_schedule):
            if count_vesting_shares > 0:
                vesting_event = VestingEvent(idx, count_vesting_shares)
                vesting_events.append(vesting_event)

                price_per_share = share_price_process[idx]
                income_tax = round(
                    1.0 * count_vesting_shares * price_per_share * marginal_income_tax_rate, 2)
                income_tax_event = TaxEvent(
                    idx, TaxType.INCOME, income_tax)
                tax_events.append(income_tax_event)

                lot = Lot(idx, count_vesting_shares, price_per_share)
                lots.append(lot)

        # portfolio
        portfolio_basis = 0
        portfolio_value = 0
        for idx, lot in enumerate(lots):
            portfolio_basis += lot.share_count * lot.basis_per_share
            portfolio_value += lot.share_count * share_price_process[-1]

        # liquidation
        capital_gains_tax = round(
            1.0 * (portfolio_value - portfolio_basis) * marginal_long_term_capital_gains_rate, 2)
        capital_gains_tax_event = TaxEvent(
            len(share_price_process) - 1, TaxType.CAPITAL_GAINS_LONG_TERM, capital_gains_tax)
        tax_events.append(capital_gains_tax_event)

        return (vesting_events, tax_events)
