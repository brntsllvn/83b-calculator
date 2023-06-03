from dataclasses import dataclass

from src.domain.employee_purchase import EmployeePurchase


@dataclass
class PortfolioEventData:
    vesting_schedule: [int]
    termination_idx: int
    employee_purchase: EmployeePurchase = EmployeePurchase(0, 0)


@dataclass
class TaxEventData:
    marginal_income_tax_rate: float
    marginal_long_term_capital_gains_rate: float
    share_price_process: [float]


@dataclass
class Metadata:
    discount_rate: float
