import numpy as np
import pydub
# apt-get install libav-tools libavcodec-extra

def create_high_low_sound(filename: str):
    soundHigh = pydub.AudioSegment.from_mp3(filename)
    soundHigh = soundHigh.set_channels(1).set_frame_rate(5000)
    soundLow = soundHigh
    soundLow = soundLow.set_frame_rate(4900)
    return (soundHigh, soundLow)

def generator_10sec_song(sound: pydub.AudioSegment, duration: int = 100):
    while len(sound) > duration:
        yield sound[:duration]
        sound = sound[duration:]
    yield sound

def generator_low_and_high_sound(mp3):
    (soundHigh, soundLow) = create_high_low_sound(mp3)
    high_gen = generator_10sec_song(soundHigh)
    low_gen = generator_10sec_song(soundLow)
    for g, b in zip(high_gen, low_gen):
        yield(([[x / 255. for x in l.raw_data]]), ([[y / 255. for y in h.raw_data]]))

if __name__ == '__main__':
    import download_data
    for path in download_data.getFileIterator():
        for a in generator_low_and_high_sound(path):
            print('len(sound[0]):', len(a[0]))
            print('len(sound[1]):', len(a[1]))
            break
        break
