from utils import sec as utils_sec
from bell_sound_gen import Sine as bell_sound_sine

class Saw:
  def __init__(self):
    self.o = bell_sound_sine()
    self.fb = 0

  def next(self, freq, cutoff=2):
    o = self.o.next(freq, cutoff * self.fb)
    self.fb = (o + self.fb) * 0.5
    return self.fb

class Lp1:
  def __init__(self):
    self.y = 0

  def next(self, x, cutoff):
    self.y += cutoff * (x - self.y)
    return self.y

ON_THE_RUN = [82.41, 98, 110, 98, 146.83, 130.81, 146.83, 164.81]

class OnTheRunGeneration():
    def __init__(self):
        pass

    @staticmethod
    def generate_on_the_run_samples():
        osc1 = Saw()
        lfo1 = bell_sound_sine()
        flt1 = Lp1()
        flt2 = Lp1()
        flt3 = Lp1()
        flt4 = Lp1()

        samples = []

        for bars in range(16):
          for freq in ON_THE_RUN:
            for t in range(int(utils_sec(0.09))):
              x = osc1.next(freq)
              cutoff = 0.5 + lfo1.next(0.2) * 0.4
              x = flt1.next(x, cutoff)
              x = flt2.next(x, cutoff)
              x = flt3.next(x, cutoff)
              x = flt4.next(x, cutoff)
              samples.append(0.5 * x)

        return samples
