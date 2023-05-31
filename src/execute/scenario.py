from dataclasses import dataclass

from src.events.employment_event import EmploymentType, EmployeePurchase


@dataclass
class Scenario:
    vesting_schedule: [int]
    share_price_process: [float]
    employment_process: [EmploymentType]
    employee_purchase: EmployeePurchase = EmployeePurchase(0, 0)


@dataclass
class ScenarioMetadata:
    marginal_income_tax_rate: float
    marginal_long_term_capital_gains_rate: float
    discount_rate: float
