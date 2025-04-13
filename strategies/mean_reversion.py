import pandas as pd

def rsi_strategy(df, period=14, lower=30, upper=70):
    """
    Implements a simple RSI-based trading strategy.

    Buy when RSI < lower threshold.
    Sell when RSI > upper threshold.

    Parameters:
        df (pd.DataFrame): Stock OHLCV data with a 'Close' column.
        period (int): Lookback period for RSI calculation.
        lower (int): RSI level below which to trigger a buy.
        upper (int): RSI level above which to trigger a sell.

    Returns:
        pd.DataFrame: DataFrame with RSI and 'Signal' columns.
    """
    df = df.copy()

    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    df['Signal'] = 0
    df.loc[df['RSI'] < lower, 'Signal'] = 1
    df.loc[df['RSI'] > upper, 'Signal'] = -1

    return df

def bollinger_band_strategy(df, window=20, num_std=2):
    """
    Implements a Bollinger Band trading strategy.

    Buy when price < lower band.
    Sell when price > upper band.

    Parameters:
        df (pd.DataFrame): OHLCV data with 'Close'
        window (int): SMA window
        num_std (float): Number of std deviations

    Returns:
        pd.DataFrame: With bands and Signal column
    """
    df = df.copy()

    rolling_mean = df['Close'].rolling(window=window).mean()
    rolling_std = df['Close'].rolling(window=window).std()

    df['Middle_Band'] = rolling_mean
    df['Upper_Band'] = rolling_mean + num_std * rolling_std
    df['Lower_Band'] = rolling_mean - num_std * rolling_std

    df['Signal'] = 0
    df.loc[df['Close'] < df['Lower_Band'], 'Signal'] = 1
    df.loc[df['Close'] > df['Upper_Band'], 'Signal'] = -1

    return df
