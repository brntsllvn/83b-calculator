from dataclasses import dataclass

from reports.income_tax_event import IncomeTaxEvent


@dataclass
class IncomeTaxReport:
    income_tax_events: [IncomeTaxEvent]


def get_income_tax_report(section_83b_election_filed,
                          share_prices,
                          vesting_schedule,
                          marginal_income_tax_rate):
    income_tax_events = get_income_tax_events(section_83b_election_filed,
                                              share_prices,
                                              vesting_schedule,
                                              marginal_income_tax_rate)
    return IncomeTaxReport(income_tax_events)


def get_income_tax_events(section_83b_election_filed,
                          share_prices,
                          vesting_schedule,
                          marginal_income_tax_rate):

    income_tax_events = []
    for idx, vesting_shares in enumerate(vesting_schedule):
        income_tax = 0
        current_price_per_share = share_prices[idx]
        if section_83b_election_filed and idx == 0:
            shares_granted = sum(vesting_schedule)
            taxable_income = shares_granted * current_price_per_share
            income_tax = round(1.0 * taxable_income *
                               marginal_income_tax_rate, 2)
            return IncomeTaxEvent(idx, income_tax)
        else:
            vesting_shares = vesting_schedule[idx]
            if vesting_shares == 0:
                continue
            taxable_income = vesting_shares * current_price_per_share
            income_tax = round(1.0 * taxable_income *
                               marginal_income_tax_rate, 2)
            income_tax_event = IncomeTaxEvent(idx, income_tax)
            income_tax_events.append(IncomeTaxEvent(idx, income_tax))
    return income_tax_events
