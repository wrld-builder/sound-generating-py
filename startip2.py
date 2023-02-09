M = 32
ON = 0.5
OFF = 0
T1 = 6
T2 = 54


class Startip2Generation:
    def __init__(self):
        pass

    @staticmethod
    def decimate(samples, m):
        x_pos = 0
        x_delay = [0] * m
        y = 0
        for i, x in enumerate(samples):
            y += x - x_delay[x_pos]
            x_delay[x_pos] = x
            x_pos = (x_pos + 1) % len(x_delay)
            samples[i] = y / m
        return samples[::m]

    @staticmethod
    def out(samples, x, t):
        samples += [x] * t

    @staticmethod
    def engine(samples, dur, t1, t2, vol, periods):
        counters = periods[:]
        t1_counter = t1
        t2_counter = t2
        update_counter = t1
        width = 1
        is_slide_up = True
        for d in range(dur):
            for i in range(3):
                counters[i] -= 1
                if counters[i] == 0:
                    Startip2Generation.out(samples, ON, width * T1)
                    Startip2Generation.out(samples, OFF, (16 - width) * T1)
                    counters[i] = periods[i]
            update_counter -= 1
            if update_counter == 0:
                update_counter = 10
                if is_slide_up:
                    t1_counter -= 1
                    if t1_counter == 0:
                        t1_counter = t1
                        width += 1
                        if width == 15:
                            width = 14
                            is_slide_up = False
                else:
                    t2_counter -= 1
                    if t2_counter == 0:
                        t2_counter = t2
                        if width - 1 != vol:
                            width -= 1
            Startip2Generation.out(samples, samples[-1], T2)

    @staticmethod
    def play(samples, frames):
        dur = 0
        vol = 0
        t1 = 0
        t2 = 0
        i = 0
        while frames[i] != 0:
            if frames[i] == 0xff:
                dur = frames[i + 2] << 8 | frames[i + 1]
                t1, t2, vol = frames[i + 3:i + 6]
                i += 6
            else:
                Startip2Generation.engine(samples, dur, t1, t2, vol, frames[i: i + 3])
                i += 3

    @staticmethod
    def generate_startip2_samples():
        samples = [0]

        with open("tmp/startip2.txt") as f:
            frames = [int(x, 16) for x in f.read().split()]
            Startip2Generation.play(samples, frames)
        return Startip2Generation.decimate(samples, M)
