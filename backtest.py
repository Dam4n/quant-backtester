import argparse
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from utils.utils import load_data, get_data
from strategies.trend_following import moving_average_trend_following
from strategies.buy_and_hold import buy_and_hold
from strategies.mean_reversion import rsi_strategy, bollinger_band_strategy
from strategies.pairs_trading import pairs_trading_strategy
from execution.execution import simulate_trades
from metrics.metrics import calculate_performance_metrics

def plot_time_series(df, y_column, title, xlabel, ylabel, legend_label):
    plt.plot(df.index, df[y_column], label=legend_label, color='purple')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.xticks(rotation=45)
    valid_range = df.dropna(subset=[y_column]).index
    plt.xlim(valid_range.min(), valid_range.max())
    plt.tight_layout()

def plot_signals(df, strategy_choice):
    """
    Plot buy/sell signals based on the strategy used.
    """
    if strategy_choice == 'trend_following':
        df['Signal_Change'] = df['Signal'].diff()
        buy_signals = df[df['Signal_Change'] == 2]
        sell_signals = df[df['Signal_Change'] == -2]
    elif strategy_choice == 'rsi':
        df['Signal_Change'] = df['Signal'].diff()
        buy_signals = df[(df['Signal_Change'] == 1) & (df['Signal'] == 1)]
        sell_signals = df[(df['Signal_Change'] == -1) & (df['Signal'] == -1)]
    elif strategy_choice == 'bollinger':
        df['Signal_Change'] = df['Signal'].diff()
        buy_signals = df[(df['Signal_Change'] == 1) & (df['Signal'] == 1)]
        sell_signals = df[(df['Signal_Change'] == -1) & (df['Signal'] == -1)]

        plt.plot(df.index, df['Upper_Band'], label='Upper Band', linestyle='--', color='orange')
        plt.plot(df.index, df['Lower_Band'], label='Lower Band', linestyle='--', color='orange')
    elif strategy_choice == 'pairs':
        df['Signal_Change'] = df['Signal'].diff()
        buy_signals = df[df['Signal_Change'] == 1]
        sell_signals = df[df['Signal_Change'] == -1]
    else:
        return  # No signals to plot for buy-and-hold

    plt.scatter(buy_signals.index, buy_signals['Close'], label='Buy Signal', marker='^', color='green', s=100)
    plt.scatter(sell_signals.index, sell_signals['Close'], label='Sell Signal', marker='v', color='red', s=100)

def main():
    parser = argparse.ArgumentParser(description="Quantitative Strategy Backtester")
    parser.add_argument('--ticker', type=str, required=True, help='Ticker symbol')
    parser.add_argument('--pair-ticker', type=str, help='Second ticker for pairs trading')
    parser.add_argument('--start', type=str, required=True, help='Start date in YYYY-MM-DD format')
    parser.add_argument('--end', type=str, required=True, help='End date in YYYY-MM-DD format')
    parser.add_argument('--strategy', type=str, choices=['trend_following', 'buy_and_hold', 'rsi', 'bollinger', 'pairs'], default='trend_following')
    parser.add_argument('--initial-cash', type=float, default=10000)
    parser.add_argument('--short-window', type=int, default=10)
    parser.add_argument('--long-window', type=int, default=30)
    parser.add_argument('--rsi-period', type=int, default=14)
    parser.add_argument('--rsi-lower', type=int, default=30)
    parser.add_argument('--rsi-upper', type=int, default=70)
    parser.add_argument('--bollinger-window', type=int, default=20,
                        help='Window size for Bollinger Bands (default: 20)')
    parser.add_argument('--bollinger-std', type=float, default=2.0,
                        help='Standard deviation multiplier for Bollinger Bands (default: 2.0)')

    args = parser.parse_args()

    if args.strategy == 'pairs':
        print(f"Checking data for {args.ticker}...")
        print(f"Checking data for {args.pair_ticker}...")
        get_data([args.ticker, args.pair_ticker], args.start, args.end)
        print(f"Loading data for {args.ticker}...")
        print(f"Loading data for {args.pair_ticker}...")
        df1 = load_data(args.ticker, args.start, args.end)
        df2 = load_data(args.pair_ticker, args.start, args.end)
    else:
        print(f"Checking data for {args.ticker}...")
        get_data([args.ticker], args.start, args.end)
        print(f"Loading data for {args.ticker}...")
        df = load_data(args.ticker, args.start, args.end)

    print("Running strategy...")
    if args.strategy == 'trend_following':
        df = moving_average_trend_following(df, short_window=args.short_window, long_window=args.long_window)
    elif args.strategy == 'buy_and_hold':
        df = buy_and_hold(df)
    elif args.strategy == 'rsi':
        df = rsi_strategy(df, period=args.rsi_period, lower=args.rsi_lower, upper=args.rsi_upper)
    elif args.strategy == 'bollinger':
        df = bollinger_band_strategy(df, window=args.bollinger_window, num_std=args.bollinger_std)
    elif args.strategy == 'pairs':
        df = pairs_trading_strategy(df1, df2)

    print("Simulating trades...")
    df = simulate_trades(df, initial_cash=args.initial_cash)

    print("Calculating performance metrics...")
    metrics = calculate_performance_metrics(df)
    print("\n--- Performance Metrics ---")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    print("Plotting results...")
    plt.figure(figsize=(14, 6))
    plt.plot(df.index, df['Close'], label='Price', alpha=0.6)

    if 'SMA_Short' in df.columns:
        plt.plot(df.index, df['SMA_Short'], label='Short MA', linestyle='--')
    if 'SMA_Long' in df.columns:
        plt.plot(df.index, df['SMA_Long'], label='Long MA', linestyle='--')

    plot_signals(df, args.strategy)

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.xticks(rotation=45)

    strategy_title = args.strategy.replace('_', ' ').title()
    if args.strategy == 'pairs':
        title = f"{args.ticker} & {args.pair_ticker} - {strategy_title} Strategy with Signals"
    else:
        title = f"{args.ticker} - {strategy_title} Strategy with Signals"
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    valid_range = df.dropna(subset=['Close']).index
    plt.xlim(valid_range.min(), valid_range.max())
    plt.tight_layout()
    plt.show()

    print("Plotting portfolio performance...")
    if args.strategy == 'pairs':
        title = f"{args.ticker} & {args.pair_ticker} - Portfolio Value Over Time"
    else:
        title = f"{args.ticker} - Portfolio Value Over Time"

    plot_time_series(df, 'Portfolio Value', title, "Date", "Portfolio Value ($)", "Portfolio Value")
    plt.show()

if __name__ == "__main__":
    main()
