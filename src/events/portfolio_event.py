from dataclasses import dataclass
from enum import Enum


class PortfolioEventType(Enum):
    def __str__(self):
        return str(self.value)
    GRANT = 1
    PURCHASE = 2
    FILE_83B = 3
    VEST = 4
    REPURCHASE = 5
    SALE = 6


@dataclass
class PortfolioEvent:
    time_idx: int
    portfolio_event_type: PortfolioEventType
    share_count: int
