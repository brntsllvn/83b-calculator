from dataclasses import dataclass

from src.events.employment_event import EmploymentType, EmployeePurchase


@dataclass
class PortfolioEventData:
    vesting_schedule: [int]
    employment_process: [EmploymentType]
    employee_purchase: EmployeePurchase = EmployeePurchase(0, 0)


@dataclass
class TaxEventData:
    marginal_income_tax_rate: float
    marginal_long_term_capital_gains_rate: float
    share_price_process: [float]


@dataclass
class Metadata:
    discount_rate: float
