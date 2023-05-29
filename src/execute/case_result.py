from dataclasses import dataclass

from src.events.portfolio_event import PortfolioEvent


@dataclass
class CaseResult:
    portfolio_events: [PortfolioEvent]
