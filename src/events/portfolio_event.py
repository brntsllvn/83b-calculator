from dataclasses import dataclass
from enum import Enum


class PortfolioEventType(Enum):
    def __str__(self):
        return str(self.value)
    GRANT = 1
    PURCHASE = 2
    FILE_83B = 3
    VEST = 4
    REPURCHASE = 5
    SALE = 6


@dataclass
class PortfolioEvent:
    time_idx: int
    portfolio_event_type: PortfolioEventType
    share_count: int


def get_portfolio_events(file_83b_election, scenario):
    portfolio_events = []
    share_grant = sum(scenario.vesting_schedule)
    grant_event = PortfolioEvent(0, PortfolioEventType.GRANT, share_grant)
    portfolio_events.append(grant_event)

    if scenario.employee_purchase and scenario.employee_purchase.share_count > 0:
        purchase_event = PortfolioEvent(
            0, PortfolioEventType.PURCHASE, scenario.employee_purchase.share_count)
        portfolio_events.append(purchase_event)

    if file_83b_election:
        # TODO: ISO 83(b) may not be time 0 depending on exercise
        election_event = PortfolioEvent(
            0, PortfolioEventType.FILE_83B, share_grant)
        portfolio_events.append(election_event)

    for idx in range(1, len(scenario.vesting_schedule)):
        if idx == scenario.termination_idx:
            # TODO: add cases for FMV > purchase, FMV == purchase, FMV < puchase
            repurchase_event = PortfolioEvent(
                idx, PortfolioEventType.REPURCHASE, share_grant)
            portfolio_events.append(repurchase_event)
            break
        else:
            vesting_share_count = scenario.vesting_schedule[idx]
            if vesting_share_count > 0:
                vesting_event = PortfolioEvent(
                    idx, PortfolioEventType.VEST, vesting_share_count)
                portfolio_events.append(vesting_event)

        if idx == len(scenario.vesting_schedule) - 1:
            # TODO add cases for short-term holding period and long-term
            sale_event = PortfolioEvent(
                idx, PortfolioEventType.SALE, share_grant)
            portfolio_events.append(sale_event)

    return portfolio_events
