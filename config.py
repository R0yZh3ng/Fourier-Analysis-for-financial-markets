from datetime import datetime


#Ticker config
TICKERS = ["TSLA", "SPY", "MAGS"]
START_DATE = datetime(year = 2024, month = 1, day = 1)
END_DATE = datetime(year = 2026, month = 1, day = 1)
DATA_CACHE_DIR = "data/"

#fft settings
MIN_PERIOD = 5      #days - ignore cycles shorter than 5 days
MAX_PERIOD = 252    #days - one trading year
TOP_N_CYCLES = 10   #number of dominant cycles to extract
SAMPLING_FREQUENCY = 1 # 1 sample per day
WINDOW_SIZE = 252   #for welchs

# filtering settings
LOWPASS_CUTOFF = 20 #filter out cycles less than n days
BANDWITH = 0.3

# prediction settings
FORECAST_DAYS = 30  #how far ahead to predict
BACKTEST_WINDOW = 252  #days in history used in backtesting

# sonification settings
AUDIO_DURATION = 200
AUDIO_MIN_HZ = 80
AUDIO_MAX_HZ = 800
SAMPLE_RATE = 44100

# output
OUTPUT_DIR = "output/"
