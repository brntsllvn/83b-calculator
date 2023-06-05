from abc import ABC  # , abstractmethod
from dataclasses import dataclass


@dataclass
class TaxEvent(ABC):
    time_idx: int
    taxable_dollars: float
    tax_liability_dollars: float


@dataclass
class IncomeTax(TaxEvent):
    marginal_income_tax_rate: float


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


@dataclass
class CapitalGains(TaxEvent):
    lots: [Lot]
    marginal_rate: float

    def __eq__(self, o):
        if isinstance(o, CapitalGains):
            equal = self.time_idx == o.time_idx and \
                self.taxable_dollars == o.taxable_dollars and \
                self.tax_liability_dollars == o.tax_liability_dollars and \
                self.marginal_rate == o.marginal_rate
            lots_equal = all(self_lot == o_lot for self_lot,
                             o_lot in zip(self.lots, o.lots))
            return equal and lots_equal
        return False
