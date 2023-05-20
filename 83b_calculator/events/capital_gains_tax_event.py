from dataclasses import dataclass


@dataclass
class CapitalGainsTaxEvent:
    time_idx: int
    tax: float
