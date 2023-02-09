import math
import struct
import wave
import numpy as np


class BellGeneration:
    def __init__(self):
        pass

    @staticmethod
    def write_wave(filename, samples, freq=44100):
        f = wave.open(filename, "w")
        f.setparams((1, 2, freq, len(samples), "NONE", ""))
        f.writeframes(b"".join(
            [struct.pack('<h', round(x * 32767)) for x in samples]))
        f.close()

    @staticmethod
    def sec(x, freq=44100):
        return freq * x

    @staticmethod
    def generate_bell_sound(freq=44100, time_ms=1000):
        oc = Sine()
        om = Sine()
        bell_samples = []

        for t in range(int(time_ms)):
            env = 1 - t / freq
            bell_samples.append(0.5 * oc.next(80, 3 * env * om.next(450)))
        return bell_samples


class Sine:
    def __init__(self):
        self.phase = 0
        self.__SR = 44100

    def next(self, freq, pm=0):
        s = math.sin(self.phase + pm)
        self.phase = (self.phase + 2 * math.pi * freq / self.__SR) % (2 * math.pi)
        return s
