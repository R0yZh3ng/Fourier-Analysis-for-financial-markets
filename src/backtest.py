import numpy as np
import pandas as pd

import config
from src.analysis import compute_spectrum, get_dominant_cycles, extract_cycles
from src.prediction import fit_cycle, extrapolate

def backtest(prices: np.ndarray, ticker: str) -> dict:
    """ walk forward backtest of cycle prediction accuracy, returns hit rate and trade log"""
    window = config.BACKTEST_WINDOW
    correct = 0
    total = 0
    trade_log = []

    for i in range(window, len(prices) - config.FORECAST_DAYS):
        #slice the window
        window_prices = prices[i - window:i]
        actual_prices = prices[i:i + config.FORECAST_DAYS]

        returns = np.diff(np.log(window_prices)) * 100
        freqs, power = compute_spectrum(returns)
        cycles_df = get_dominant_cycles(freqs, power)
        extracted = extract_cycles(freqs, cycles_df)

        preds = {}
        for period, signal in extracted.items():
            params = fit_cycle(signal, period)
            if params is None:
                continue
            preds[period] = extrapolate(signal, params)

        if not preds:
            continue

        forecast = np.sum(list(preds.values()), axis = 0)
        predicted_direction = forecast.mean() > 0
        actual_direction = actual_prices[-1] > actual_prices[0]

        correct += predicted_direction == actual_direction
        total += 1
        trade_log.append({
            "day": i,
            "predicted": "UP" if predicted_direction else "DOWN",
            "actual": "UP" if actual_direction else "DOWN",
            "correct": predicted_direction == actual_direction
        })

    hit_rate = correct / total if total > 0 else 0
    return {"hit_rate": hit_rate, "total_trades": total, "trade_log": pd.DataFrame(trade_log)}
