import numpy as np
import wave
import struct


def get_new_time_by_duration_sec(duration, samplerate):
    return np.arange(duration * samplerate) / samplerate


class CONST_SR:
    SR = 44100


def sec(x):
    return x * CONST_SR.SR

def write_wave(filename, samples):
    f = wave.open(filename, "w")
    f.setparams((1, 2, CONST_SR.SR, len(samples), "NONE", ""))
    f.writeframes(b"".join(
        [struct.pack('<h', round(x * 32767)) for x in samples]))
    f.close()
