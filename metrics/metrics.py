import numpy as np

def calculate_performance_metrics(df, risk_free_rate=0.0):
    """
    Calculate performance metrics for a trading strategy.

    Parameters:
        df (pd.DataFrame): DataFrame with 'Portfolio Value' column
        risk_free_rate (float): Daily risk-free rate (e.g., 0.01 / 252 for 1% annual)

    Returns:
        dict: Dictionary of performance metrics
    """
    df = df.copy()
    df['Daily Return'] = df['Portfolio Value'].pct_change()
    df.dropna(subset=['Daily Return'], inplace=True)

    trading_days = df['Daily Return'].count()

    total_return = (df['Portfolio Value'].iloc[-1] / df['Portfolio Value'].iloc[0]) - 1
    avg_daily_return = df['Daily Return'].mean()
    std_daily_return = df['Daily Return'].std()

    sharpe_ratio = np.nan
    if std_daily_return != 0:
        sharpe_ratio = (avg_daily_return - risk_free_rate) / std_daily_return
        sharpe_ratio *= np.sqrt(trading_days)

    running_max = df['Portfolio Value'].cummax()
    drawdown = df['Portfolio Value'] / running_max - 1
    max_drawdown = drawdown.min()

    return {
        'Total Return (%)': round(total_return * 100, 2),
        'Max Drawdown (%)': round(max_drawdown * 100, 2),
        'Sharpe Ratio': round(sharpe_ratio, 2) if not np.isnan(sharpe_ratio) else 'N/A'
    }