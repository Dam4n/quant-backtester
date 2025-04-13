import pandas as pd

def pairs_trading_strategy(df_a, df_b, lookback=30, entry_z=1.0, exit_z=0.0):
    """
    Implements a basic pairs trading strategy using the spread between two assets.

    Parameters:
        df_a (pd.DataFrame): Price data for asset A (must include 'Close')
        df_b (pd.DataFrame): Price data for asset B (must include 'Close')
        lookback (int): Rolling window size to calculate mean and std of spread
        entry_z (float): Z-score threshold to enter trades
        exit_z (float): Z-score threshold to exit trades

    Returns:
        pd.DataFrame: Combined dataframe with 'Close' (spread), Z-score, and Signal
    """
    df = pd.DataFrame(index=df_a.index)
    df['Price_A'] = df_a['Close']
    df['Price_B'] = df_b['Close']
    df = df.dropna()

    df['Spread'] = df['Price_A'] - df['Price_B']
    df['Close'] = df['Spread']

    df['Mean'] = df['Spread'].rolling(window=lookback).mean()
    df['Std'] = df['Spread'].rolling(window=lookback).std()
    df['ZScore'] = (df['Spread'] - df['Mean']) / df['Std']

    df['Signal'] = 0
    df.loc[df['ZScore'] > entry_z, 'Signal'] = -1
    df.loc[df['ZScore'] < -entry_z, 'Signal'] = 1
    df.loc[df['ZScore'].abs() < exit_z, 'Signal'] = 0

    df['Signal'] = df['Signal'].ffill().fillna(0)

    return df
