from dataclasses import dataclass
from enum import IntEnum


class TaxType(IntEnum):
    INCOME = 1
    CAPITAL_GAINS_LONG_TERM = 2
    ZERO = 10


@dataclass
class TaxEvent:
    time_idx: int
    taxable_amount: float
    tax_type: TaxType
    tax_amount: float
