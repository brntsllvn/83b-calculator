from dataclasses import dataclass

from src.state.lot import Lot


@dataclass
class Portfolio:
    lots: [Lot]
