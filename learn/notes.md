frequency resolution is in case the cycle is very long

nyquist theorem says to sample at  at least twice the frequency of what you want to detect

using the min max normalization to get to audible frequency ranges, the formula is as follows

x_scaled = [(x - min) / (max - min)] * (new_max - new_min) + new min
-> the above creates a issue specificially for audio,human ears perceive audio logarithmically, meaning that 
100hz -> 200 hz are the the same as 1000hz -> 2000hz, a doubling, even though they are way further apart in magnitude. so linear mapping makes audio sound bad because our ears interprete equal linear steps aas increasly tiny intevral as frequency goes up, so everything bunches up perceptually in the high end. logatithmic mapping spaces frequencies so that each steiop is a equal perceived interval to human ears.

stationarity is the statistical property of a stochastic process or tiem series where the joint probability distribution does not chaneg over time, meaning that it is stationary if its mean, variance and autocorrelation strictuires remain entirely constanr regardless of the specific point in tiem at wehich tehy are observed

-> the ADF test specificially checks whether a time series has a "unit root" - does this series have a drifting mean that never reverts, if it does then its non-stationary, if it doesnt, its stationary.

