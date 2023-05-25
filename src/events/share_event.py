from dataclasses import dataclass
from enum import IntEnum

# TODO: implement


@dataclass
class ShareEventType(IntEnum):
    GRANT = 1
    PURCHASE = 2
    VEST = 3
    REPURCHASE = 4
    SALE = 5


@dataclass
class ShareEvent:
    time_idx: int
    share_event_type: ShareEventType
    share_count: int
    share_price: float
    taxable: bool
