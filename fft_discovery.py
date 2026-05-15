import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import yfinance as yf

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


