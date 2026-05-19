frequency resolution is in case the cycle is very long

nyquist theorem says to sample at  at least twice the frequency of what you want to detect

using the min max normalization to get to audible frequency ranges, the formula is as follows

x_scaled = [(x - min) / (max - min)] * (new_max - new_min) + new min
-> the above creates a issue specificially for audio,human ears perceive audio logarithmically, meaning that 
100hz -> 200 hz are the the same as 1000hz -> 2000hz, a doubling, even though they are way further apart in magnitude. so linear mapping makes audio sound bad because our ears interprete equal linear steps aas increasly tiny intevral as frequency goes up, so everything bunches up perceptually in the high end. logatithmic mapping spaces frequencies so that each steiop is a equal perceived interval to human ears.

stationarity is the statistical property of a stochastic process or tiem series where the joint probability distribution does not chaneg over time, meaning that it is stationary if its mean, variance and autocorrelation strictuires remain entirely constanr regardless of the specific point in tiem at wehich tehy are observed

-> the ADF test specificially checks whether a time series has a "unit root" - does this series have a drifting mean that never reverts, if it does then its non-stationary, if it doesnt, its stationary.

Dominant cycles in a fourier anaylsis the the peaks with the greatest magnitude or in other words, the highest amplitude peaks in the frequency spectrum


for data saving formats

CSV is large in size, slow read speed, has universal compatibility and doesnt preserve types
Parquet is small in size, very fast read speed, compatible with python, r , spark, and does preserve types ---- this is the industry standard
pickle has medium size, fast read speed, compatible with python and perserves types
JSON is very large in size, slow read speed, universal compatibility and only partially perserves the types

best way to save data would be to use parquet witha csv option in case export to excel

the __main__ name guard is there because python runs all the tip level code when importing a file, the guard prevents main from running automatically if someone imports and that import chain eventually touches main.py, so this is there so that main only runs when you expliclaity execute python main.py

normalize the returns using log, theyre addicitve across time so that you can sum daily log return to get the total returns over a period, regular percent returns arent additive but rathger multipl;icative
the multiplying by 100 is just so that the decimal becomes a percentage

welch's method, instead of one fft on the whoel signal, it splits the data into overlapping windows, ffts each one, and averages the results, this creates much less noise
this is called variance reduction, when you average the windows togeter, the random noise taht is different in each window canacels out, while the true repeating cycles survive as they show up consistently acorss all windows

market microstructure noise is the short term cycles that are largely aritficial thythms baked into how market operate, not real economic sugnals, normally these would be filtered out and focus on cycles above 5-10 days

larger windows mean less averaging, so less noise ccnellaation but the peaks get taller due to better frequency resolution, larger windwos can distinguish between frequencies that are close torgther, whats previously smeared concentrats into one sharp peak

power just shows how likely there is a cycle, meaning it does not have direct correlation to the amplitude.

hit rate:

50-55 barely better than random and not worth trading
55-60 decent edge and potentially profitable after costs
60+ strong edge
70+ either found smt real or overfitted the data

efficient market hypothesis
 if a pattern in a large index fund like spy is detectable and consistently profitable, then funds will trade against it which destroys the pattern.
