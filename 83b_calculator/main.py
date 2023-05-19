from calculator import Calculator
import pprint


"""
    I want...
    
    Input...
    - several probability-weighted price paths
    - several probability-weighted tenure paths
    - interest rate path or equity opportunity cost
    
    Output...
    - wavg NPV of the 83(b) election

    Value of the 83(b) election is...
    - yes-83(b) minus no-83(b)
    - discount cash flows to present value 
    - NPV   
"""


def main():
    MARGINAL_INCOME_TAX_RATE = 0.37
    MARGINAL_LONG_TERM_CAPITAL_GAINS_RATE = 0.23
    SHARE_PRICES = [0.01, 0.05, 0.25, 1.25, 2.45, 5.00]
    VESTING_SCHEDULE = [0, 25_000, 25_000, 25_000, 25_000, 0]
    VESTING_PERIOD_IDX = 4

    calculator = Calculator()
    no83b = calculator.run(
        MARGINAL_INCOME_TAX_RATE,
        MARGINAL_LONG_TERM_CAPITAL_GAINS_RATE,
        SHARE_PRICES,
        VESTING_SCHEDULE,
        False,
        VESTING_PERIOD_IDX
    )
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(no83b)

    yes83b = calculator.run(
        MARGINAL_INCOME_TAX_RATE,
        MARGINAL_LONG_TERM_CAPITAL_GAINS_RATE,
        SHARE_PRICES,
        VESTING_SCHEDULE,
        True,
        VESTING_PERIOD_IDX
    )

    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(yes83b)


main()
