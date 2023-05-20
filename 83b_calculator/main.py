import pprint

from execute.simulate import run_scenario

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
    marginal_income_tax_rate = 0.37
    marginal_long_term_capital_gains_rate = 0.20
    share_price_process = [0.01, 0.05, 0.25, 1.25, 2.45, 5.00]
    vesting_schedule = [0, 25_000, 25_000, 25_000, 25_000, 0]
    filed_83b_election = False

    results = run_scenario(marginal_income_tax_rate,
                           marginal_long_term_capital_gains_rate,
                           filed_83b_election,
                           vesting_schedule,
                           share_price_process)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(results)


main()
