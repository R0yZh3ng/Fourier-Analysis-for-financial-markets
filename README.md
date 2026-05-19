# Fourier Market Analysis

## What it does
This is a tool that analyzes publically tradeable financial assets for any cyclical patterns in its price progression. Upon detection of cycles, it will extrapolate the pattern as a potential indicator of future price movement.

## Methodology
After obtaining the historical data of the financial asset, its daily returns are computed from raw closing prices. Then reason for this is to ensure that the data is stationary when 
applying the fourier analysis, and to verify it's stationarity, we applied the adfuller function to test for the presence of a unit root.

Then we used welch's method to transform our data, which in comparison to directly using the fast fourier transform, it takes windowed segments of the data and averages them out. What this means is that the small frequencies in the data, likely noise, will be mostly canceled out, leaving us with the more significant or likely cyclical patterns.

These patterns are then extracted based on power given by welch's method and filtered to leave us with the top 10 most significant cycles; and since we wanted to observe longer/seasonal patterns, we have set a cutoff to be greater than periods of 5 days. These values can all be altered in the config file to be suited for your specific needs. 

The extracted cycles are then used to predict future price movements within a prediction window. This is done through fitting a sine wave to the extracted cycle using regression and then extrapolating that fitting function to predict future price movements and the magnitude of their movements. Since we are looking at multiple cycles at once, we sum all the predictions into one combined prediction to adjust for the smaller cycles.

The predictions are then computed for a set window size through years of historical data, then this data is compared to observed price movements in the same time frame, and the prediction accuracies are computed.

Lastly the results are visualized using graphs with matplotlib

## Results
I chose three tickers in particular for this project, first one being TSLA which is a volatile ticker with high popularity, second is SPY which is an index fund in order to introduce more noise in the data, lastly is MAG which is a collection of the 7 largest tech companies leading the market.

the results for these three tickers are as follows:

TSLA: next 30 days signal -> UP (average return = 0.1675%)
SPY: next 30 days signal -> UP (average return = 0.0034%)
MAGS: next 30 days signal -> UP (average return = 0.0311%)

TSLA backtest: hit rate = 60.0% over 220 trades
We can see that the algorithm indicates decent success rates for TSLA, and on the chart we can observe that there is a very significant cycle which seems to occur per 1/2 of the trading year, which may indicate the financial report cycles.

SPY backtest: hit rate = 19.5% over 220 trades
the SPY predictions however were very unfavourable, this is likely the result of there being too much noise in large index funds as changes in any sub sector is going to impact the asset as a whole.

MAGS backtest: hit rate = 74.1% over 220 trades
The MAG backtest seemed to perform extremely well, this may be because of large tech companies following the same cycles in the trading year as they're often in partnerships within the etf, but its more likely that the data was just overfitted given that the complexity of this algorithm does not take into account the many extranous factors of the market.


## Installation

just create a virutal enviroment on your machine, use pip to install requirements.txt, and then run main.py from root

## Usage
no clue what this section is

## "Can you hear the music?"

a little easter egg inspired by the movie oppenheimer,
here are the "compositions" created by the cycles i detected in these financial instruments, and to no one's surprise they dont sound like much, if anything the screams of retail traders watching their porfolio go down 80% from one YOLO
