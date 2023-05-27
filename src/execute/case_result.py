from dataclasses import dataclass

from src.events.share_event import ShareEvent
from src.events.tax_event import TaxEvent
from src.state.lot import Lot


@dataclass
class CaseResult:
    share_events: [ShareEvent]
    lots: [Lot]
    tax_events: [TaxEvent]
