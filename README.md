# Trading Strategy Backtesting

This project provides a modular backtesting framework for evaluating trading strategies using historical stock data. The default implementation tests a "Buy at Close, Sell at Next Day's Open" strategy with Tesla (TSLA) stock data over the past 5 years.

## Strategy Description

The default strategy is simple:
1. Buy $10,000 worth of TSLA shares at market close
2. Sell all shares at the next day's market open
3. Repeat daily for each trading day

## VM Setup for Ubuntu 22.04

### Option 1: Cloud Provider (DigitalOcean, AWS, etc.)
1. Create an account with your preferred cloud provider
2. Create a new VM with Ubuntu 22.04 LTS (minimum 4GB RAM recommended)
3. Set up SSH access to your VM
4. Log in to your VM via SSH

### Option 2: VirtualBox (Local Setup)
1. Download VirtualBox from [virtualbox.org](https://www.virtualbox.org/wiki/Downloads)
2. Download Ubuntu 22.04 ISO from [ubuntu.com](https://ubuntu.com/download/desktop)
3. Open VirtualBox and click "New"
4. Name your VM "TradingBacktest" and select:
   - Type: Linux
   - Version: Ubuntu 64-bit
5. Allocate at least 4GB RAM
6. Create a virtual hard disk (25GB minimum)
7. Start the VM and select the Ubuntu ISO file when prompted
8. Follow the Ubuntu installation prompts
9. After installation completes, reboot your VM

### Initial System Setup
```bash
# Update package lists
sudo apt update && sudo apt upgrade -y

# Install essential tools
sudo apt install -y python3 python3-pip python3-venv git
```

## Setup

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

### Installation

1. Clone this repository
```bash
git clone https://github.com/mdavarynejad/y1d.git
cd y1d
```

2. Create and activate a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the required packages
```bash
pip install -r requirements.txt
```

4. Create results directory if it doesn't exist
```bash
mkdir -p results
```

### Package Versioning and Stability

This project uses specific versions for critical dependencies to ensure compatibility:

- **Bokeh 2.4.3**: The visualization library must be this specific version to work correctly with the backtesting package
- Other packages use flexible versioning constraints with upper bounds to prevent breaking changes

If you encounter visualization errors, ensure you have the correct Bokeh version:
```bash
pip install bokeh==2.4.3
```

If you need absolute stability, you can create a pinned requirements file with exact versions:

```bash
# Create a pinned requirements file with exact versions
pip freeze > requirements-frozen.txt
```

To update to the latest compatible versions (except for Bokeh which must remain at 2.4.3):

```bash
# Update packages to latest compatible versions
pip install --upgrade -r requirements.txt
```

For advanced dependency management, consider using tools like `pip-tools` or `poetry`:

```bash
# Using pip-tools
pip install pip-tools
pip-compile requirements.txt  # Creates requirements.txt with exact versions
pip-sync                      # Installs exactly what's in requirements.txt
```

## Creating Custom Trading Strategies

The framework is designed to be modular, allowing you to easily plug in your own trading strategies. Here's how to create and use your own strategy:

### Strategy Class Structure

All strategies must inherit from the `Strategy` class provided by the `backtesting` package. Each strategy requires two key methods:

1. `init()`: Called once at the start of the backtest to initialize indicators or variables
2. `next()`: Called for each new data point (e.g., daily) to make trading decisions

### Example: Create a Custom Strategy

Create a new file named `my_strategy.py` with your strategy implementation:

```python
from backtesting import Strategy
from backtesting.lib import crossover
import config

class MyCustomStrategy(Strategy):
    """
    Your custom trading strategy description here.
    Example: Simple Moving Average Crossover Strategy
    """
    
    # Define parameters that can be optimized
    n1 = 20  # Fast moving average period
    n2 = 50  # Slow moving average period
    
    def init(self):
        """Initialize strategy indicators"""
        # Calculate moving averages
        self.sma1 = self.I(lambda: self.data.Close.rolling(self.n1).mean())
        self.sma2 = self.I(lambda: self.data.Close.rolling(self.n2).mean())
    
    def next(self):
        """Define trading logic for each bar"""
        # Buy when fast MA crosses above slow MA
        if crossover(self.sma1, self.sma2):
            self.buy()
            
        # Sell when fast MA crosses below slow MA
        elif crossover(self.sma2, self.sma1):
            self.position.close()
```

### Integrating Your Strategy

To use your custom strategy in the backtesting framework:

1. Import your strategy into `backtest_strategy.py` or create a new runner script:

```python
from backtesting import Backtest
from my_strategy import MyCustomStrategy
from data_handling import get_data_for_backtesting
import config
import os
from datetime import datetime
import pandas as pd

def run_my_strategy(visualize=True, save_results=True):
    """Run backtesting with your custom strategy"""
    # Get data for backtesting
    data = get_data_for_backtesting(
        config.TICKER,
        config.DATA_GRANULARITY,
        config.LOOKBACK_YEARS
    )
    
    # Set up and run the backtest
    bt = Backtest(
        data,
        MyCustomStrategy,  # Use your custom strategy here
        cash=config.INITIAL_CASH,
        commission=config.COMMISSION_RATE,
        exclusive_orders=True
    )
    
    # Run the backtest
    stats = bt.run()
    print(stats)
    
    # Save and visualize results (same as original code)
    # ...
    
    return stats

if __name__ == "__main__":
    run_my_strategy()
```

2. Create a command-line interface for your strategy (optional):

```python
#!/usr/bin/env python3
"""
Main script to run custom trading strategy backtesting.
"""
import argparse
import config
from my_custom_backtest import run_my_strategy

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Backtest custom trading strategy."
    )
    # Add your strategy-specific parameters
    parser.add_argument(
        "--fast-ma",
        type=int,
        default=20,
        help="Fast moving average period"
    )
    parser.add_argument(
        "--slow-ma",
        type=int,
        default=50,
        help="Slow moving average period"
    )
    # Add common parameters
    parser.add_argument(
        "--ticker",
        type=str,
        default=config.TICKER,
        help=f"Ticker symbol to backtest (default: {config.TICKER})"
    )
    # ... other common parameters ...
    
    return parser.parse_args()

def main():
    """Main function to run the backtest"""
    args = parse_arguments()
    
    # Update config with command line arguments
    config.TICKER = args.ticker
    # ... other config updates ...
    
    # Run your strategy
    stats = run_my_strategy()
    
    # Print results
    print("\nBacktest Results Summary:")
    print(f"Total Return: {stats['Return [%]']:.2f}%")
    # ... other metrics ...

if __name__ == "__main__":
    main()
```

### Advanced: Strategy Optimization

You can optimize your strategy parameters using the `backtesting` library's optimization features:

```python
# Optimize strategy parameters
stats = bt.optimize(
    n1=range(10, 30, 5),     # Test fast MA from 10 to 30 in steps of 5
    n2=range(40, 100, 10),   # Test slow MA from 40 to 100 in steps of 10
    maximize='Sharpe Ratio',  # Maximize the Sharpe ratio
    constraint=lambda p: p.n1 < p.n2  # Ensure fast MA is shorter than slow MA
)
```

## Usage

### Running the Default Backtest

To run the backtest with default parameters:

```bash
python run_backtest.py
```

### Running Your Custom Strategy

```bash
python run_my_strategy.py --fast-ma 15 --slow-ma 45 --ticker GOOG
```

### Command Line Options

You can customize the backtest with the following options:

```bash
python run_backtest.py --ticker TSLA --investment 10000 --years 5
```

Common options:
- `--ticker`: Stock ticker symbol (default: TSLA)
- `--investment`: Investment amount in USD (default: 10000)
- `--years`: Number of years to look back (default: 5)
- `--no-visualize`: Disable result visualization
- `--no-save`: Disable saving results

### Analyzing Results

After running one or more backtests, you can analyze the results:

```bash
python analyze_results.py
```

This will generate performance metrics charts and provide statistical analysis of the trading strategy.

## Project Structure

- `config.py`: Configuration parameters for the strategy
- `data_handling.py`: Functions for fetching and processing stock data
- `backtest_strategy.py`: Implementation of the default trading strategy
- `run_backtest.py`: Main script to execute backtests
- `analyze_results.py`: Tools for analyzing backtest results across multiple runs (see details below)
- `requirements.txt`: Python dependencies
- `results/`: Directory for storing backtest results
- `my_strategy.py`: Your custom strategy implementation (create this)
- `run_my_strategy.py`: Runner for your custom strategy (create this)

### Why analyze_results.py is Necessary

While the backtesting package does provide performance metrics and visualization for individual backtest runs, `analyze_results.py` extends these capabilities with several critical features:

1. **Aggregation of Multiple Runs**: It loads and analyzes results from multiple backtest runs stored in the results directory, allowing you to compare different strategies or parameter sets.

2. **Historical Comparison**: It tracks performance over time by loading saved results from previous runs, enabling you to see how your strategy evolves as you refine it.

3. **Custom Visualizations**: It creates specialized charts that compare key performance metrics (Return, Sharpe Ratio, Drawdown, Win Rate) across different runs or parameter sets in a single view.

4. **Statistical Analysis**: It calculates average metrics across multiple runs to provide a more robust assessment of strategy performance:
   ```python
   # Calculate average metrics
   avg_return = results_df['Return [%]'].mean()
   avg_sharpe = results_df['Sharpe Ratio'].mean()
   ```

5. **Persistence Management**: It handles loading saved results from disk, making it possible to analyze backtest performance days or weeks after the initial runs.

Without `analyze_results.py`, you would only be able to see results from your most recent run, making it difficult to compare strategies, track improvements as you modify parameters, or see how a strategy performs across different market conditions.

## Performance Metrics

The backtesting framework provides various performance metrics, including:

- Total Return (%)
- Sharpe Ratio
- Maximum Drawdown (%)
- Win Rate (%)
- Number of Trades

## Troubleshooting

### Display Issues with Matplotlib
If you're running in a headless environment or encounter display issues:
```bash
export MPLBACKEND=Agg
```
This will save plots to files instead of attempting to display them.

### Bokeh Visualization Issues
The backtesting package requires Bokeh version 2.4.3 specifically. If you see errors like:
```
ValueError: failed to validate DatetimeTickFormatter(...).days: expected a value of type str
```
Install the correct version:
```bash
pip install bokeh==2.4.3
```

This is already specified in the requirements.txt file, but if you're having issues, you can reinstall it directly.

### Viewing HTML Plot Files
After running the backtest, an interactive HTML file is created in the results directory. To view it:

1. If running locally: Simply open the HTML file in any web browser
2. If running on a remote server: Either:
   - Copy the file to your local machine: `scp username@vm-ip-address:~/y1d/results/*.html ./`
   - Start a simple HTTP server: `python -m http.server 8080` and access via browser

### Network Issues
Ensure your VM has internet access to fetch stock data:
```bash
ping -c 4 google.com
```

### Permission Issues
If you encounter permission problems:
```bash
sudo chown -R $USER:$USER ~/y1d
```

### Accessing Results from Local Machine
If using a remote VM, copy results to your local machine:
```bash
# On your local machine
scp -r username@vm-ip-address:~/y1d/results/ ./local-results/
```

### Package Compatibility Issues

If you encounter compatibility issues with other packages:

1. Make sure Bokeh is at version 2.4.3:
   ```bash
   pip install bokeh==2.4.3
   ```

2. Try reverting to known working versions:
   ```bash
   # Install specific versions known to work
   pip install pandas==2.0.3 numpy==1.24.4 backtesting==0.3.3
   ```

3. Check for deprecation warnings that might indicate future issues:
   ```bash
   python -W always run_backtest.py
   ```

## Usage Instructions

Follow these steps:

1. Set up your VM following the instructions above
2. Clone this repository and install dependencies
3. Run the default backtest to familiarize yourself with the strategy
4. Create your own custom trading strategy by following the examples
5. Run and optimize your strategy, analyzing its performance
6. Write a report comparing your strategy with the default strategy