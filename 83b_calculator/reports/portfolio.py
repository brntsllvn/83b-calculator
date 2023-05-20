from dataclasses import dataclass

from reports.lot import Lot


@dataclass
class PortfolioReport:
    lots: [Lot]
    portfolio_basis: float
    portfolio_value: float


def get_portfolio_report(section_83b_election_filed, share_prices, vesting_schedule):
    lots = get_lots(section_83b_election_filed, share_prices, vesting_schedule)
    portfolio_basis = get_portfolio_basis(lots)
    portfolio_value = get_portfolio_value(lots)
    return PortfolioReport(lots, portfolio_basis, portfolio_value)


def get_lots(section_83b_election_filed, share_prices, vesting_schedule):
    lots = []
    for idx, vesting_shares in enumerate(vesting_schedule):
        if vesting_shares > 0:
            if section_83b_election_filed:
                basis_per_share = share_prices[0]
            else:
                basis_per_share = share_prices[idx]
            current_price_per_share = share_prices[-1]
            lot = Lot(
                idx,
                vesting_shares,
                basis_per_share,
                round(1.0 * vesting_shares * basis_per_share, 2),
                current_price_per_share,
                round(1.0 * vesting_shares * current_price_per_share, 2)
            )
            lots.append(lot)
    return lots


def get_portfolio_basis(lots):
    portfolio_basis = 0
    for lot in lots:
        portfolio_basis += lot.lot_basis
    return portfolio_basis


def get_portfolio_value(lots):
    portfolio_value = 0
    for lot in lots:
        portfolio_value += lot.lot_value
    return portfolio_value