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


def get_tax_events(portfolio_events,
                   share_price_process,
                   employee_purchase,
                   merginal_income_tax_rate,
                   marginal_long_term_capital_gains_rate):
    filed_83b = get_filed_83b(portfolio_events)
    tax_events = []
    for portfolio_event in portfolio_events:
        pet = portfolio_event.portfolio_event_type
        tax_event = None
        if pet is PortfolioEventType.GRANT:
            continue
        elif pet is PortfolioEventType.PURCHASE:
            continue
        elif pet is PortfolioEventType.FILE_83B:
            tax_event = get_83b_taxable_event(
                portfolio_event,
                share_price_process[0],
                employee_purchase,
                merginal_income_tax_rate
            )
        elif pet is PortfolioEventType.VEST:
            tax_event = get_vest_taxable_event(
                filed_83b,
                portfolio_event,
                share_price_process,
                merginal_income_tax_rate
            )
        elif pet is PortfolioEventType.REPURCHASE:
            print("NOT IMPLEMENTED")
        elif pet is PortfolioEventType.SALE:
            tax_event = get_sale_taxable_event(
                filed_83b,
                portfolio_event,
                portfolio_events,
                share_price_process,
                employee_purchase,
                marginal_long_term_capital_gains_rate
            )
        else:
            raise "unknown portfolio event type"
        if tax_event is not None:
            tax_events.append(tax_event)
    return tax_events


def get_filed_83b(portfolio_events):
    for portfolio_event in portfolio_events:
        if portfolio_event.portfolio_event_type is PortfolioEventType.FILE_83B:
            return True
    return False


def get_83b_taxable_event(
        portfolio_event,
        price_per_share_at_grant,
        employee_purchase,
        merginal_income_tax_rate):
    employee_purchase_dollars = 1.0 * \
        employee_purchase.price_per_share * employee_purchase.share_count
    taxable_dollars = 1.0 * price_per_share_at_grant * \
        portfolio_event.share_count - employee_purchase_dollars
    tax_dollars = 1.0 * taxable_dollars * merginal_income_tax_rate
    if tax_dollars > 0:
        return TaxEvent(portfolio_event.time_idx, taxable_dollars, TaxType.INCOME, tax_dollars)
    return None


def get_vest_taxable_event(
        filed_83b,
        portfolio_event,
        share_price_process,
        merginal_income_tax_rate):
    if filed_83b:
        return None

    time_idx = portfolio_event.time_idx
    share_price = share_price_process[time_idx]
    taxable_dollars = 1.0 * share_price * portfolio_event.share_count
    tax_dollars = 1.0 * taxable_dollars * merginal_income_tax_rate
    return TaxEvent(time_idx, taxable_dollars, TaxType.INCOME, tax_dollars)


def get_sale_taxable_event(
        filed_83b,
        sale_portfolio_event,
        all_portfolio_events,
        share_price_process,
        employee_purchase,
        marginal_long_term_capital_gains_rate):
    employee_purchase_dollars = \
        1.0 * employee_purchase.price_per_share * employee_purchase.share_count
    fair_market_value = 1.0 * \
        sale_portfolio_event.share_count * share_price_process[-1]
    if filed_83b:
        basis = 1.0 * sale_portfolio_event.share_count * \
            share_price_process[0] + employee_purchase_dollars
    else:
        basis = get_no_83b_basis(all_portfolio_events,
                                 share_price_process,
                                 employee_purchase_dollars)

    taxable_dollars = fair_market_value - basis
    tax_dollars = 1.0 * taxable_dollars * marginal_long_term_capital_gains_rate
    return TaxEvent(
        sale_portfolio_event.time_idx,
        taxable_dollars,
        TaxType.CAPITAL_GAINS_LONG_TERM,
        tax_dollars)


def get_no_83b_basis(all_portfolio_events,
                     share_price_process,
                     employee_purchase_dollars):
    basis = 0
    for portfolio_event in all_portfolio_events:
        if portfolio_event.portfolio_event_type is PortfolioEventType.VEST:
            basis += 1.0 * portfolio_event.share_count * \
                share_price_process[portfolio_event.time_idx] + \
                employee_purchase_dollars
    return basis
