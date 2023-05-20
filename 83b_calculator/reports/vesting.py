from dataclasses import dataclass

from reports.portfolio import PortfolioReport
from reports.income_tax import IncomeTaxReport


# TODO: Create a VestingEvent (similar to IncomeTaxEvent)
# @dataclass
# class VestingEvent:
#     time_idx: int
#     shares_vesting: int


@dataclass
class VestingReport:
    time_idx: int
    price_per_share: float
    portfolio_report: PortfolioReport
    income_tax_report: IncomeTaxReport
