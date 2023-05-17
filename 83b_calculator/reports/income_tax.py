from dataclasses import dataclass


@dataclass
class IncomeTaxReport:
    shares_vesting_this_period: int
    income_tax: float
