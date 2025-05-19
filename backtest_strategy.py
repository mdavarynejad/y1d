from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import math

import config
from data_handling import get_data_for_backtesting

class BuyBeforeOpenSellAtOpen(Strategy):
    """
    Strategy: Buy $10,000 worth of TSLA shares at market close,
    and sell them at next day's market open.
    This should happen every trading day.
    """
    
    def init(self):
        """Initialize the strategy"""
        self.investment_amount = config.INVESTMENT_AMOUNT
    
    def next(self):
        """Define the trading logic for each bar"""
        # First, close any existing position at the open price
        if self.position:
            self.position.close()
        
        # Then, buy new shares at the close price for the next day
        price = self.data.Close[-1]  # Use close price for buying
        # Floor the number of shares to ensure it's a whole number
        num_shares = math.floor(self.investment_amount / price)
        
        # Only buy if we can afford at least 1 share
        if num_shares >= 1:
            self.buy(size=num_shares)


def run_backtest(visualize=True, save_results=True):
    """
    Run the backtesting with the configured strategy
    """
    # Get data for backtesting
    data = get_data_for_backtesting(
        config.TICKER, 
        config.DATA_GRANULARITY, 
        config.LOOKBACK_YEARS
    )
    
    # Set up and run the backtest
    bt = Backtest(
        data,
        BuyBeforeOpenSellAtOpen,
        cash=config.INITIAL_CASH,
        commission=config.COMMISSION_RATE,
        exclusive_orders=True
    )
    
    # Run the backtest
    stats = bt.run()
    print(stats)
    
    # Create results directory if it doesn't exist
    if save_results and not os.path.exists(config.RESULTS_PATH):
        os.makedirs(config.RESULTS_PATH)
    
    # Save stats to CSV
    if save_results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stats_df = pd.DataFrame([stats])
        stats_df.to_csv(f"{config.RESULTS_PATH}/stats_{timestamp}.csv", index=False)
    
    # Plot the results with Bokeh
    if visualize:
        try:
            filename = f"{config.RESULTS_PATH}/backtest_plot_{timestamp}.html" if save_results else None
            bt.plot(filename=filename)
            print(f"Interactive plot saved to {filename}" if filename else "Plot displayed")
        except Exception as e:
            print(f"Error: Unable to generate plot: {e}")
            print("Please make sure you have installed Bokeh version 2.4.3:")
            print("pip install bokeh==2.4.3")
            print("The backtest results are still valid and have been saved to CSV.")
    
    return stats


if __name__ == "__main__":
    run_backtest() 