import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.io import wavfile

#date time objects instead of strings make the code cleaner
start_date = datetime(year=2024, month = 1, day = 1)
end_date = datetime(year=2026, month = 1, day = 1)

ticker = "NVDA"


#formatting this way allows for the tickers to be an array input for multiple
df_NVDA = yf.download(tickers = ticker,
                      start = start_date,
                      end = end_date,
                      interval = "1d",
                      group_by = "ticker",
                      auto_adjust = True,  #corrects for stock splits and dividends so price history doesnt include fake jumps
                      progress = False #this is just a cosmetic progress bar when downloading data
                      )

print(df_NVDA["NVDA"]["Close"]) #NOTE: yfinance uses multiindex colum structure now, so to access the closing prices, need to do this

plt.figure(figsize=(12, 4))
plt.plot(df_NVDA["NVDA"]["Close"])
plt.title("NVDA Price history from 2024 - 2026")
plt.xlabel("Time (day)")
plt.ylabel("Price")
plt.savefig("nvda.png")

close_prices = df_NVDA["NVDA"]["Close"].values #NOTE: the .values coverts this data to a numpy array
returns = np.diff(close_prices)

transformed_prices = np.fft.fft(returns)
magnitude = np.abs(transformed_prices)
frequency = np.fft.fftfreq(len(magnitude), d = 1)

#NOTE: we only want the positive frequencies
positive_mask = frequency > 0 

frequency_pos = frequency[positive_mask]
magnitude_pos = magnitude[positive_mask]
period = 1 / frequency_pos

plt.figure(figsize=(12, 4))
plt.plot(period, magnitude_pos) #x, y coordinates by index
plt.title("FFT of NVDA closing prices")
plt.xlabel("period(days)")
plt.ylabel("magnitude")
plt.xlim(2, 252) # zoom: cycles in 252 days, the number of trading days in a year
plt.savefig("nvdafft.png")

cutoff = 1/20 # we want cycles longer than 20 days
filtered = transformed_prices.copy()
filtered[np.abs(frequency) > cutoff] = 0

reconstructed = np.fft.ifft(filtered)
reconstructed_prices = np.cumsum(reconstructed.real) + close_prices[0]

plt.figure(figsize=(12,4))
plt.plot(close_prices[1:], label="Original", alpha=0.5)
plt.plot(reconstructed_prices, label="Filtered (>20 day cycles)", linewidth=2)
plt.legend()
plt.title("NVDA - Original vs Low-Pass Filtered")
plt.savefig("nvda_filtered.png")

top_indices = np.argsort(magnitude_pos)[-10:] # get indices sorted by magnitude, takes the last 10 which are the largest 10

#get the actual frequencies and magnitude   
top_freqs = frequency_pos[top_indices]
top_mags = magnitude_pos[top_indices]

freq_min = top_freqs.min()
freq_max = top_freqs.max()

hz_min = 200
hz_max = 2000

#normalizing the frequency
top_freqs_hz = (top_freqs - freq_min)/(freq_max - freq_min) * (hz_max - hz_min) + hz_min

print(top_freqs_hz)

sample_rate = 44100
duration = 10
t = np.linspace(0, duration, sample_rate * duration)

audio = np.zeros_like(t)

#normalize magnitudes too
amp_min = top_mags.min()
amp_max = top_mags.max()

amplitudes = (top_mags - amp_min)/(amp_max - amp_min)

#for each pair, add a sign wave to to audio

for freq_hz, amp in zip (top_freqs_hz, amplitudes):
    audio += amp * np.sin(2 * np.pi * freq_hz * t)

#noramlzie and save
audio = audio /np.max(np.abs(audio))
audio_int = (audio * 32767).astype(np.int16)
wavfile.write("market_music.wav", sample_rate, audio_int)
