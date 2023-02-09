import random
import numpy as np
import sounddevice as sd


class BeepGenerator:
    def __init__(self, max_freq, max_duration_s, samplerate, amplitude, max_duration_ms=None):
        self.__MAX_FREQUENCY = max_freq
        self.__MAX_DURATION = max_duration_s
        self.__MAX_DURATION_MS = max_duration_ms  # for using win_beep
        self.__samplerate = samplerate  # set a bit rate
        self.__amplitude = amplitude

    def __repr__(self):
        return \
            'Max frequency: {}\n' \
            'Max duration: {}\n' \
            'Max duration(ms, for winsound): {}\n' \
            'Samplerate: {}\n' \
            'Amplitude: {}' \
                .format(self.__MAX_FREQUENCY, self.__MAX_DURATION, self.__MAX_DURATION_MS, self.__samplerate,
                        self.__amplitude)

    def generate_random_beep_np(self):
        random_frequency = random.randint(1, self.__MAX_FREQUENCY)
        random_duration = random.randint(1, self.__MAX_DURATION)
        new_time = np.arange(random_duration * self.__samplerate) / self.__samplerate
        signal = self.__amplitude * np.sin(2 * np.pi * random_frequency * new_time)
        sd.play(signal)
        sd.wait()

    @property
    def samplerate(self):
        return self.__samplerate

    @samplerate.setter
    def samplerate(self, new_samplerate):
        self.samplerate = new_samplerate
