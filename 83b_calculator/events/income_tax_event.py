from dataclasses import dataclass


@dataclass
class IncomeTaxEvent:
    time_idx: int
    tax: float
