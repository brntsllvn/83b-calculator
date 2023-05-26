from dataclasses import dataclass

from src.events.share_event import ShareEvent, ShareEventType
from src.events.tax_event import TaxEvent, TaxType
from src.state.lot import Lot


@dataclass
class Result:
    share_events: [ShareEvent]
    lots: [Lot]
    tax_events: [TaxEvent]


def get_portfolio(lots, liquidation_share_price):
    basis = 0
    value = 0
    share_count = 0
    for idx, lot in enumerate(lots):
        basis += lot.share_count * lot.basis_per_share
        value += lot.share_count * liquidation_share_price
        share_count += lot.share_count
    return value, basis, share_count


def get_liquidation_events(marginal_long_term_capital_gains_rate,
                           share_price_process,
                           lots):
    liquidate_time_idx = len(share_price_process) - 1
    liquidation_share_price = share_price_process[-1]
    portfolio_value, portfolio_basis, portfolio_share_count = \
        get_portfolio(lots, liquidation_share_price)

    sale_event = ShareEvent(
        liquidate_time_idx,
        ShareEventType.SALE,
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
