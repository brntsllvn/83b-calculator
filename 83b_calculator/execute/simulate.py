from events.vesting_event import VestingEvent
from events.income_tax_event import IncomeTaxEvent
from events.capital_gains_tax_event import CapitalGainsTaxEvent
from state.portfolio import Portfolio
from state.lot import Lot


def run_scenario(marginal_income_tax_rate,
                 marginal_long_term_capital_gains_rate,
                 filed_83b_election,
                 vesting_schedule,
                 share_price_process):

    vesting_events = []
    income_tax_events = []
    capital_gains_tax_events = []
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
                income_tax_event = IncomeTaxEvent(idx, income_tax)
                income_tax_events.append(income_tax_event)

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
        capital_gains_tax_event = CapitalGainsTaxEvent(
            len(share_price_process) - 1, capital_gains_tax)
        capital_gains_tax_events.append(capital_gains_tax_event)

        return (vesting_events, income_tax_events, capital_gains_tax_events)
