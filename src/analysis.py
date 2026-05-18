import numpy as np
import pandas as pd
from scipy.signal import welch, butter, filtfilt

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

def bandpass_filter(returns: np.ndarray, period_days: float, bandwith: float = config.BANDWITH) -> np.ndarray:
    """Isolating a single cycle from the returns signal"""
    low = (1 / period_days) * (1 - bandwith)
    high = (1/period_days) * (1 + bandwith)
    low = max(low, 0.001) # prevent 0
    high = min(high, 0.499) # prevent hitting nyquist
    b, a = butter(N=3, Wn=[low, high], btype='band', fs = 1.0) #for flattest possible response in the passband, frequencies to keep pass through at full strength with no distrotion, outside the band it rolls off smoothly
    return filtfilt(b, a, returns) # actually applies the filter, done twice, forward once and backward once to get rid of phase shift (forawrd pass slightlyu delays the signal in time)

def extract_cycles(returns: np.ndarray, cycles_df: pd.DataFrame) -> dict:
    """returns {period_days: filtered_signal} for each dominant cycle"""
    extracted = {}
    for _, row in cycles_df.iterrows(): #loops over each row in the dominant cycles dataframe, the _ is the index(dont need) the row is the period_days etc
        filtered = bandpass_filter(returns, row["period_days"])
        extracted[round(row["period_days"], 1)] = filtered
    return extracted

def analyze_all(data: dict) -> dict:
    """Runs analysis on each ticker, returns {ticker:dominant_cycles_df}"""
    results = {}
    for ticker, returns in data.items():
        freqs, power = compute_spectrum(returns)
        cycles_df = get_dominant_cycles(freqs, power)
        extracted = extract_cycles(returns, cycles_df)
        results[ticker] = {
            "returns": returns,
            "cycles_df": cycles_df,
            "extracted": extracted
        }
    return results
