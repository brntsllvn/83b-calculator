from dataclasses import dataclass
from enum import Enum


class EmploymentType(Enum):
    def __str__(self):
        return str(self.value)
    EMPLOYED = 1
    TERMINATED = 2
    UNEMPLOYED = 3
