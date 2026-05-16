frequency resolution is in case the cycle is very long

nyquist theorem says to sample at  at least twice the frequency of what you want to detect

using the min max normalization to get to audible frequency ranges, the formula is as follows

x_scaled = [(x - min) / (max - min)] * (new_max - new_min) + new min

