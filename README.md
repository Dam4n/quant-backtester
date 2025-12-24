# Quantitative Trading Backtester

A modular Python framework for researching and evaluating systematic equity trading strategies using historical market data.
This project is designed as a **research and experimentation tool**, enabling strategy comparison, portfolio-level simulation, and performance analysis under clearly defined assumptions.

The focus is on **clarity, extensibility, and reproducibility**, rather than production-grade execution or latency modeling.

---

## Project Overview

This backtester provides a configurable environment to:

* Implement multiple quantitative trading strategies
* Simulate trade execution and portfolio evolution
* Compare strategy performance across common financial metrics
* Visualize signals, positions, and portfolio value over time

The framework supports **single-asset and multi-asset strategies**, including relative-value approaches such as pairs trading.

---

## Supported Strategies

* **Moving Average Trend Following**
* **RSI Mean Reversion**
* **Bollinger Bands Mean Reversion**
* **Pairs Trading** (price-spread z-score between two assets)
* **Buy-and-Hold** baseline for benchmarking

Each strategy is implemented as a modular component, allowing new strategies to be added with minimal changes to the execution and evaluation pipeline.

---

## Simulation Model & Assumptions

This backtester is intended for **research and comparative analysis**, not live trading.
Key modeling assumptions include:

* Trades are executed at historical bar prices (no intrabar modeling)
* No explicit transaction costs, slippage, or market impact
* No order book or latency simulation
* Capital is allocated at the portfolio level with simplified position sizing
* Strategies operate on historical OHLCV data

These assumptions allow rapid iteration and clean comparison, while keeping the framework extensible for future realism enhancements.

---

## Features

* **Backtesting Engine**: Simulates trading strategies using historical OHLCV market data
* **Portfolio-Level Simulation**: Tracks cash, positions, and total portfolio value over time
* **Strategy Comparison**: Run and compare multiple strategies over the same date range
* **Performance Metrics**:

  * Total return
  * Volatility
  * Sharpe ratio
  * Maximum drawdown
* **Data Management**: Downloads and caches Yahoo Finance data locally for reuse
* **Visualization**:

  * Price charts with strategy-specific overlays (moving averages, bands, signals)
  * Portfolio value time series
* **Command-Line Interface**: Configure tickers, strategies, and parameters without code changes

---

## Installation

```bash
git clone https://github.com/Dam4n/quant-backtester.git
cd quant-backtester
pip install -r requirements.txt
```

---

## Usage

### Download Historical Data

```python
from utils.utils import get_data
get_data(['AAPL'], '2023-01-01', '2023-12-31')
```

### Run a Single Strategy Backtest

```bash
python backtest.py --ticker AAPL --start 2023-01-01 --end 2023-12-31 --strategy trend_following
```

### Run Pairs Trading

```bash
python backtest.py --ticker RIVN --pair-ticker AMZN --start 2024-01-01 --end 2024-12-31 --strategy pairs
```

### Compare Multiple Strategies

```bash
python compare_strategies.py --ticker AAPL --start 2023-01-01 --end 2023-12-31
```

(Optionally include `--pair-ticker` to evaluate relative-value strategies.)

---

## Strategy Parameterization

Strategies can be tuned directly from the command line:

* **Moving Average**: `--short-window`, `--long-window`
* **RSI**: `--rsi-period`, `--rsi-lower`, `--rsi-upper`
* **Bollinger Bands**: `--bollinger-window`, `--bollinger-std`

This design supports rapid experimentation and parameter sensitivity analysis.

---

## Repository Structure

* `strategies/` — Individual trading strategy implementations
* `execution/` — Trade execution and cash flow simulation
* `metrics/` — Performance metric computation
* `utils/` — Data loading, caching, and shared utilities
* `backtest.py` — Runs a single strategy with signal visualization
* `compare_strategies.py` — Compares multiple strategies on the same dataset

---

## Example Outputs

* Buy and sell signals annotated on price charts
* Strategy-specific indicators (moving averages, Bollinger Bands, RSI)
* Portfolio value over time
* Console output summarizing performance metrics such as return, Sharpe ratio, and drawdown

---

## Future Extensions

Potential extensions include:

* Transaction cost and slippage modeling
* Rolling and risk-adjusted performance analytics
* Event-driven execution enhancements
* Multi-strategy portfolio allocation

---

## License

MIT License — see the [LICENSE](LICENSE) file for details.

---
