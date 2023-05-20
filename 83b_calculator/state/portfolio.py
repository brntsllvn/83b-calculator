from dataclasses import dataclass

from state.lot import Lot


@dataclass
class Portfolio:
    lots: [Lot]
