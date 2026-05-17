from datetime import datetime


#Ticker config
Tickers = ["TSLA", "SPY", "MAGS"]
start_date = datetime(year = 2024, month = 1, day = 1)
end_date = datetime(year = 2026, month = 1, day = 1)
DATA_CACHE_DIR = "data/"

#fft settings
MIN_PERIOD = 2      #days - ignore cycles shorter than 2 days
MAX_PERIOD = 252    #days - one trading year
TOP_N_CYCLES = 10   #number of dominant cycles to extract

# filtering settings
LOWPASS_CUTOFF = 20 #filter out cycles less than n days

# prediction settings
FORECAST_DAYS = 30  #how far ahead to predict
BACKTEST_WINDOW =   #days in history used in backtesting

# sonification settings
AUDIO DURATION = 200
AUDIO_MIN_HZ = 80
AUDIO_MAX_HZ = 800
SAMPLE_RATE = 44100

# output
OUTPUT_DIR = "output/"
