from dataclasses import dataclass
from enum import Enum


class TaxType(Enum):
    INCOME = 1
    CAPITAL_GAINS_LONG_TERM = 2
    PLACEHOLDER = 10


@dataclass
class TaxEvent:
    time_idx: int
    tax_type: TaxType
    tax_amount: float
