from abc import ABC  # , abstractmethod
from dataclasses import dataclass

from src.domain.purchase import EmployeePurchase, EmployerPurchase


@dataclass
class PortfolioEvent(ABC):
    time_idx: int
    share_count: int

    # @abstractmethod
    # def common_method(self):
    #     pass


@dataclass
class Grant(PortfolioEvent):
    employee_purchase: EmployeePurchase

    def __eq__(self, o):
        if isinstance(o, Grant):
            equal = self.time_idx == o.time_idx and \
                self.share_count == o.share_count and \
                self.employee_purchase.price_per_share == o.employee_purchase.price_per_share and \
                self.employee_purchase.share_count == o.employee_purchase.share_count
            return equal
        return False

    def __post_init__(self):
        if not isinstance(self.employee_purchase, EmployeePurchase):
            raise TypeError(
                "employee_purchase must be of type EmployeePurchase")

    # def common_method(self):
    #     print("Common method in FirstImplementation")


@dataclass
class File83b(PortfolioEvent):
    pass


@dataclass
class Vest(PortfolioEvent):
    pass


@dataclass
class Sell(PortfolioEvent):
    pass


@dataclass
class Repurchase(PortfolioEvent):
    employer_purchase: EmployerPurchase

    def __eq__(self, o):
        if isinstance(o, Repurchase):
            equal = self.time_idx == o.time_idx and \
                self.share_count == o.share_count and \
                self.employer_purchase.price_per_share == o.employer_purchase.price_per_share and \
                self.employer_purchase.share_count == o.employer_purchase.share_count
            return equal
        return False
