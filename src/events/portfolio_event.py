from src.domain.portfolio_event import Grant, File83b, Vest, Sell, Repurchase, Forfeit
from src.domain.purchase import EmployerPurchase


def get_portfolio_events(file_83b_election, scenario):
    portfolio_events = []
    share_grant = sum(scenario.vesting_schedule)
    grant_event = Grant(0, share_grant, scenario.employee_purchase)
    portfolio_events.append(grant_event)

    if file_83b_election:
        # TODO: ISO 83(b) may not be time 0 depending on exercise
        election_event = File83b(0, share_grant)
        portfolio_events.append(election_event)

    for idx in range(1, len(scenario.vesting_schedule)):
        if idx == scenario.termination_idx:
            if scenario.employee_purchase.share_count > 0:
                employer_purchase = _get_employer_purchase(
                    scenario.employee_purchase)
                repurchase_event = Repurchase(
                    idx, share_grant, employer_purchase)
                portfolio_events.append(repurchase_event)
            else:
                portfolio_events.append(Forfeit(idx, share_grant))
            break
        else:
            vesting_share_count = scenario.vesting_schedule[idx]
            if vesting_share_count > 0:
                vesting_event = Vest(idx, vesting_share_count)
                portfolio_events.append(vesting_event)

        if idx == scenario.liquidation_idx:
            # TODO add cases for short-term holding period and long-term
            sale_event = Sell(idx, share_grant)
            portfolio_events.append(sale_event)

    return portfolio_events


def _get_employer_purchase(employee_purchase):
    """
        TODO Repurchase option cases:
        1. Default: "Company A will repurchase the stock from E for the lesser
            of the then current fair market value or the original purchase price"
            1.1 min(FMV, purchase_price)
        2. max(FMV, purchase_price)
    """
    return EmployerPurchase(employee_purchase.share_count, employee_purchase.price_per_share)
