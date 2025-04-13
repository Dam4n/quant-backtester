import os
import yfinance as yf
import pandas as pd

def get_data(tickers, start_date, end_date, save_path='data'):
    """
    Download daily OHLCV data for a list of tickers and save to CSV files.

    Parameters:
        tickers (list): List of ticker symbols
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format
        save_path (str): Directory where CSV files will be saved
    """
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for ticker in tickers:
        file_path = os.path.join(save_path, f"{ticker}.csv")

        if os.path.exists(file_path):
            print(f"{ticker} data already exists. Skipping download.")
            continue

        print(f"Downloading {ticker}...")
        df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        if not df.empty:
            df.to_csv(file_path, index_label='Date')
            print(f"Saved {ticker} to {file_path}")
        else:
            print(f"No data found for {ticker}")

def load_data(ticker, start_date=None, end_date=None, data_path='data'):
    """
    Load OHLCV data for a ticker from CSV and return a formatted DataFrame.

    Parameters:
        ticker (str): Ticker symbol
        start_date (str): Optional start date to filter data
        end_date (str): Optional end date to filter data
        data_path (str): Folder where CSV files are stored

    Returns:
        pd.DataFrame: Cleaned DataFrame with Date as index
    """
    file_path = os.path.join(data_path, f"{ticker}.csv")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file for {ticker} not found at {file_path}")

    df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')

    df = df.apply(pd.to_numeric, errors='coerce')
    df.dropna(inplace=True)

    # Optional: filter by date range
    if start_date:
        df = df[df.index >= start_date]
    if end_date:
        df = df[df.index <= end_date]

    return df