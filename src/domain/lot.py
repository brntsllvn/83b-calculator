from dataclasses import dataclass


@dataclass
class Lot:
    acquisition_time_idx: int
    basis_per_share: float
    share_count: int

    def __eq__(self, o):
        if isinstance(o, Lot):
            equal = self.acquisition_time_idx == o.acquisition_time_idx and \
                self.basis_per_share == o.basis_per_share and \
                self.share_count == o.share_count
            return equal
        return False
