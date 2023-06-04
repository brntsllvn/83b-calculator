from src.domain.scenario import PortfolioEventData, TaxEventData, Metadata
from src.execute.scenario_runner import run_scenario


def main():
    portfolio_event_data = PortfolioEventData(
        vesting_schedule=[0, 25_000, 25_000, 25_000, 25_000, 0],
        termination_idx=-1
    )
    tax_event_data = TaxEventData(
        marginal_income_tax_rate=0.37,
        marginal_long_term_capital_gains_rate=0.20,
        share_price_process=[0.01, 0.05, 0.25, 1.25, 2.45, 5.00],
    )
    metadata = Metadata(
        discount_rate=0.06
    )

    return run_scenario(portfolio_event_data, tax_event_data, metadata)


main()
