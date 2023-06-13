from dataclasses import dataclass, asdict
from typing import List
from pprint import pprint


@dataclass
class TaxFlows:
    file_83b_tax_paid: List[float]
    forgo_83b_tax_paid: List[float]
    tax_diff_process: List[float]


@dataclass
class ScenarioResult:
    tax_flows: TaxFlows
    raw: float
    npv: float

    def pp(self):
        pprint(asdict(self))
