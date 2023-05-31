def test_simulate_irb_2012_28_examples_1_2():
    tax_event_data = TaxEventData(
        marginal_income_tax_rate=0.37,
        marginal_long_term_capital_gains_rate=0.20,
        share_price_process=[1, 1, 1.6, 2.4],
        discount_rate=0.06
    )

    portfolio_event_data = PortfolioEventData(
        vesting_schedule=[0, 0, 25_000, 0],
        employment_process=[EmploymentType.EMPLOYED] * 4,
        employee_purchase=EmployeePurchase(1, 25_000)
    )

    portfolio_events = get_portfolio_events(True, portfolio_event_data)
    assert False
