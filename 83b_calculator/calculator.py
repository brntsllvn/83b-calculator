from portfolio_report import PortfolioReport


class Calculator:
    def run(self):
        MARGINAL_INCOME_TAX_RATE = 0.37
        MARGINAL_LONG_TERM_CAPITAL_GAINS_RATE = 0.23
        SHARE_PRICES = [0.01, 0.05, 0.25, 1.25, 2.45, 5.00]
        VESTING_SCHEDULE = [0, 25_000, 25_000, 25_000, 25_000, 0]

        section_83b_election_filed = False
        vesting_period_idx = 1

        report = self.get_report(
            section_83b_election_filed,
            vesting_period_idx,
            SHARE_PRICES,
            VESTING_SCHEDULE
        )

        print(report)

    def get_report(self,
                   section_83b_election_filed,
                   vesting_period_idx,
                   share_prices,
                   vesting_schedule):
        return PortfolioReport(
            vesting_period_idx,
            1_000,
            1_000_000,
            400_000,
            [],
            25_000.01,
            10_001.99,
            3_334.55,
            1_200.23
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
