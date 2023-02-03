import vol_gen

if __name__ == '__main__':
    # noise = vol_gen.WhiteNoise(300000, 44100, "assets/noise.wav")
    # noise.generate()
    # noise.playNoise()

    sound = vol_gen.BubbleSound()
    for i in range(10):
        sound.play_bubble(8.0, 1.0, 0)
