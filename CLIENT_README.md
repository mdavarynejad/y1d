# Trading Strategy Framework for Move Tickers

## Overview

This repository provides a standardized framework for Move Tickers to test and evaluate trading strategies. It implements a modular backtesting environment using the `backtesting.py` package, allowing students to focus on strategy development rather than testing infrastructure.

## Purpose

At Move Tickers, we encourage students to explore diverse projects in the trading space, including:
- Time series analysis and pattern grouping
- Portfolio optimization techniques
- Development of novel trading strategies
- Market behavior modeling

Regardless of approach, empirical validation through backtesting represents a critical step in strategy development. This framework ensures that all strategies can be evaluated using consistent, industry-recognized metrics.

## Why Backtesting.py?

We've selected the `backtesting.py` package as our standard testing environment for several key reasons:

1. **Standardization**: Provides consistent performance metrics across different strategies
2. **Ease of Use**: Offers a clean API that lets students focus on strategy logic
3. **Platform Compatibility**: Seamlessly integrates with Move Tickers' existing systems
4. **Visualization Tools**: Generates clear performance visualizations with minimal effort
5. **Extensibility**: Allows for custom metrics and analysis when needed

## Key Performance Metrics

Every trading strategy requires rigorous evaluation. This framework automatically generates critical performance metrics:

| Metric | Description |
|--------|-------------|
| Return [%] | Total percentage return of the strategy |
| Return (Ann.) [%] | Annualized return percentage |
| Sharpe Ratio | Risk-adjusted performance measure |
| Sortino Ratio | Downside risk-adjusted performance |
| Max. Drawdown [%] | Largest peak-to-trough decline |
| Win Rate [%] | Percentage of profitable trades |
| # Trades | Total number of executed trades |

These metrics provide a comprehensive view of strategy performance beyond simple returns, allowing for nuanced comparison across different approaches.

## Implementation Benefits

By using this standardized framework, students can:

1. **Focus on Strategy Development**: Spend time on innovative ideas rather than testing infrastructure
2. **Ensure Consistency**: Compare different strategies using the same metrics and methodology
3. **Accelerate Development**: Build upon a working foundation rather than starting from scratch
4. **Meet Industry Standards**: Learn evaluation practices used by professional traders

## Framework Structure

```
trading-strategy/
├── config.py              # Configuration parameters
├── data_handling.py       # Data acquisition and processing
├── backtest_strategy.py   # Strategy implementation
├── run_backtest.py        # Execution script
├── analyze_results.py     # Results analysis and visualization
├── requirements.txt       # Dependencies
└── results/               # Output directory
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/mdavarynejad/y1d.git
cd y1d
```

### 2. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Default Strategy

```bash
python run_backtest.py
```

### 4. Analyze Results

```bash
python analyze_results.py
```

### 5. Develop Your Own Strategy

Create a new strategy class by inheriting from the `Strategy` base class:

```python
from backtesting import Strategy

class MyCustomStrategy(Strategy):
    def init(self):
        # Initialize indicators
        pass
        
    def next(self):
        # Define trading logic
        if condition:
            self.buy()
        elif another_condition:
            self.position.close()
```

## Conclusion

We believe this framework will significantly enhance the quality of student projects at Move Tickers while providing valuable experience with industry-standard tools and methodologies. By standardizing on the `backtesting.py` package, we ensure that strategies can be easily compared, validated, and integrated into our platform.

For any questions or support, please contact the Move Tickers team.

---

*Move Tickers - Empowering the next generation of quantitative traders* 