import argparse
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from utils.utils import get_data, load_data
from strategies.trend_following import moving_average_trend_following
from strategies.buy_and_hold import buy_and_hold
from strategies.mean_reversion import rsi_strategy, bollinger_band_strategy
from strategies.pairs_trading import pairs_trading_strategy
from execution.execution import simulate_trades
from metrics.metrics import calculate_performance_metrics

def plot_comparison(df_dict):
    """
    Plot portfolio value comparison across multiple strategies.
    """
    plt.figure(figsize=(14, 6))
    for label, df in df_dict.items():
        plt.plot(df.index, df['Portfolio Value'], label=label)

    valid_ranges = [df.dropna(subset=['Portfolio Value']).index for df in df_dict.values()]
    common_range = valid_ranges[0]
    for rng in valid_ranges[1:]:
        common_range = common_range.intersection(rng)

    if not common_range.empty:
        plt.xlim(common_range.min(), common_range.max())

    plt.title("Strategy Comparison - Portfolio Value Over Time")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value ($)")
    plt.legend()
    plt.grid(True)
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Compare performance of multiple trading strategies")
    parser.add_argument('--ticker', type=str, help='Ticker symbol', default='AAPL')
    parser.add_argument('--pair-ticker', type=str, help='Second ticker for pairs trading')
    parser.add_argument('--start', type=str, required=True, help='Start date in YYYY-MM-DD format')
    parser.add_argument('--end', type=str, required=True, help='End date in YYYY-MM-DD format')
    parser.add_argument('--initial-cash', type=float, default=10000, help='Initial portfolio value (default: 10000)')
    parser.add_argument('--short-window', type=int, default=10, help='Short window for moving average')
    parser.add_argument('--long-window', type=int, default=30, help='Long window for moving average')
    parser.add_argument('--rsi-period', type=int, default=14, help='RSI lookback period')
    parser.add_argument('--rsi-lower', type=int, default=30, help='RSI buy threshold')
    parser.add_argument('--rsi-upper', type=int, default=70, help='RSI sell threshold')
    parser.add_argument('--bollinger-window', type=int, default=20)
    parser.add_argument('--bollinger-std', type=float, default=2.0)
    parser.add_argument('--cost-bps', type=float, default=0.001, help='Transaction cost per trade (e.g. 0.001 = 10 bps)')

    args = parser.parse_args()

    print(f"Getting data for {args.ticker}...")
    get_data([args.ticker], args.start, args.end)

    df_main = load_data(args.ticker, args.start, args.end)

    if args.pair_ticker:
        print(f"Getting data for {args.pair_ticker}...")
        get_data([args.pair_ticker], args.start, args.end)
        df_pair = load_data(args.pair_ticker, args.start, args.end)
    else:
        df_pair = None

    strategy_funcs = {
        'Moving Average Trend Following': lambda df: moving_average_trend_following(
            df, short_window=args.short_window, long_window=args.long_window),
        'Buy and Hold': buy_and_hold,
        'RSI Strategy': lambda df: rsi_strategy(
            df, period=args.rsi_period, lower=args.rsi_lower, upper=args.rsi_upper),
        'Bollinger Bands': lambda df: bollinger_band_strategy(
            df, window=args.bollinger_window, num_std=args.bollinger_std),
    }

    if df_pair is not None:
        strategy_funcs['Pairs Trading'] = lambda df: pairs_trading_strategy(df, df_pair)

    results = {}
    metrics_summary = {}

    for name, strategy_func in strategy_funcs.items():
        print(f"\nRunning {name} strategy...")
        df = df_main.copy()
        df = strategy_func(df)
        df = simulate_trades(df, initial_cash=args.initial_cash, cost_bps=args.cost_bps)

        metrics = calculate_performance_metrics(df)
        results[name] = df
        metrics_summary[name] = metrics

    print("\n--- Performance Comparison ---")
    metrics_df = pd.DataFrame(metrics_summary).T
    print(metrics_df)

    plot_comparison(results)

if __name__ == "__main__":
    main()
