from calculator import Calculator


def main():
    MARGINAL_INCOME_TAX_RATE = 0.37
    MARGINAL_LONG_TERM_CAPITAL_GAINS_RATE = 0.23
    SHARE_PRICES = [0.01, 0.05, 0.25, 1.25, 2.45, 5.00]
    VESTING_SCHEDULE = [0, 25_000, 25_000, 25_000, 25_000, 0]
    SECTION_83B_FILED = False
    VESTING_PERIOD_IDX = 4

    calculator = Calculator()
    calculator.run(
        MARGINAL_INCOME_TAX_RATE,
        MARGINAL_LONG_TERM_CAPITAL_GAINS_RATE,
        SHARE_PRICES,
        VESTING_SCHEDULE,
        SECTION_83B_FILED,
        VESTING_PERIOD_IDX
    )


main()
