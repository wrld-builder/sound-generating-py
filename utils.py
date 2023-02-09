import numpy as np


def get_new_time_by_duration_sec(duration, samplerate):
    return np.arange(duration * samplerate) / samplerate


class CONST_SR:
    SR = 44100


def sec(x):
    return x * CONST_SR.SR
