from src.execute.shared import CaseResult, get_repurchase_events
from src.events.share_event import PortfolioEvent, PortfolioEventType
from src.events.tax_event import TaxEvent, TaxType
from src.state.lot import Lot
from src.execute.shared import get_sale_events
from src.events.employment_event import EmploymentType


def execute_no_83b(marginal_income_tax_rate,
                   marginal_long_term_capital_gains_rate,
                   employee_purchase,
                   vesting_schedule,
                   share_price_process,
                   employment_process):
    share_events = []
    tax_events = []
    lots = []

    share_grant_count = sum(vesting_schedule)
    basis_per_share = share_price_process[0]

    grant_event = PortfolioEvent(
        0,
        PortfolioEventType.GRANT,
        share_grant_count,
        basis_per_share,
        False
    )
    share_events.append(grant_event)

    if employee_purchase.share_count > 0:
        purchase_event = PortfolioEvent(
            0,
            PortfolioEventType.PURCHASE,
            employee_purchase.share_count,
            employee_purchase.price_per_share,
            False
        )
        share_events.append(purchase_event)

    lots, vesting_events, tax_events = \
        _no_83b_calculate_lots_and_events(marginal_income_tax_rate,
                                          marginal_long_term_capital_gains_rate,
                                          vesting_schedule,
                                          share_price_process,
                                          employee_purchase,
                                          basis_per_share,
                                          share_grant_count,
                                          employment_process)

    share_events.extend(vesting_events)
    case_result = CaseResult(share_events, lots, tax_events)
    return case_result


def _no_83b_calculate_lots_and_events(marginal_income_tax_rate,
                                      marginal_long_term_capital_gains_rate,
                                      vesting_schedule,
                                      share_price_process,
                                      employee_purchase,
                                      basis_per_share,
                                      share_grant_count,
                                      employment_process):

    share_events = []
    lots = []
    tax_events = []
    for idx, count_vesting_shares in enumerate(vesting_schedule):
        employment_status = employment_process[idx]
        if employment_status is EmploymentType.EMPLOYED and count_vesting_shares > 0:
            vesting_event = PortfolioEvent(
                idx,
                PortfolioEventType.VEST,
                count_vesting_shares,
                share_price_process[idx],
                True)
            share_events.append(vesting_event)

            price_per_share = share_price_process[idx]
            fair_market_value = count_vesting_shares * price_per_share
            employee_purchase_price = employee_purchase.price_per_share * \
                employee_purchase.share_count
            taxable_income = fair_market_value - employee_purchase_price
            income_tax = round(1.0 * taxable_income *
                               marginal_income_tax_rate, 2)
            if income_tax != 0:
                income_tax_event = TaxEvent(
                    idx, taxable_income, TaxType.INCOME, income_tax)
                tax_events.append(income_tax_event)

            lot = Lot(idx, count_vesting_shares, price_per_share)
            lots.append(lot)
        elif employment_status is EmploymentType.TERMINATED:
            repurchase_share_event, repurchase_tax_event = get_repurchase_events(
                marginal_long_term_capital_gains_rate,
                idx,
                share_grant_count,
                share_price_process[idx],
                lots,
                employee_purchase)
            share_events.append(repurchase_share_event)
            if repurchase_tax_event != None:
                tax_events.append(repurchase_tax_event)
    return lots, share_events, tax_events
