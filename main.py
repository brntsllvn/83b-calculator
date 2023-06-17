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
    import matplotlib.dates as mdates
    import matplotlib.transforms as mtransforms
    import numpy as np
    import pandas as pd
    from datetime import datetime, timedelta

    # Reset style to default
    plt.rcParams.update(plt.rcParamsDefault)

    # Create dates for 6 periods
    dates = pd.date_range(datetime.now(), periods=6).tolist()

    # Generating random data for each of the series
    stock_price = np.abs(np.random.normal(100, 20, len(dates))) # Ensuring positive numbers
    employment = np.array([1, 1, 1, 1, 0, 0]) # Recession for the first 4 data points
    vesting = np.cumsum(np.random.choice([10,0], size=(len(dates),), p=[1./4, 3./4])) # accumulation step function
    comparison_series1 = -np.abs(np.random.normal(20, 5, len(dates))) # Negative numbers
    comparison_series2 = -np.abs(np.random.normal(20, 5, len(dates))) # Negative numbers

    # Create the figure and the different axes
    fig = plt.figure(figsize=(10, 14))
    ax0 = plt.subplot2grid((4, 1), (0, 0))
    ax1 = plt.subplot2grid((4, 1), (1, 0), sharex=ax0)
    ax2 = plt.subplot2grid((4, 1), (2, 0), sharex=ax0)

    # Plot the stock price
    ax0.plot(dates, stock_price, color='b', alpha=0.7, linewidth=2.5, label='Stock Price')
    ax0.set_ylim(bottom=0)  # Stock Price y-axis starts at $0

    # Create a 'recession' window on portfolio activity
    trans = mtransforms.blended_transform_factory(ax1.transData, ax1.transAxes)
    ax1.fill_between(dates, 0, 1, where=employment==1, facecolor='gray', alpha=0.3, transform=trans, zorder=0)

    # Plot the vesting schedule
    ax1.step(dates, vesting, color='r', alpha=1, linewidth=2.5, label='Wealth Events', zorder=1)
    ax1.set_ylim(bottom=0)  # Portfolio Activity y-axis starts at 0

    # Create bar chart for the comparison series
    ax2.bar(dates, comparison_series1, align='edge', width=0.15, label='Series 1', color='r', alpha=0.7)
    ax2.bar(dates, comparison_series2, align='edge', width=-0.15, label='Series 2', color='b', alpha=0.7)
    ax2.axhline(0, color='black', linewidth=0.6, linestyle='dashdot') # Thin black line at y=0

    # Set labels and legend
    for ax, label in zip([ax0, ax1, ax2], ['Stock Price', 'Wealth Events', 'Comparison Series']):
        ax.set_ylabel(label, fontsize=12, fontweight='bold')
        ax.legend(fontsize=10)

    ax2.set_xlabel('Date', fontsize=12, fontweight='bold')
    fig.autofmt_xdate()

    # Add table at the bottom of the figure
    table_ax = plt.subplot2grid((4, 1), (3, 0), sharex=ax0)
    data = np.round(np.random.rand(3, len(dates)), decimals=2)  # generate some random data for the table
    rows_labels = ['Row1', 'Row2', 'Row3']
    col_labels = [d.strftime('%Y-%m-%d') for d in dates]
    table_ax.axis('tight')
    table_ax.axis('off')
    table = table_ax.table(cellText=data, rowLabels=rows_labels, colLabels=col_labels, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)

    plt.tight_layout()

    # Save the figure to a file
    plt.savefig('chart.png')

main()
