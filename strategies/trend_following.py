import pandas as pd
import numpy as np

def moving_average_trend_following(df, short_window=50, long_window=200):
    """
    Calculate moving average crossover signals.

    Parameters:
        df (pd.DataFrame): Stock OHLCV data
        short_window (int): Window for short moving average
        long_window (int): Window for long moving average

    Returns:
        pd.DataFrame: Original DataFrame with added MA columns and 'Signal' column
    """
    df = df.copy()

    df['SMA_Short'] = df['Close'].rolling(window=short_window).mean()
    df['SMA_Long'] = df['Close'].rolling(window=long_window).mean()

    df['Signal'] = 0

    mask = df['SMA_Short'].notna() & df['SMA_Long'].notna()

    df.loc[mask, 'Signal'] = np.where(df.loc[mask, 'SMA_Short'] > df.loc[mask, 'SMA_Long'], 1, -1)

    return df