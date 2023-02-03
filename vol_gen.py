import random
import numpy as np
import sounddevice as sd
import simpleaudio as sa
import wavio
import math
from pydub import AudioSegment
from pydub.playback import play
from wavefile import WaveWriter
from scipy.integrate import odeint

class CONSTANTS_SOUND:
        CF = 1497.
        MU = 8.9e-4
        RHO_WATER = 998.
        GTH = 1.6e6
        GAMMA = 1.4
        G = 9.8
        SIGMA = 0.072
        ETA = 0.84
        PATM = 101325.

class BeepGenerator:
    def __init__(self, max_freq, max_duration_s, samplerate, amplitude, max_duration_ms=None):
        self.__MAX_FREQUENCY = max_freq
        self.__MAX_DURATION = max_duration_s
        self.__MAX_DURATION_MS = max_duration_ms     # for using win_beep
        self.__samplerate = samplerate       # set a bit rate
        self.__amplitude = amplitude

    def __repr__(self):
        return \
            'Max frequency: {}\n' \
            'Max duration: {}\n' \
            'Max duration(ms, for winsound): {}\n' \
            'Samplerate: {}\n' \
            'Amplitude: {}'\
            .format(self.__MAX_FREQUENCY, self.__MAX_DURATION, self.__MAX_DURATION_MS, self.__samplerate, self.__amplitude)

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

class WhiteNoise:
    def __init__(self, samples, samplerate, filename):
        self.samples = samples
        self.samplerate = samplerate
        self.filename = filename


    def generate(self):
        x = []
        l = []

        x.append(np.random.random(size = self.samples))

        for i in x:
            for j in i:
                l.append(j)

        l = np.array(l)

        wavio.write(self.filename, l, self.samplerate, sampwidth=2)


    def playNoise(self):
        song = AudioSegment.from_wav(self.filename)
        play(song)

# Class to play bubble sounds
class BubbleSound:
    def __init__(self):
        self.moving_type = 1
        self.interface_type = 1

    def change_type(self, t):
        if t == 1 or t == 2:
            self.moving_type = t

    def change_interface(self, t):
        if t == 1 or t == 2:
            self.interface_type = t

    def bubble_capacitance(self, r, d):
        if self.interface_type == 1: # fluid
            C = r / (1.0 - r / (2 * d) - (r / (2*d))**4)
        else: # Rigid interface
            C = r / (1.0 + r / (2 * d) - (r / (2*d))**4)

        return C


    def minnaert_freq(self, r, d):
        omega = math.sqrt(3 * CONSTANTS_SOUND.GAMMA * CONSTANTS_SOUND.PATM - 2 * CONSTANTS_SOUND.SIGMA * r) / (r * math.sqrt(CONSTANTS_SOUND.RHO_WATER))

        f = omega / 2 / math.pi
        return f

    def actual_freq(self, r, d):
        C = self.bubble_capacitance(r, d)

        p0 = CONSTANTS_SOUND.PATM
        v0 = 4.0/3.0 * math.pi * r**3
        omega = math.sqrt(4.0 * math.pi * CONSTANTS_SOUND.GAMMA * p0 * C / (CONSTANTS_SOUND.RHO_WATER * v0))
        f = omega / 2 / math.pi

        return f


    def calc_beta(self, r, w0):
        dr = w0 * r / CONSTANTS_SOUND.CF
        dvis = 4. * CONSTANTS_SOUND.MU / (CONSTANTS_SOUND.RHO_WATER * w0 * r**2)
        phi = 16. * CONSTANTS_SOUND.GTH * CONSTANTS_SOUND.G / (9 * (CONSTANTS_SOUND.GAMMA-1)**2 * w0)
        dth = 2*(math.sqrt(phi - 3.) - (3. * CONSTANTS_SOUND.GAMMA - 1.) /
                 (3. * (CONSTANTS_SOUND.GAMMA - 1))) / (phi - 4)

        dtotal = dr + dvis + dth

        return w0 * dtotal / math.sqrt(dtotal**2 + 4)

    def jet_forcing(self, r, t):
        cutoff = min(.0006, 0.5 / (3.0 / r))

        if t < 0 or t > cutoff:
            return 0


        jval = (-9 * CONSTANTS_SOUND.GAMMA * CONSTANTS_SOUND.SIGMA * CONSTANTS_SOUND.ETA *
                (CONSTANTS_SOUND.PATM + 2 * CONSTANTS_SOUND.SIGMA/r) * math.sqrt(1 + CONSTANTS_SOUND.ETA**2) /
                (4 * CONSTANTS_SOUND.RHO_WATER**2 * r**5 ) * t**2)

        # Convert to radius (instead of fractional radius)
        jval *= r

        # Convert to pressure
        mrp = CONSTANTS_SOUND.RHO_WATER * r
        jval *= mrp

        return jval

    def bubble_terminal_velocity(self, r):
        d = 2 * r

        del_rho = 997. # Density difference between the phases

        # eq 2
        vtpot = 1./36. * del_rho * CONSTANTS_SOUND.G * d**2 / CONSTANTS_SOUND.MU

        # eq 6
        vt1 = vtpot * math.sqrt(1 + 0.73667 * math.sqrt(CONSTANTS_SOUND.G * d) / vtpot)

        # eq 8
        vt2 = math.sqrt(3 * CONSTANTS_SOUND.SIGMA / CONSTANTS_SOUND.RHO_WATER / d + G * d * del_rho / 2 / RHO_WATER)

        # eq 1
        vt = 1 / math.sqrt( 1 / vt1**2 + 1/vt2**2 )

        return vt

    def bubble_integrator(self, y, t, r, d0, dt, of):
        #[f'; f]

        f = self.jet_forcing(r, t - 0.1)

        d = d0
        if self.moving_type == 2 and t >= 0.1: # rising bubble, calc depth
            vt = self.bubble_terminal_velocity(r)

            d = max(0.51 * 2 * r, d0 - (t - 0.1) * vt)

        if t > 0.11 and math.sqrt(y[0]**2 + y[1]**2) < 1e-15:
            return [0, 0]

        p0 = CONSTANTS_SOUND.PATM + 2.0 * CONSTANTS_SOUND.SIGMA / r
        v0 = 4./3. * math.pi * r**3

        w0 = self.actual_freq(r, d) * 2 * math.pi
        k = CONSTANTS_SOUND.GAMMA * p0 / v0
        m = k / w0**2

        beta = self.calc_beta(r, w0)

        acc = f / m - 2 * beta * y[0] - w0**2 * y[1]

        if of:
            of.write(str(w0 / 2 / math.pi) + ' ' + str(y[0]) + '\n')

        #print(y)
        if np.isnan(acc) or max(y) > 1e-4:
            print('y: ' + str(y))
            print('f: ' + str(f))
            print('m: ' + str(m))
            print('w0: ' + str(w0))
            print('beta: ' + str(beta))
            print('t: ' + str(t))

            raise Exception('nan')

        return [acc, y[0]]


    def play_bubble(self, r, d, save_file):
        numsteps = 96001
        dt = 1./(numsteps-1)
        t = np.linspace(0, 1, numsteps-1)
        y0 = [0, 0]


        sol = odeint(self.bubble_integrator,
                     y0,
                     t,
                     args=(r / 1000., d * 8. / 1000. * 2., dt, None),       # convert to valid sound
                     hmax = dt)

        p = sol[:,1]

        p /= max(p.min(), p.max()) * 1.05

        # Save to wave file
        if save_file:
            with WaveWriter('assets/bub.wav', channels=1, samplerate = numsteps-1) as w :
                ps = np.reshape(p, (1, len(p)))
                w.write(ps)

        p *= 32767
        p = p.astype(np.int16)

        play_obj = sa.play_buffer(p, 1, 2, numsteps-1)

        play_obj.wait_done()
