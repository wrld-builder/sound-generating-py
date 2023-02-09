from utils import sec as utils_sec
from utils import CONST_SR as utils_sr
from bell_sound_gen import Sine as bell_sound_sine


def linear_env(segs, t):
    x0 = 0
    y0 = 0
    for x1, y1 in segs:
        if t < x1:
            return y0 + (t - x0) * ((y1 - y0) / (x1 - x0))
        x0, y0 = x1, y1
    return y0


class Env:
    def __init__(self, segs):
        self.segs = segs
        self.phase = 0

    def next(self, scale=1):
        s = linear_env(self.segs, self.phase)
        self.phase += scale / utils_sr.SR
        return s


class DrumGeneration:
    def __init__(self):
        pass

    @staticmethod
    def kick(samples, dur):
        freq = 100
        o1 = bell_sound_sine()
        o2 = bell_sound_sine()
        e1 = Env([(0, 1), (0.02, 1), (1, 0)])
        e2 = Env([(0, 1), (0.01, 0)])
        for t in range(int(utils_sec(dur))):
            o = o1.next(freq * e1.next(2.5), 16 * e2.next() * o2.next(freq))
            samples.append(0.5 * o)

    @staticmethod
    def snare(samples, dur):
        freq = 100
        o1 = bell_sound_sine()
        o2 = bell_sound_sine()
        e1 = Env([(0, 1), (0.2, 0.2), (0.4, 0)])
        e2 = Env([(0, 1), (0.17, 0)])
        e3 = Env([(0, 1), (0.005, 0.15), (1, 0)])
        fb = 0
        for t in range(int(utils_sec(dur))):
            fb = e2.next() * o1.next(freq, 1024 * fb)
            samples.append(0.5 * o2.next(e1.next() * freq * 2.5, 4.3 * e3.next() * fb))
