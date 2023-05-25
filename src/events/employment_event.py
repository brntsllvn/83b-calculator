from dataclasses import dataclass
from enum import IntEnum


@dataclass
class EmploymentType(IntEnum):
    EMPLOYED = 1
    TERMINATED = 2
    UNEMPLOYED = 3


@dataclass
class EmploymentEvent:
    time_idx: int
    employment_type: EmploymentType
