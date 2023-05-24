import json

from src.execute.simulate import run_scenario


def test_simulate():
    marginal_income_tax_rate = 0.37
    marginal_long_term_capital_gains_rate = 0.20
    discount_rate = 0.06
    vesting_schedule = [0, 0, 25_000, 0]
    share_price_process = [1, 1, 1.6, 2.4]

    results = run_scenario(marginal_income_tax_rate,
                           marginal_long_term_capital_gains_rate,
                           discount_rate,
                           vesting_schedule,
                           share_price_process)

    yes_83b_events_and_lots = results.yes_83b_events_and_lots

    yes_83b_vesting_events = yes_83b_events_and_lots.vesting_events
    assert len(yes_83b_vesting_events) == 1
    assert yes_83b_vesting_events[0].time_idx == 2
    assert yes_83b_vesting_events[0].share_count == 25_000

    yes_83b_lots = yes_83b_events_and_lots.lots
    assert len(yes_83b_lots) == 1
    assert yes_83b_lots[0].time_idx == 2
    assert yes_83b_lots[0].share_count == 25_000
    assert yes_83b_lots[0].basis_per_share == 1

    yes_83b_tax_events = yes_83b_events_and_lots.tax_events
    assert len(yes_83b_tax_events) == 2
    assert yes_83b_tax_events[0].time_idx == 0
    assert yes_83b_tax_events[0].taxable_amount == 25_000
    assert yes_83b_tax_events[0].tax_type == 1
    assert yes_83b_tax_events[0].tax_amount == 9_250
    assert yes_83b_tax_events[1].time_idx == 3
    assert yes_83b_tax_events[1].taxable_amount == 35_000
    assert yes_83b_tax_events[1].tax_type == 2
    assert yes_83b_tax_events[1].tax_amount == 7_000

    no_83b_events_and_lots = results.no_83b_events_and_lots

    no_83b_vesting_events = no_83b_events_and_lots.vesting_events
    assert len(no_83b_vesting_events) == 1
    no_83b_vesting_events[0].time_idx == 2
    no_83b_vesting_events[0].share_count == 25_000

    no_83b_lots = no_83b_events_and_lots.lots
    assert len(no_83b_lots) == 1
    assert no_83b_lots[0].time_idx == 2
    assert no_83b_lots[0].share_count == 25_000
    assert no_83b_lots[0].basis_per_share == 1.6

    no_83b_tax_events = no_83b_events_and_lots.tax_events
    assert len(no_83b_tax_events) == 2
    assert no_83b_tax_events[0].time_idx == 2
    assert no_83b_tax_events[0].taxable_amount == 40_000
    assert no_83b_tax_events[0].tax_type == 1
    assert no_83b_tax_events[0].tax_amount == 14_800
    assert no_83b_tax_events[1].time_idx == 3
    assert no_83b_tax_events[1].taxable_amount == 20_000
    assert no_83b_tax_events[1].tax_type == 2
    assert no_83b_tax_events[1].tax_amount == 4_000

    election_83b_value = results.election_83b_value

    assert election_83b_value.tax_diff_process == [
        -9250.0, 0.0, 14800.0, -3000.0]
    assert election_83b_value.raw == 2550.0
    assert election_83b_value.npv == 1403.09
