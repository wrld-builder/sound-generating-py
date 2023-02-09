from pydub import AudioSegment
from pydub.playback import play
import wavio
import numpy as np

class WhiteNoise:
    def __init__(self, samples, samplerate, filename):
        self.samples = samples
        self.samplerate = samplerate
        self.filename = filename

    @staticmethod
    def __sample_gen(samples):
        x = []
        l = []

        x.append(np.random.random(size=samples))

        for i in x:
            for j in i:
                l.append(j)

        return np.array(l)

    # white noise np generation
    @staticmethod
    def generate_white_noise(samples):
        return WhiteNoise.__sample_gen(samples)

    def generate_write_wav(self):
        l = WhiteNoise.__sample_gen(self.samples)
        wavio.write(self.filename, l, self.samplerate, sampwidth=2)


    def playNoise(self):
        song = AudioSegment.from_wav(self.filename)
        play(song)