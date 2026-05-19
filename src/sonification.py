import numpy as np
from scipy.io import wavfile

import config

def sonify(ticker: str, cycles_df, output_path: str = None):
    """Convert dominant market cycles to audio"""
    t = np.linspace(0, config.AUDIO_DURATION, config.SAMPLE_RATE * config.AUDIO_DURATION)
    audio = np.zeros_like(t)

    periods = cycles_df["period_days"].values
    powers = cycles_df["power"].values

    log_min = np.log(config.AUDIO_MIN_HZ)
    log_max = np.log(config.AUDIO_MAX_HZ)
    period_min = periods.min()
    period_max = periods.max()

    for period, power in zip(periods, powers):
        t_norm = (period - period_min) / (period_max - period_min)
        freq_hz = np.exp(log_min + t_norm * (log_max - log_min))
        amplitude = power / powers.max()
        audio += amplitude * np.sin(2 * np.pi * freq_hz * t)

    audio = audio / np.max(np.abs(audio))
    audio_int = (audio * 32767).astype(np.int16)

    if output_path is None:
        output_path = f"{config.OUTPUT_DIR}{ticker}_market_music.wav"

    wavfile.write(output_path, config.SAMPLE_RATE, audio_int)
    print(f"{ticker} sonification saved to {output_path}")

