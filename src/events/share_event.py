from dataclasses import dataclass
from enum import IntEnum

# TODO: implement


@dataclass
class PortfolioEventType(IntEnum):
    GRANT = 1
    PURCHASE = 2
    VEST = 3
    REPURCHASE = 4
    SALE = 5


@dataclass
class PortfolioEvent:
    time_idx: int
    share_event_type: PortfolioEventType
    share_count: int
    share_price: float
    taxable: bool
