# quant-backtester

A high-performance backtesting engine for various algorithmic trading strategies. This project provides an event-driven simulation framework to test and optimize trading strategies using historical market data. Supports multiple strategies, order execution logic, and portfolio performance analysis.

## Features

- **Backtesting Engine**: Simulate algorithmic trading strategies using historical OHLCV data.
- **Multiple Strategies Supported**:
  - Moving Average Trend Following
  - RSI Mean Reversion
  - Bollinger Bands Mean Reversion
  - Pairs Trading (based on price spread z-score between two assets)
  - Buy and Hold baseline
- **Trade Simulation**: Executes trades based on strategy signals and tracks portfolio value.
- **Data Management**: Download and cache Yahoo Finance data; loads from local files if already downloaded.
- **Visualization**: Price charts with strategy-specific overlays (e.g., moving averages, bands, signal markers) and portfolio value plots.
- **Command-Line Interface**: Easily configure strategy parameters, tickers, and date ranges.

## Installation

```bash
git clone https://github.com/Dam4n/quant-backtester.git
cd quant-backtester
pip install -r requirements.txt
```

## Usage

### 1. **Download Historical Data**

```python
from utils.utils import get_data
get_data(['AAPL'], '2023-01-01', '2023-12-31')
```

### 2. **Run a Strategy Backtest**

```bash
python backtest.py --ticker AAPL --start 2023-01-01 --end 2023-12-31 --strategy trend_following
```

To run **pairs trading**, include a second ticker:

```bash
python backtest.py --ticker RIVN --pair-ticker AMZN --start 2024-01-01 --end 2024-12-31 --strategy pairs
```

### 3. **Compare Multiple Strategies**

```bash
python compare_strategies.py --ticker AAPL --start 2023-01-01 --end 2023-12-31
```

(Optionally add `--pair-ticker` to include Pairs Trading in the comparison.)

## Strategy Customization

Adjust parameters using command-line arguments:

- Moving Average: `--short-window`, `--long-window`
- RSI: `--rsi-period`, `--rsi-lower`, `--rsi-upper`
- Bollinger Bands: `--bollinger-window`, `--bollinger-std`

## File Overview

- `backtest.py`: Backtests a single strategy with visual signal overlays.
- `compare_strategies.py`: Compares portfolio performance across multiple strategies.
- `utils/`: Data loading and caching utilities.
- `strategies/`: Contains individual strategy implementations.
- `execution/`: Simulates trade execution and cash flow tracking.
- `metrics/`: Computes performance metrics like total return, Sharpe ratio, and drawdown.

## Visual Outputs

- **Signal Overlay Plot**: Displays strategy-specific signals (e.g., RSI thresholds, MA crossovers, Bollinger Bands, Pairs z-score divergences).
- **Portfolio Performance Plot**: Visualizes how your capital changes over time with each strategy.

## Example Output

- Buy/Sell signals marked with green (buy) and red (sell) arrows.
- Bollinger Bands and Moving Averages shown as dashed overlays.
- Portfolio value line chart overlaid on time axis.
- Console output of performance metrics including total return, Sharpe ratio, and max drawdown.

## Contributing

Contributions welcome! Submit a pull request, file an issue, or fork the project.

## License

MIT License - see the [LICENSE](LICENSE) file for details.

---
