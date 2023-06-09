from abc import ABC  # , abstractmethod
from dataclasses import dataclass


@dataclass
class Purchase(ABC):
    share_count: int
    price_per_share: float

    def __post_init__(self):
        if self.share_count is None or \
                self.share_count < 0 or \
                self.price_per_share is None or \
                self.price_per_share < 0 or \
                not isinstance(self.share_count, int) or \
                not isinstance(self.price_per_share, float):
            raise ValueError(
                "share_count must be a positive integer, price_per_share must be a positive float")


@dataclass
class EmployeePurchase(Purchase):
    pass


@dataclass
class EmployerPurchase(Purchase):
    pass
