import math
from utils import sec as utils_sec
from utils import CONST_SR as utils_sr


class BellGeneration:
    def __init__(self):
        pass

    @staticmethod
    def generate_bell_sound(freq=44100, time_s=1):
        oc = Sine()
        om = Sine()
        bell_samples = []

        for t in range(int(utils_sec(time_s))):
            env = 1 - t / freq
            bell_samples.append(0.5 * oc.next(80, 3 * env * om.next(450)))
        return bell_samples


class Sine:
    def __init__(self):
        self.phase = 0

    def next(self, freq, pm=0):
        s = math.sin(self.phase + pm)
        self.phase = (self.phase + 2 * math.pi * freq / utils_sr.SR) % (2 * math.pi)
        return s
