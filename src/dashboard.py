import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import config

def plot_spectrum(ax, ticker: str, results: dict):
    """plot welch powerr specturm with period labels"""
    freqs = results["cycles_df"]["frequency"].values
    power = results["cycles_df"]["power"].values
    periods = 1/freqs
    
    ax.plot(periods, power)
    for _, row in results["cycles_df"].iterrows():
        ax.axvline(x = row["period_days"], linestyle='--', alpha =0.7, color = 'red')
        ax.text(row["period_days"], max(power)*0.9, f"{row['period_days']:.0f}d", fontsize = 8)

    ax.set_title(f"{ticker} power spectrum")
    ax.set_xlabel("period (days)")
    ax.set_ylabel("power")
    pass

def plot_cycles(ax, ticker: str, prices, results: dict):
    """plot dominant cycles overlaid on price"""
    dominant_cycles = results["extracted"]
    top_cycles = results["cycles_df"].nlargest(3, "power")["period_days"].values
    
    ax.plot(prices, color="gray", alpha = 0.5, label = "price")

    for period, signal in dominant_cycles.items():
        #scale the signal to price range so that its visible
        if not any(abs(period - top) < 0.1 for top in top_cycles):
            continue
        scaled = signal / signal.std() * prices.std() * 0.3 + prices.mean()
        ax.plot(scaled, alpha = 0.6, label=f"{period}d cycles")

    ax.set_title(f"{ticker} dominant cycles overlaid on prices")
    ax.set_xlabel("days")
    ax.set_ylabel("price")
    ax.legend(fontsize=7)

def plot_prediction(ax, ticker: str, prices, combined_forecast):
    """plot historical price + future prediction"""
    ax.plot(prices, color="blue", label="historical")

    forecast_start = len(prices)
    forecast_x = np.arange(forecast_start, forecast_start + len(combined_forecast))
    last_price = prices[-1]
    forecast_prices = last_price + np.cumsum(combined_forecast)
    
    ax.plot(forecast_x, forecast_prices, color="orange", label = "forecast")
    ax.axvline(x=forecast_start, linestyle='--', color = 'gray', alpha=0.7, label="forecast start")
    ax.fill_between(forecast_x,
                    forecast_prices - forecast_prices.std(),
                    forecast_prices + forecast_prices.std(),
                    alpha =0.3, color = "orange", label  = "confidence interval"
                    )
    ax.set_title(f"{ticker} price prediction")
    ax.set_xlabel("days")
    ax.set_ylabel("price")
    ax.legend(fontsize=8)

    

def generate_report(ticker: str, prices, results, combined_forecast):
    """generate all three plots as one figure"""
    fig = plt.figure(figsize=(16, 10))
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.3)

    ax_spectrum = fig.add_subplot(gs[0,0])
    ax_cycles = fig.add_subplot(gs[0,1])
    ax_pred = fig.add_subplot(gs[1, :])

    fig.suptitle(f"{ticker} Fourier Market Analysis", fontsize=16, fontweight="bold")

    plot_spectrum(ax_spectrum, ticker, results)
    plot_cycles(ax_cycles, ticker, prices, results)
    plot_prediction(ax_pred, ticker, prices, combined_forecast)

    plt.savefig(f"{config.OUTPUT_DIR}{ticker}_dashboard.png", dpi = 150, bbox_inches="tight")
    plt.close()

