from dataclasses import dataclass
from typing import List

from src.domain.portfolio_event import EmployeePurchase


@dataclass
class PortfolioEventData:
    vesting_schedule: List[int]
    termination_idx: int
    employee_purchase: EmployeePurchase
    liquidation_idx: int


@dataclass
class TaxEventData:
    marginal_income_tax_rate: float
    marginal_long_term_capital_gains_rate: float
    share_price_process: List[float]


@dataclass
class Metadata:
    discount_rate: float
