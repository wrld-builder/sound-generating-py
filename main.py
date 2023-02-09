from risset_mix_gen import RissetMixGeneration
from startip2 import Startip2Generation
from on_the_run_like_gen import OnTheRunGeneration
from cham_the_run_like_gen import ChamGeneration
from sounddevice import play as sd_play
from sounddevice import wait as sd_wait

if __name__ == '__main__':
    r = RissetMixGeneration.generate_risset_samples()
    sd_play(r)
    sd_wait()

    sd_play(Startip2Generation.generate_startip2_samples())
    sd_wait()

    sd_play(OnTheRunGeneration.generate_on_the_run_samples())
    sd_wait()

    sd_play(ChamGeneration.generate_cham_samples())
    sd_wait()
