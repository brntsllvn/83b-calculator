from dataclasses import dataclass


@dataclass
class IncomeTaxReport:
    shares_vesting_this_period: int
    income_tax: float


def get_income_tax_report(section_83b_election_filed,
                          vesting_period_idx,
                          share_prices,
                          vesting_schedule,
                          marginal_income_tax_rate):
    shares_vesting_this_period = get_shares_vesting_this_period(
        vesting_period_idx,
        vesting_schedule
    )
    income_tax = get_income_tax(section_83b_election_filed,
                                vesting_period_idx,
                                share_prices,
                                vesting_schedule,
                                marginal_income_tax_rate)
    return IncomeTaxReport(shares_vesting_this_period, income_tax)


def get_shares_vesting_this_period(vesting_period_idx, vesting_schedule):
    return vesting_schedule[vesting_period_idx]


def get_income_tax(section_83b_election_filed,
                   vesting_period_idx,
                   share_prices,
                   vesting_schedule,
                   marginal_income_tax_rate):
    # TODO: add 83(b) case
    vesting_shares = vesting_schedule[vesting_period_idx]
    current_price_per_share = share_prices[vesting_period_idx]
    vesting_value = round(1.0 * vesting_shares * current_price_per_share, 2)
    income_tax = vesting_value * marginal_income_tax_rate
    return income_tax
