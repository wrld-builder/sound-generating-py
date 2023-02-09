from utils import sec as utils_sec
from utils import CONST_SR as utils_sr
import random


class Lp1:
    def __init__(self):
        self.y = 0

    def next(self, x, cutoff):
        self.y += cutoff * (x - self.y)
        return self.y


class ChamGeneration:
    def __init__(self):
        pass

    @staticmethod
    def pluck(samples, amp, freq, dur):
        flt = Lp1()
        delay_buf = [0] * int(utils_sr.SR / freq)
        delay_pos = 0
        for i in range(int(len(delay_buf) * amp)):
            delay_buf[i] = random.random()
        for t in range(int(utils_sec(dur))):
            delay_buf[delay_pos] = flt.next(delay_buf[delay_pos], 220 / len(delay_buf))
            samples.append(amp * delay_buf[delay_pos])
            delay_pos = (delay_pos + 1) % len(delay_buf)

    @staticmethod
    def rest(samples, dur):
        for t in range(int(utils_sec(dur))):
            samples.append(samples[-1])

    @staticmethod
    def generate_cham_samples():
        samples = []

        for i in range(4):
            ChamGeneration.pluck(samples, 0.7, 58, 0.27)
            ChamGeneration.pluck(samples, 0.4, 62, 0.27)
            ChamGeneration.pluck(samples, 0.4, 66, 0.27)
            ChamGeneration.pluck(samples, 0.6, 69, 0.27)
            ChamGeneration.pluck(samples, 0.5, 138, 0.01)
            ChamGeneration.rest(samples, 0.13)
            ChamGeneration.pluck(samples, 0.7, 123, 0.13)
            ChamGeneration.rest(samples, 0.27)
            ChamGeneration.pluck(samples, 0.7, 139, 0.47)
            ChamGeneration.rest(samples, 0.07)
            ChamGeneration.pluck(samples, 0.7, 78, 0.27)
            ChamGeneration.pluck(samples, 0.4, 82, 0.27)
            ChamGeneration.pluck(samples, 0.4, 87, 0.27)
            ChamGeneration.pluck(samples, 0.6, 92, 0.27)
            ChamGeneration.pluck(samples, 0.5, 184, 0.01)
            ChamGeneration.rest(samples, 0.13)
            ChamGeneration.pluck(samples, 0.7, 139, 0.13)
            ChamGeneration.rest(samples, 0.27)
            ChamGeneration.pluck(samples, 0.7, 165, 0.47)
            ChamGeneration.rest(samples, 0.07)

        return samples
