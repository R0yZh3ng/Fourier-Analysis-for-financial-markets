import numpy as np
import pandas as pd
from scipy.signal import welch

import config

def compute_spectrum(returns: np.ndarray) -> tuple:
    """Returns (frequencies, power) using welch's method"""
    freqs, power = welch(returns, fs=config.SAMPLING_FREQUENCY, nperseg=config.WINDOW_SIZE) #welch does windowing, fft and averge all internally, it also applies the positive mask, fs is one sample a day, nperseg is half a trading year per window
    return freqs, power

def get_dominant_cycles(freqs, power, n=config.TOP_N_CYCLES) -> pd.DataFrame:
    """Returns dataframe with columns: period_days, frequency, power"""
    freqs = freqs[1:]
    power = power[1:]

    mask = (1/freqs) >= config.MIN_PERIOD # filtering out microstructure noise
    freqs = freqs[mask]
    power = power[mask]
    top_indices = np.argsort(power)[-n:]
    df = pd.DataFrame({"period_days": 1/freqs[top_indices],
                        "frequency":freqs[top_indices],
                        "power": power[top_indices]
                       }).sort_values("period_days")
    return df

def analyze_all(data: dict) -> dict:
    """Runs analysis on each ticker, returns {ticker:dominant_cycles_df}"""
    results = {}
    for ticker, returns in data.items():
        freqs, power = compute_spectrum(returns)
        results[ticker] = get_dominant_cycles(freqs, power)
    return results


