from reports.vesting import VestingReport
from reports.portfolio import PortfolioReport, get_portfolio_report
from reports.income_tax import IncomeTaxReport, get_income_tax_report


class Calculator:
    def run(self,
            marginal_income_tax_rate,
            marginal_capital_gains_rate,
            share_prices,
            vesting_schedule,
            section_83b_election_filed,
            vesting_period_idx):
        vesting_report = self.get_vesting_report(
            section_83b_election_filed,
            vesting_period_idx,
            share_prices,
            vesting_schedule,
            marginal_income_tax_rate
        )
        return vesting_report

    def get_vesting_report(self,
                           section_83b_election_filed,
                           vesting_period_idx,
                           share_prices,
                           vesting_schedule,
                           marginal_income_tax_rate):
        current_price_per_share = share_prices[vesting_period_idx]
        income_tax_report = get_income_tax_report(section_83b_election_filed,
                                                  vesting_period_idx,
                                                  share_prices,
                                                  vesting_schedule,
                                                  marginal_income_tax_rate)
        portfolio_report = get_portfolio_report(section_83b_election_filed,
                                                vesting_period_idx,
                                                share_prices,
                                                vesting_schedule)
        return VestingReport(
            vesting_period_idx,
            current_price_per_share,
            portfolio_report,
            income_tax_report
        )

    def get_vested_shares(self, vesting_schedule):
        vested_shares = []
        for idx, shares in enumerate(vesting_schedule):
            if idx == 0:
                vested_shares.append(0)
            else:
                accumulated_vested_shares = vested_shares[idx - 1]
                vested_shares.append(accumulated_vested_shares + shares)
        return vested_shares

    def get_unvested_shares(self, vesting_schedule):
        total_shares = sum(vesting_schedule)
        unvested_shares = []
        for idx, shares in enumerate(vesting_schedule):
            if idx == 0:
                unvested_shares.append(total_shares)
            else:
                accumulated_vested_shares = unvested_shares[idx - 1]
                unvested_shares.append(accumulated_vested_shares - shares)
        return unvested_shares

    def get_share_value(self, share_prices, shares):
        share_value = []
        for idx, price in enumerate(share_prices):
            share_value.append(round(1.0 * price * shares[idx], 2))
        return share_value

    def get_vested_lots(self, share_prices, vesting_schedule):
        vested_lots = []
        for idx, shares in enumerate(vesting_schedule):
            if shares != 0:
                vested_lots.append(
                    Lot(
                        vesting_schedule[idx],
                        share_prices[idx],
                        round(
                            1.0 * vesting_schedule[idx] * share_prices[idx], 2)
                    )
                )
        return vested_lots
