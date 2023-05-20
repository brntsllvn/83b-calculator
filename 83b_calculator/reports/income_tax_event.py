from dataclasses import dataclass


@dataclass
class IncomeTaxEvent:
    time_idx: int
    income_tax: float
