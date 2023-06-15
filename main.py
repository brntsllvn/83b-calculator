from src.domain.scenario import PortfolioEventData, TaxEventData, Metadata
from src.execute.scenario_runner import run_scenario


def main():
    # portfolio_event_data = PortfolioEventData(
    #     vesting_schedule=[0, 25_000, 25_000, 25_000, 25_000, 0],
    #     termination_idx=-1,
    #     liqiudation_idx=5,
    # )
    # tax_event_data = TaxEventData(
    #     marginal_income_tax_rate=0.37,
    #     marginal_long_term_capital_gains_rate=0.20,
    #     share_price_process=[0.01, 0.05, 0.25, 1.25, 2.45, 5.00],
    # )
    # metadata = Metadata(
    #     discount_rate=0.06
    # )

    # return run_scenario(portfolio_event_data, tax_event_data, metadata)
    
    import matplotlib.pyplot as plt
    import numpy as np

    # Create some dummy data
    time = np.array(['2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06'])
    series1 = np.array([-10000.0, 0, 0, 0, 0, -99800.0])
    series2 = np.array([0, -462.5, -2312.5, -11562.5, -22662.5, -80000.0])

    x = np.arange(len(time))  # the label locations

    # Calculate the cumulative difference between series1 and series2
    cumulative_diff = np.cumsum(series1 - series2)

    # Create a figure and a set of subplots
    fig, ax = plt.subplots()

    # Add the bars for 'series1' and 'series2' at the respective 'time' positions
    rects1 = ax.bar(x - 0.2, series1, 0.4, label='File 83(b)', color='blue')
    rects2 = ax.bar(x + 0.2, series2, 0.4, label='Forgo 83(b)', color='green')

    # Add a line for the cumulative difference
    ax.plot(x, cumulative_diff, color='orange', label='Cumulative Difference')

    # Add a label to the final point on the cumulative sum line
    final_cumsum = cumulative_diff[-1]
    ax.text(x[-1], final_cumsum, f'Final CumSum: {final_cumsum:.2f}', va='bottom', ha='right')

    # Add labels, title and legend
    ax.set_xlabel('Time')
    ax.set_ylabel('Values')
    ax.set_title('Comparison of two time series and cumulative difference')
    ax.set_xticks(x)
    ax.set_xticklabels(time)
    ax.legend()

    # Save the figure to a file
    plt.savefig('chart.png')



main()
