from dataclasses import dataclass


@dataclass
class Lot:
    vesting_period_idx: int
    shares_count: int
    basis_per_share: float
    lot_basis: float
    price_per_share: float
    lot_value: float
