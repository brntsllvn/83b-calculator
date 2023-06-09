from abc import ABC
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
class CapitalGains(TaxEvent):
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
        return True
