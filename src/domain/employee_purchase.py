from dataclasses import dataclass
from enum import Enum


@dataclass
class EmployeePurchase:
    price_per_share: float
    share_count: int
