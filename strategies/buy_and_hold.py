def buy_and_hold(df):
    df = df.copy()
    df['Signal'] = 1
    return df