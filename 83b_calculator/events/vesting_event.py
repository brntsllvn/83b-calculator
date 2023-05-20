from dataclasses import dataclass


@dataclass
class VestingEvent:
    time_idx: int
    share_count: int
