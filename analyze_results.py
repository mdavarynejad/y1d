#!/usr/bin/env python3
"""
Script to analyze and visualize backtesting results.
"""
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

import config


def load_results(results_dir=config.RESULTS_PATH):
    """Load all CSV result files from the results directory"""
    # Get all CSV files in the results directory
    csv_files = glob.glob(os.path.join(results_dir, "stats_*.csv"))
    
    if not csv_files:
        print(f"No result files found in {results_dir}")
        return None
    
    # Load and concatenate all results
    dfs = []
    for file in csv_files:
        df = pd.read_csv(file)
        # Add filename as a column for reference
        df['filename'] = os.path.basename(file)
        # Extract timestamp from filename
        df['timestamp'] = df['filename'].str.extract(r'stats_(\d{8}_\d{6})').iloc[0, 0]
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d_%H%M%S')
        dfs.append(df)
    
    # Combine all dataframes
    all_results = pd.concat(dfs, ignore_index=True)
    return all_results


def plot_performance_metrics(results_df):
    """Plot key performance metrics from results"""
    if results_df is None or results_df.empty:
        print("No results to plot")
        return
    
    # Create a figure with multiple subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(f"{config.TICKER} Buy-Before-Open Strategy Performance", fontsize=16)
    
    # Plot Return
    axes[0, 0].bar(results_df['timestamp'], results_df['Return [%]'], color='green')
    axes[0, 0].set_title('Total Return (%)')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Plot Sharpe Ratio
    axes[0, 1].bar(results_df['timestamp'], results_df['Sharpe Ratio'], color='blue')
    axes[0, 1].set_title('Sharpe Ratio')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # Plot Max Drawdown
    axes[1, 0].bar(results_df['timestamp'], results_df['Max. Drawdown [%]'], color='red')
    axes[1, 0].set_title('Max Drawdown (%)')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # Plot Win Rate
    axes[1, 1].bar(results_df['timestamp'], results_df['Win Rate [%]'], color='purple')
    axes[1, 1].set_title('Win Rate (%)')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    # Save the figure
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join(config.RESULTS_PATH, f"performance_metrics_{timestamp}.png")
    plt.savefig(save_path)
    print(f"Performance metrics plot saved to {save_path}")
    
    # Show the plot
    plt.show()


def analyze_trades(results_df):
    """Analyze trading statistics and print summary"""
    if results_df is None or results_df.empty:
        print("No results to analyze")
        return None
    
    # Calculate average metrics
    avg_return = results_df['Return [%]'].mean()
    avg_sharpe = results_df['Sharpe Ratio'].mean()
    avg_drawdown = results_df['Max. Drawdown [%]'].mean()
    avg_win_rate = results_df['Win Rate [%]'].mean()
    avg_trades = results_df['# Trades'].mean()
    
    # Print summary statistics
    print("\n=== Trading Strategy Analysis ===")
    print(f"Strategy: Buy ${config.INVESTMENT_AMOUNT} of {config.TICKER} before market open, sell at open")
    print(f"Lookback Period: {config.LOOKBACK_YEARS} years")
    print("\nAverage Performance Metrics:")
    print(f"  - Average Return: {avg_return:.2f}%")
    print(f"  - Average Sharpe Ratio: {avg_sharpe:.2f}")
    print(f"  - Average Max Drawdown: {avg_drawdown:.2f}%")
    print(f"  - Average Win Rate: {avg_win_rate:.2f}%")
    print(f"  - Average Number of Trades: {avg_trades:.0f}")
    
    # Compile stats into a dictionary
    stats_summary = {
        'avg_return': avg_return,
        'avg_sharpe': avg_sharpe,
        'avg_drawdown': avg_drawdown,
        'avg_win_rate': avg_win_rate,
        'avg_trades': avg_trades,
        'ticker': config.TICKER,
        'investment_amount': config.INVESTMENT_AMOUNT,
        'lookback_years': config.LOOKBACK_YEARS,
        'num_backtests': len(results_df),
        'analysis_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save the summary stats to a CSV file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_file = os.path.join(config.RESULTS_PATH, f"strategy_summary_{timestamp}.csv")
    pd.DataFrame([stats_summary]).to_csv(summary_file, index=False)
    print(f"Strategy summary saved to {summary_file}")
    
    return stats_summary


def main():
    """Main function to analyze results"""
    # Ensure results directory exists
    if not os.path.exists(config.RESULTS_PATH):
        os.makedirs(config.RESULTS_PATH)
        print(f"Created results directory: {config.RESULTS_PATH}")
        print("No backtest results found. Run the backtest first.")
        return
    
    # Load results
    results = load_results()
    
    if results is not None and not results.empty:
        # Analyze trades and save summary to file
        analyze_trades(results)
        
        # Plot performance metrics
        plot_performance_metrics(results)
    

if __name__ == "__main__":
    main() 