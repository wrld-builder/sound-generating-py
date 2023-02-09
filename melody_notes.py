import numpy as np

class MelodyNotesGenerator:
    def __init__(self, samplerate):
        self.__BIT_COUNT = 2 ** 16  # 16-bit sound
        self.__samplerate = samplerate  # set a bit rate
        self.__notes_freq_array = np.array([261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88])  # notes [1 oct.]

    def generate_sample(self, frequency, duration, volume):
        new_amplitude = np.round(volume * self.__BIT_COUNT)
        total_samples_count = np.round(self.__samplerate * duration)
        new_frequency = float(2) * np.pi * frequency / self.__samplerate
        return np.round(new_amplitude * np.sin(np.arange(0, total_samples_count) * new_frequency))

    def generate_tones(self, duration):
        tones = []

        for freq in self.__notes_freq_array:
            tone = np.array(self.generate_sample(freq, duration, 1.0), dtype=np.int16)
            tones.append(tone)
        return tones

    @property
    def samplerate(self):
        return self.__samplerate

    @samplerate.setter
    def samplerate(self, new_rate):
        self.__samplerate = new_rate
