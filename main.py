from pprint import pp

from src.execute.simulate import (  
    run_scenario, EmployeePurchase, Scenario, ScenarioMetadata)
from src.events.employment_event import EmploymentType


def main():
    metadata = ScenarioMetadata(
        marginal_income_tax_rate=0.37,
        marginal_long_term_capital_gains_rate=0.20,
        discount_rate=0.06
    )

    scenario = Scenario(
        vesting_schedule=[0, 25_000, 25_000, 25_000, 25_000, 0],
        share_price_process=[0.01, 0.05, 0.25, 1.25, 2.45, 5.00],
        employment_process=[EmploymentType.EMPLOYED] * 6
    )

    results = run_scenario(scenario, metadata)


main()
