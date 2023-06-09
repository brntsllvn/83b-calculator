from typing import List
from abc import ABC
from dataclasses import dataclass
from src.domain.lot import Lot


@dataclass
class TaxEvent(ABC):
    time_idx: int
    taxable_dollars: float
    tax_liability_dollars: float


@dataclass
class IncomeTax(TaxEvent):
    marginal_income_tax_rate: float


@dataclass
class CapitalGains(TaxEvent):
    lots: List[Lot]
    marginal_rate: float

    def __eq__(self, o):
        if o is None:
            return False

        if not isinstance(o, CapitalGains):
            return False

        if self.time_idx != o.time_idx or \
                self.taxable_dollars != o.taxable_dollars or \
                self.tax_liability_dollars != o.tax_liability_dollars or \
                self.marginal_rate != o.marginal_rate:
            return False

        if (self.lots is None and o.lots is not None) or (self.lots is not None and o.lots is None):
            return False

        if self.lots is not None and o.lots is not None:
            if len(self.lots) != len(o.lots):
                return False

            if not all(self_lot == o_lot for self_lot, o_lot in zip(self.lots, o.lots)):
                return False

        return True
