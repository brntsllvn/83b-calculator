from pprint import pp

from src.execute.simulate import run_scenario


def main():
    marginal_income_tax_rate = 0.37
    marginal_long_term_capital_gains_rate = 0.20
    discount_rate = 0.06
    # vesting_schedule = [0, 25_000, 25_000, 25_000, 25_000, 0]
    # share_price_process = [0.01, 0.05, 0.25, 1.25, 2.45, 5.00]
    # vesting_schedule = [0, 100_000, 0]
    # share_price_process = [0.01, 1.00, 5.00]

    results = run_scenario(marginal_income_tax_rate,
                           marginal_long_term_capital_gains_rate,
                           discount_rate,
                           share_grant_count,
                           employee_purchase,
                           vesting_schedule,
                           share_price_process)
    pp(results, depth=2, indent=4)


main()