from dataclasses import dataclass


@dataclass
class Lot:
    time_idx: int
    share_count: int
    basis_per_share: float