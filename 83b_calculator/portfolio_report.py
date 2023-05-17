from dataclasses import dataclass

from lot import Lot


@dataclass
class PortfolioReport:
    vesting_period_idx: int
    shares_vesting_this_period: int
    total_vested_shares_incl_this_period: int
    unvested_remaining: int
    lots: [Lot]
    portfolio_value_dollars: float
    portfolio_basis_dollars: float
    income_tax: float
    capital_gains_tax: float
