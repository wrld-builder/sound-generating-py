import math
from utils import CONST_SR as utils_sr
from utils import sec as utils_sec

f = 96
i1 = 0.03
i2 = i1 * 2
i3 = i1 * 3
i4 = i1 * 4

class RissetMixGeneration:
    def __init__(self):
        pass

    @staticmethod
    def sines(bank, t):
        mix = 0
        for f in bank:
            mix += math.sin(2 * math.pi * f * t / utils_sr.SR)
        return mix

    @staticmethod
    def generate_risset_samples():
        risset = []

        for i in [f, f + i1, f + i2, f + i3, f + i4, f - i1, f - i2, f - i3, f - i4]:
            for j in [i, 5 * i, 6 * i, 7 * i, 8 * i, 9 * i, 10 * i]:
                risset.append(j)

        samples = []
        for t in range(int(utils_sec(20))):
            samples.append(0.01 * RissetMixGeneration.sines(risset, t))
        return samples
