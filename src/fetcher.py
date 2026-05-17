import os
import numpy as np
import pandas as pd
import yfinance as yf
from statsmodels.tsa.stattools import adfuller

import config

def fetch_ticker(ticker:str) ->pd.DataFrame:
    """Download or load from cache"""
    cache_path = f"{config.DATA_CACHE_DIR}{ticker}.parquet"
    if os.path.exists(cache_path):
        df = pd.read_parquet(cache_path)
        return df
    else:
        df = yf.download(tickers = ticker,
                         start = config.START_DATE,
                         end = config.END_DATE,
                         interval = "1d",
                         group_by = "ticker",
                         auto_adjust = True,
                         progress = False)
        df.to_parquet(cache_path)
        return df


def make_stationary(prices: np.ndarray, ticker: str) -> np.ndarray:
    """Diff and verify stationarity with ADF"""
    returns = np.diff(np.log(prices)) * 100
    stationarity = adfuller(returns) 
    print(f"{ticker} ADF p-value: {stationarity[1]:.4f} - {'stationary' if stationarity[1] < 0.05 else 'not stationary x'}")
    return returns

def fetch_all() -> dict:
    """loop over config.TICKERS, return {ticker: returns}"""
    result = {}
    for ticker in config.TICKERS:
        df = fetch_ticker(ticker)
        prices = df[ticker]["Close"].values
        result[ticker] = make_stationary(prices, ticker) 
    return result
        
