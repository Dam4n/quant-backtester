def simulate_trades(df, initial_cash=10000):
    """
    Simulate trades based on signal column in DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame with 'Close' prices and 'Signal' column
        initial_cash (float): Starting portfolio cash

    Returns:
        pd.DataFrame: DataFrame with portfolio value and trade tracking
    """
    df = df.copy()
    cash = initial_cash
    position = 0
    portfolio_values = []

    for i, row in df.iterrows():
        price = row['Close']
        signal = row['Signal']

        if signal == 1 and position == 0:
            position = cash / price
            cash = 0
        elif signal == -1 and position > 0:
            cash = position * price
            position = 0

        portfolio_value = cash + (position * price)
        portfolio_values.append(portfolio_value)

    df['Portfolio Value'] = portfolio_values
    return df