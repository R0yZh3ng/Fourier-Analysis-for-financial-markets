import numpy as np
import pandas as pd
from scipy.optimize import curve_fit # curve fit is a regression function
import config

def sine_model(t, amplitude, frequency, phase, trend):
    """The function we're fitting to each cycle"""
    return amplitude * np.sin(2*np.pi * frequency * t + phase) + trend

def fit_cycle(signal: np.ndarray, period_days: float) -> dict:
    """Fit a sine wave to an extracted cycle signal"""
    t = np.arange(len(signal))

    #initial params
    p0 = [
        signal.std(),    #amplitude
        1/period_days,   #frequency
        0,               #phase
        signal.mean()    #trend
    ]

    try:
        params, _ = curve_fit(sine_model, t, signal, p0 = p0, maxfev = 5000)
        return {"amplitude": params[0], "frequency": params[1], "phase": params[2],"trend": params[3]}
    except RuntimeError:
        return None

def extrapolate(signal: np.ndarray, params:dict) -> np.ndarray:
    """Project the fitted sine wave into the future"""
    t_future = np.arange(len(signal), len(signal) + config.FORECAST_DAYS)
    return sine_model(t_future, **params) #**kwargs allow a function to accept an arbitrary number of keyword arguments

def predict_all(results: dict) ->dict:
    """returns {ticker: {period: future_signal}}"""
    predictions = {}
    for ticker, result in results.items():
        predictions[ticker] = {}
        for period, signal in result["extracted"].items():
            params = fit_cycle(signal, period)
            if params is None:
                print(f"{ticker} {period}d cycle: could not fit")
                continue
            future = extrapolate(signal, params)
            predictions[ticker][period] = future
    return predictions

def combine_predictions(predictions: dict) -> dict:
    """sums all cycle forecasts into one combined prediction per ticker"""
    combined = {}
    for ticker, cycles in predictions.items():
        if not cycles:
            continue

        forecast = np.sum(list(cycles.values()), axis=0)
        combined[ticker] = forecast
    return combined



