import numpy as np

class WaveGenerator:
    def __init__(self):
        pass

    # Harmonic fluid: sin / cos
    # Formula: A * cos(wt + f)
    @staticmethod
    def generate_sine_wave_cycle(freq, amplitude, duration, samplerate):
        return amplitude * np.cos(2 * np.pi + freq * get_new_time_by_duration_sec(duration, samplerate))

    @staticmethod
    def generate_sine_wave(freq, amplitude, duration, samplerate):
        return amplitude * np.cos(2 * np.pi * freq * get_new_time_by_duration_sec(duration, samplerate))