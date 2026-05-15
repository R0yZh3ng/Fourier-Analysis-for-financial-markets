import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import yfinance as yf

end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=365)

ticker = "AAPL"

df = yf.download(ticker, start=start_date, end=end_date)

prices = df["Close"].values.flatten()

# Use log returns instead of raw prices
returns = np.diff(np.log(prices))

# FFT
fft_result = np.fft.fft(returns)
frequencies = np.fft.fftfreq(len(returns), d=1)

# Keep only positive frequencies
positive = frequencies > 0

frequencies = frequencies[positive]
fft_result = fft_result[positive]

magnitude = np.abs(fft_result)
periods = 1 / frequencies

# Plot FFT
plt.figure(figsize=(14, 6))
plt.plot(periods, magnitude)
plt.title("FFT Spectrum of AAPL Log Returns")
plt.xlabel("Period (Days)")
plt.ylabel("Magnitude")
plt.xlim(0, 100)

plt.savefig("new.png")
