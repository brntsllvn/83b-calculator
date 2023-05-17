from dataclasses import dataclass

from reports.lot import Lot


@dataclass
class PortfolioReport:
    lots: [Lot]
