import numpy as np
import pydub
# apt-get install libav-tools libavcodec-extra

def create_good_bad_sound(filename: str):
    soundGood = pydub.AudioSegment.from_mp3(filename)
    soundGood = soundGood.set_channels(1).set_frame_rate(5000)
    soundBad = soundGood
    soundBad = soundBad.set_frame_rate(4900)
    return (soundGood, soundBad)

def generator_10sec_song(sound: pydub.AudioSegment, duration: int = 100):
    while len(sound) > duration:
        yield sound[:duration]
        sound = sound[duration:]
    yield sound

def generator_bad_and_good_sound(mp3):
    (soundGood, soundBad) = create_good_bad_sound(mp3)
    good_gen = generator_10sec_song(soundGood)
    bad_gen = generator_10sec_song(soundBad)
    for g, b in zip(good_gen, bad_gen):
        yield(([[x / 255. for x in b.raw_data]]), ([[y / 255. for y in g.raw_data]]))

if __name__ == '__main__':
    import download_data
    for path in download_data.getFileIterator():
        for a in generator_bad_and_good_sound(path):
            print('len(sound[0]):', len(a[0]))
            print('len(sound[1]):', len(a[1]))
            break
        break
