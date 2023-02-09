from bell_sound_gen import BellGeneration
from sounddevice import play as sd_play
from sounddevice import wait as sd_wait

if __name__ == '__main__':
    sd_play(BellGeneration.generate_bell_sound(time_s=1))       # bell generation?
    sd_wait()
