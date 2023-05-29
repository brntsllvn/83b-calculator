from dataclasses import dataclass

from src.events.share_event import PortfolioEvent
from src.events.tax_event import TaxEvent
from src.state.lot import Lot


@dataclass
class CaseResult:
    share_events: [PortfolioEvent]
    lots: [Lot]
    tax_events: [TaxEvent]
