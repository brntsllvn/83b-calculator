import json

from src.execute.simulate import (
    run_scenario, EmployeePurchase, ScenarioMetadata, Scenario)
from src.events.portfolio_event import PortfolioEventType, PortfolioEvent
from src.events.tax_event import TaxEvent, TaxType
from src.events.employment_event import EmploymentType

"""
    https://www.irs.gov/irb/2012-28_IRB#RR-2012-19
    Example 1: 83(b), employee pays FMV at grant
    Example 2: No 83(b), employee pays FMV at grant
"""


"""
    Additional cases:
    - 83(b): Employee pays FMV at grant, vests a fraction, is terminated, company repurchases
    - Cooley examples: 
    -- 3 year:
        vesting_schedule = [0, 100_000, 0]
        share_price_process = [0.01, 1.00, 5.00]
    -- 6 year:
        vesting_schedule = [0, 25_000, 25_000, 25_000, 25_000, 0]
        share_price_process = [0.01, 0.05, 0.25, 1.25, 2.45, 5.00]
"""


def test_simulate_irb_2012_28_examples_1_2():
    metadata = ScenarioMetadata(
        marginal_income_tax_rate=0.37,
        marginal_long_term_capital_gains_rate=0.20,
        discount_rate=0.06
    )

    scenario = Scenario(
        vesting_schedule=[0, 0, 25_000, 0],
        share_price_process=[1, 1, 1.6, 2.4],
        employment_process=[EmploymentType.EMPLOYED] * 4,
        employee_purchase=EmployeePurchase(1, 25_000)
    )

    results = run_scenario(scenario, metadata)

    yes_83b_result = results.file_83b_result

    yes_83b_share_events = yes_83b_result.share_events
    assert len(yes_83b_share_events) == 4
    assert yes_83b_share_events[0] == PortfolioEvent(
        0, PortfolioEventType.GRANT, 25_000
    )
    assert yes_83b_share_events[1] == PortfolioEvent(
        0, PortfolioEventType.PURCHASE, 25_000
    )
    assert yes_83b_share_events[2] == PortfolioEvent(
        2, PortfolioEventType.VEST, 25_000
    )
    assert yes_83b_share_events[3] == PortfolioEvent(
        3, PortfolioEventType.SALE, 25_000
    )

    yes_83b_tax_events = yes_83b_result.tax_events
    assert len(yes_83b_tax_events) == 1
    assert yes_83b_tax_events[0] == TaxEvent(
        3, 35_000, TaxType.CAPITAL_GAINS_LONG_TERM, 7_000)

    no_83b_result = results.forgo_83b_result
    no_83b_share_events = no_83b_result.share_events
    assert len(no_83b_share_events) == 4
    assert no_83b_share_events[0] == PortfolioEvent(
        0, PortfolioEventType.GRANT, 25_000
    )
    assert no_83b_share_events[1] == PortfolioEvent(
        0, PortfolioEventType.PURCHASE, 25_000
    )
    assert no_83b_share_events[2] == PortfolioEvent(
        2, PortfolioEventType.VEST, 25_000
    )
    assert no_83b_share_events[3] == PortfolioEvent(
        3, PortfolioEventType.SALE, 25_000
    )

    no_83b_tax_events = no_83b_result.tax_events
    assert len(no_83b_tax_events) == 2
    assert no_83b_tax_events[0] == TaxEvent(2, 15_000, TaxType.INCOME, 5_550)
    assert no_83b_tax_events[1] == TaxEvent(
        3, 20_000, TaxType.CAPITAL_GAINS_LONG_TERM, 4_000)

    election_83b_value = results.election_83b_value
    assert election_83b_value.tax_diff_process == [
        0.0, 0.0, 5550.0, -3000.0]
    assert election_83b_value.raw_dollars == 2550.0
    assert election_83b_value.npv_dollars == 2420.62


"""
    https://www.irs.gov/irb/2012-28_IRB#RR-2012-19
    Example 3: 83(b)
    1) employee pays FMV at grant
    2) termination before vest
    3) company repurchases
"""


def test_simulate_irb_2012_28_example_3():
    metadata = ScenarioMetadata(
        marginal_income_tax_rate=0.37,
        marginal_long_term_capital_gains_rate=0.20,
        discount_rate=0.06
    )

    scenario = Scenario(
        vesting_schedule=[0, 0, 25_000, 0],
        share_price_process=[1, 1, 1.6, 2.4],
        employment_process=[
            EmploymentType.EMPLOYED,
            EmploymentType.TERMINATED,
            EmploymentType.UNEMPLOYED,
            EmploymentType.UNEMPLOYED],
        employee_purchase=EmployeePurchase(1, 25_000)
    )

    results = run_scenario(scenario, metadata)

    yes_83b_result = results.file_83b_result

    yes_83b_share_events = yes_83b_result.share_events
    assert len(yes_83b_share_events) == 3
    assert yes_83b_share_events[0] == PortfolioEvent(
        0, PortfolioEventType.GRANT, 25_000
    )
    assert yes_83b_share_events[1] == PortfolioEvent(
        0, PortfolioEventType.PURCHASE, 25_000
    )
    assert yes_83b_share_events[2] == PortfolioEvent(
        1, PortfolioEventType.REPURCHASE, 25_000
    )

    yes_83b_tax_events = yes_83b_result.tax_events
    assert len(yes_83b_tax_events) == 0

    no_83b_result = results.forgo_83b_result
    no_83b_share_events = no_83b_result.share_events
    assert len(no_83b_share_events) == 3
    assert no_83b_share_events[0] == PortfolioEvent(
        0, PortfolioEventType.GRANT, 25_000
    )
    assert no_83b_share_events[1] == PortfolioEvent(
        0, PortfolioEventType.PURCHASE, 25_000
    )
    assert yes_83b_share_events[2] == PortfolioEvent(
        1, PortfolioEventType.REPURCHASE, 25_000
    )

    no_83b_tax_events = no_83b_result.tax_events
    assert len(no_83b_tax_events) == 0

    election_83b_value = results.election_83b_value
    assert election_83b_value.tax_diff_process == [
        0.0, 0.0, 0.0, 0.0]
    assert election_83b_value.raw_dollars == 0
    assert election_83b_value.npv_dollars == 0


"""
    https://www.irs.gov/irb/2012-28_IRB#RR-2012-19
    Example 4: 83(b)
    Example 5: No 83(b)
"""


def test_simulate_irb_2012_28_examples_4_5():
    metadata = ScenarioMetadata(
        marginal_income_tax_rate=0.37,
        marginal_long_term_capital_gains_rate=0.20,
        discount_rate=0.06
    )

    scenario = Scenario(
        vesting_schedule=[0, 0, 25_000, 0],
        share_price_process=[1, 1, 1.6, 2.4],
        employment_process=[
            EmploymentType.EMPLOYED,
            EmploymentType.EMPLOYED,
            EmploymentType.EMPLOYED,
            EmploymentType.EMPLOYED],
        employee_purchase=EmployeePurchase(0, 0)
    )

    results = run_scenario(scenario, metadata)

    yes_83b_result = results.file_83b_result

    yes_83b_share_events = yes_83b_result.share_events
    assert len(yes_83b_share_events) == 3
    assert yes_83b_share_events[0] == PortfolioEvent(
        0, PortfolioEventType.GRANT, 25_000
    )
    assert yes_83b_share_events[1] == PortfolioEvent(
        2, PortfolioEventType.VEST, 25_000
    )
    assert yes_83b_share_events[2] == PortfolioEvent(
        3, PortfolioEventType.SALE, 25_000
    )

    yes_83b_tax_events = yes_83b_result.tax_events
    assert len(yes_83b_tax_events) == 2
    assert yes_83b_tax_events[0] == TaxEvent(
        0, 25_000, TaxType.INCOME, 9_250)
    assert yes_83b_tax_events[1] == TaxEvent(
        3, 35_000, TaxType.CAPITAL_GAINS_LONG_TERM, 7_000)

    no_83b_result = results.forgo_83b_result

    no_83b_share_events = no_83b_result.share_events
    assert len(no_83b_share_events) == 3

    assert no_83b_share_events[0] == PortfolioEvent(
        0, PortfolioEventType.GRANT, 25_000
    )
    assert no_83b_share_events[1] == PortfolioEvent(
        2, PortfolioEventType.VEST, 25_000
    )
    assert no_83b_share_events[2] == PortfolioEvent(
        3, PortfolioEventType.SALE, 25_000
    )

    no_83b_tax_events = no_83b_result.tax_events
    assert len(no_83b_tax_events) == 2
    assert no_83b_tax_events[0] == TaxEvent(
        2, 40_000, TaxType.INCOME, 14_800)
    assert no_83b_tax_events[1] == TaxEvent(
        3, 20_000, TaxType.CAPITAL_GAINS_LONG_TERM, 4_000)

    election_83b_value = results.election_83b_value

    assert election_83b_value.tax_diff_process == [
        -9250.0, 0.0, 14800.0, -3000.0]
    assert election_83b_value.raw_dollars == 2550.0
    assert election_83b_value.npv_dollars == 1403.09


"""
    https://www.irs.gov/irb/2012-28_IRB#RR-2012-19
    Example 6: Terminated employment before vesting
"""


# def test_simulate_irb_2012_28_examples_6():
#     marginal_income_tax_rate = 0.37
#     marginal_long_term_capital_gains_rate = 0.20
#     discount_rate = 0.06
#     share_grant_count = 25_000
#     vesting_schedule = [0, 0, 0, 0]
#     employee_purchase = EmployeePurchase(0, 0)
#     share_price_process = [1, 1, 1.6, 2.4]
#     employment_process = [
#         EmploymentType.EMPLOYED,
#         EmploymentType.TERMINATED,
#         EmploymentType.UNEMPLOYED,
#         EmploymentType.UNEMPLOYED]

#     results = run_scenario(marginal_income_tax_rate,
#                            marginal_long_term_capital_gains_rate,
#                            discount_rate,
#                            share_grant_count,
#                            employee_purchase,
#                            vesting_schedule,
#                            share_price_process,
#                            employment_process)

#     yes_83b_events_and_lots = results.yes_83b_events_and_lots

#     yes_83b_vesting_events = yes_83b_events_and_lots.share_events
#     assert len(yes_83b_vesting_events) == 0

#     yes_83b_tax_events = yes_83b_events_and_lots.tax_events
#     assert len(yes_83b_tax_events) == 1
#     assert yes_83b_tax_events[0].time_idx == 0
#     assert yes_83b_tax_events[0].taxable_dollars == 25_000
#     assert yes_83b_tax_events[0].tax_type == TaxType.INCOME
#     assert yes_83b_tax_events[0].tax_dollars == 9_250

#     no_83b_events_and_lots = results.no_83b_events_and_lots

#     no_83b_vesting_events = no_83b_events_and_lots.share_events
#     assert len(no_83b_vesting_events) == 0

#     no_83b_tax_events = no_83b_events_and_lots.tax_events
#     assert len(no_83b_tax_events) == 0

#     election_83b_value = results.election_83b_value

#     assert election_83b_value.tax_diff_process == [
#         -9250.0, 0.0, 0.0, 0.0]
#     assert election_83b_value.raw_dollars == -9250.0
#     assert election_83b_value.npv_dollars == -9250.0
