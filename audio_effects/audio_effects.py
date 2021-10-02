from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play_sound
from copy import deepcopy as copy
import math


def velocity_to_db(vol):
    if vol == 0:
        return -100
    return math.log(vol / 127, 10) * 20


def percentage_to_db(vol):
    if vol == 0:
        return -100
    return math.log(abs(vol / 100), 10) * 20


def bar_to_real_time(bar, bpm, mode=0):
    # return time in ms
    return int(
        (60000 / bpm) * (bar * 4)) if mode == 0 else (60000 / bpm) * (bar * 4)


def real_time_to_bar(time, bpm):
    return (time / (60000 / bpm)) / 4


def delay(sound, interval=0.5, unit=6, volumes=None, decrease_unit=None):
    # delay effect using pydub, the delay sounds would be decreasing volume one by one,
    # placing at a interval one after another after the original sound

    # sound: a pydub AudioSegment instance

    # interval: the time between each delay sound in seconds

    # unit: the number of the delay sounds

    # volumes: you can specify the volume of each delay sound using this parameter,
    # could be a list or tuple, the elements are volume percentages (from 0 to 100)

    # decrease_unit: you can specify the decrease unit (in percentages) of the volumes of the delay sounds using this parameter
    '''
    # examples
    
    test_audio = AudioSegment.from_file('C5.wav')
    test_audio_with_delay = delay(test_audio, 0.2, 15)
    play_sound(test_audio_with_delay)
    # test_audio_with_delay.export('C5 with delay.wav')
    
    '''
    if volumes:
        unit = len(volumes)
    whole_length = (unit * interval * 1000) + len(sound)
    result = AudioSegment.silent(duration=whole_length)
    result = result.overlay(sound, position=0)
    if not volumes:
        volume_unit = 100 / unit if decrease_unit is None else decrease_unit
        volumes = [100 - i * volume_unit for i in range(1, unit + 1)]
        volumes = [i if i >= 0 else 0 for i in volumes]
        volumes = [percentage_to_db(i) for i in volumes]
    else:
        volumes = [percentage_to_db(i) for i in volumes]
    for i in range(unit):
        current_volume = volumes[i]
        current = sound + current_volume
        result = result.overlay(current, position=interval * (i + 1) * 1000)
    return result


def pitch_change(sound,
                 semitones,
                 chunk_size=150,
                 crossfade=25,
                 merge_crossfade=25,
                 crossfade_threshold=10,
                 chunk_size2=50):
    # this is a pitch change function using pydub, it is a lot faster than librosa method,
    # but when you raise the pitch, the speed of the audio cannot preserve very well,
    # so this function will perform speed changes of audio using speedup function which are already
    # implemented in pydub, and speed_down function written by me to keep the speed and length of the audio
    # after pitch changes to not change too much
    new_sample_rate = int(sound.frame_rate * (2.0**(semitones / 12)))
    result = sound._spawn(sound.raw_data,
                          overrides={'frame_rate': new_sample_rate})
    result = result.set_frame_rate(44100)
    speed_changes = len(result) / len(sound)
    if speed_changes != 1:
        if speed_changes > 1:
            result = result.speedup(speed_changes, chunk_size, crossfade)
        else:
            result = speed_down(result, speed_changes, chunk_size2, crossfade,
                                merge_crossfade, crossfade_threshold)
    return result


def reverb(sound):
    pass


def speed_down(sound,
               speed_changes,
               chunk_size=50,
               crossfade=25,
               merge_crossfade=25,
               crossfade_threshold=10):
    # my attempt at making a speed down function of pydub AudioSegment,
    # since currently there are no speed down function in pydub

    # the basic idea is firstly we cut the sound into n pieces of chunks,
    # and then we copy each chunk and paste it right after itself,
    # we use the speed changes to determine how much copies of each chunk we should get,
    # and then put every chunk with its copied chunks back to a silent audio of length after speed changes,
    # then we can get the slow down audio while remain the pitch unchanged

    # Update 2021/9/8 It basically works now to some extent, but still very far from what could be considered good,
    # you can set the parameters of this function to achieve various of slow down effects of the audio,
    # the suitable parameters for different audio files to get a good slow down effect might be different.
    length = len(sound)
    desired_length = length / speed_changes
    chunks_num = int(length / chunk_size) + 1
    chunks = [
        sound[i * chunk_size:(i + 1) * chunk_size +
              (crossfade + merge_crossfade) / 2] for i in range(chunks_num)
    ]
    new_chunk_size = chunk_size / speed_changes
    average_change_size = new_chunk_size - chunk_size
    integer_part = int(average_change_size / chunk_size)
    remain_part = average_change_size - integer_part * chunk_size
    for i in range(chunks_num):
        current = chunks[i]
        current_length = len(current)
        unit = copy(current)
        if i != chunks_num - 1:
            for j in range(integer_part):
                current = current.append(
                    unit,
                    crossfade=crossfade
                    if crossfade <= current_length else current_length)
            if remain_part > 0:
                remain_audio = unit[-remain_part:]
                current_crossfade = crossfade * (remain_part / current_length)
                if current_crossfade < crossfade_threshold:
                    current_crossfade = crossfade_threshold
                    if current_crossfade > remain_part:
                        current_crossfade = 0
                current = current.append(remain_audio,
                                         crossfade=int(current_crossfade))
        else:
            if current_length > 0:
                current_change_size = (current_length /
                                       speed_changes) - current_length
                current_integer_part = int(current_change_size /
                                           current_length)
                current_remain_part = current_change_size - current_integer_part * current_length
                for j in range(current_integer_part):
                    current = current.append(
                        unit,
                        crossfade=crossfade
                        if crossfade <= current_length else current_length)
                if current_remain_part > 0:
                    remain_audio = unit[-current_remain_part:]
                    current_remain_length = len(remain_audio)
                    current_crossfade = current_remain_length * (crossfade /
                                                                 chunk_size)
                    if current_crossfade < crossfade_threshold:
                        current_crossfade = crossfade_threshold
                        if current_crossfade > current_remain_part:
                            current_crossfade = 0
                    current = current.append(remain_audio,
                                             crossfade=int(current_crossfade))
        chunks[i] = current
    result = chunks[0]
    for k in chunks[1:]:
        if len(k) >= merge_crossfade:
            result = result.append(k, crossfade=merge_crossfade)
    return result


def speed_change(sound,
                 speed_changes=1,
                 chunk_size=150,
                 crossfade=25,
                 merge_crossfade=25,
                 crossfade_threshold=10,
                 chunk_size2=50):
    if speed_changes == 1:
        return copy(sound)
    if speed_changes > 1:
        return sound.speedup(speed_changes, chunk_size, crossfade)
    else:
        return speed_down(sound, speed_changes, chunk_size2, crossfade,
                          merge_crossfade, crossfade_threshold)


def chorus(sound):
    pass
