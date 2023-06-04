from abc import ABC  # , abstractmethod
from dataclasses import dataclass


@dataclass
class Purchase(ABC):
    share_count: int
    price_per_share: float


@dataclass
class EmployeePurchase(Purchase):
    pass


@dataclass
class EmployerPurchase(Purchase):
    pass
