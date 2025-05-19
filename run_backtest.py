#!/usr/bin/env python3
"""
Main script to run the "Buy Before Open, Sell At Open" strategy backtesting.
"""
import argparse
import os
from datetime import datetime

import config
from backtest_strategy import run_backtest


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Backtest the 'Buy Before Open, Sell At Open' trading strategy."
    )
    parser.add_argument(
        "--ticker",
        type=str,
        default=config.TICKER,
        help=f"Ticker symbol to backtest (default: {config.TICKER})"
    )
    parser.add_argument(
        "--investment",
        type=float,
        default=config.INVESTMENT_AMOUNT,
        help=f"Investment amount in USD (default: {config.INVESTMENT_AMOUNT})"
    )
    parser.add_argument(
        "--years",
        type=int,
        default=config.LOOKBACK_YEARS,
        help=f"Number of years to look back (default: {config.LOOKBACK_YEARS})"
    )
    parser.add_argument(
        "--no-visualize",
        action="store_true",
        help="Disable result visualization"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Disable saving results"
    )
    
    return parser.parse_args()


def main():
    """Main function to run the backtest"""
    # Parse command line arguments
    args = parse_arguments()
    
    # Update config with any command line overrides
    config.TICKER = args.ticker
    config.INVESTMENT_AMOUNT = args.investment
    config.LOOKBACK_YEARS = args.years
    
    print(f"Running backtest for {config.TICKER} with ${config.INVESTMENT_AMOUNT} "
          f"investment over {config.LOOKBACK_YEARS} years")
    
    # Create results directory if it doesn't exist and we're saving results
    if not args.no_save and not os.path.exists(config.RESULTS_PATH):
        os.makedirs(config.RESULTS_PATH)
    
    # Run the backtest
    stats = run_backtest(
        visualize=not args.no_visualize,
        save_results=not args.no_save
    )
    
    # Print key statistics
    print("\nBacktest Results Summary:")
    print(f"Total Return: {stats['Return [%]']:.2f}%")
    print(f"Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
    print(f"Max Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
    print(f"Win Rate: {stats['Win Rate [%]']:.2f}%")
    print(f"# Trades: {stats['# Trades']}")
    

if __name__ == "__main__":
    main() 