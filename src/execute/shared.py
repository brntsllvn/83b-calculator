from dataclasses import dataclass

from src.events.portfolio_event import PortfolioEvent, PortfolioEventType
from src.events.employment_event import EmploymentType
from src.events.tax_event import TaxEvent, TaxType
from src.execute.case_result import CaseResult


def get_events(file_83b_election,
               share_price_process,
               vesting_schedule,
               employment_process,
               employee_purchase):
    portfolio_events = []
    share_grant = sum(vesting_schedule)
    grant_event = PortfolioEvent(0, PortfolioEventType.GRANT, share_grant)
    portfolio_events.append(grant_event)

    if employee_purchase.share_count > 0:
        purchase_event = PortfolioEvent(
            0, PortfolioEventType.PURCHASE, employee_purchase.share_count)
        portfolio_events.append(purchase_event)

    if file_83b_election:
        # TODO: ISO 83(b) may not be time 0 depending on exercise
        election_event = PortfolioEvent(
            0, PortfolioEventType.FILE_83B, share_grant)
        portfolio_events.append(election_event)

    for idx in range(1, len(vesting_schedule)):
        employment_status = employment_process[idx]
        if employment_status is EmploymentType.EMPLOYED:
            vesting_share_count = vesting_schedule[idx]
            if vesting_share_count > 0:
                vesting_event = PortfolioEvent(
                    idx, PortfolioEventType.VEST, vesting_share_count)
                portfolio_events.append(vesting_event)
        else:
            # TODO: add cases for FMV > purchase, FMV == purchase, FMV < puchase
            repurchase_event = PortfolioEvent(
                idx, PortfolioEventType.REPURCHASE, share_grant)
            portfolio_events.append(repurchase_event)
            break

        if idx == len(vesting_schedule) - 1:
            # TODO add cases for short-term holding period and long-term
            sale_event = PortfolioEvent(
                idx, PortfolioEventType.SALE, share_grant)
            portfolio_events.append(sale_event)

    return portfolio_events
