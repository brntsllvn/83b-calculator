from dataclasses import dataclass

from reports.portfolio import PortfolioReport
from reports.income_tax import IncomeTaxReport


@dataclass
class VestingReport:
    vesting_period_idx: int
    price_per_share: float
    portfolio_report: PortfolioReport
    income_tax_report: IncomeTaxReport
