# audio_effects
 This is a python package with some audio effects functions such as delay, speed changes implemented in python, with the help of pydub and numpy.

# Usage
## delay
This `delay` function adds delay effects to audio using pydub, the delay sounds would be decreasing volume one by one, placing at a interval one after another after the original sound. The return value is a new pydub AudioSegment instance with the delay effects added.
```python
delay(sound, interval=0.5, unit=6, volumes=None, decrease_unit=None)

# sound: a pydub AudioSegment instance

# interval: the time between each delay sound in seconds

# unit: the number of the delay sounds

# volumes: you can specify the volume of each delay sound using this parameter,
# could be a list or tuple, the elements are volume percentages (from 0 to 100)

# decrease_unit: you can specify the decrease unit (in percentages) of the volumes of the delay sounds using this parameter


# examples
current_audio = AudioSegment.from_file('Cmaj7_chord.mp3')
current_bpm = 130
current_interval = ae.bar_to_real_time(3 / 16, current_bpm, 1) / 1000
current_audio_with_delay = ae.delay(current_audio,
                                    interval=current_interval,
                                    unit=10)
```
The delay function works really well as expected, given precise time interval between each delay sound and the number of delay sounds, you can make custom delay effects on audio files.

## speed down
There is already a `speedup` function implemented in pydub, which is useful, but currently there are no speed down function in pydub, so I give it a try.

This `speed_down` function is my attempt at making a speed down function of pydub AudioSegment, the basic idea is firstly we cut the sound into n pieces of chunks, and then we copy each chunk and paste it right after itself, we use the speed changes to determine how much copies of each chunk we should get, and then put every chunk with its copied chunks back to a silent audio of length after speed changes, then we can get the slow down audio while remain the pitch unchanged. The return value is a new pydub AudioSegment instance that the speed slows down.

Update 2021/9/8 It basically works now to some extent, but still very far from what could be considered good, you can set the parameters of this function to achieve various of slow down effects of the audio, the suitable parameters for different audio files to get a good slow down effect might be different.

```python
speed_down(sound,
           speed_changes,
           chunk_size=50,
           crossfade=25,
           merge_crossfade=25,
           crossfade_threshold=10)

# sound: a pydub AudioSegment instance

# speed_changes: the ratio of the speed to change, 1 means no speed changes,
# < 1 means slow down, for example, 0.5 means half the speed,
# note that this function only works for speed to slow down, if you want to speed up, please use
# the speedup function of pydub, which you pass speed ratio > 1 to speed up the audio

# chunk_size: the chunk size of the audio to be cut in, in ms

# crossfade: the time of fading effects between 2 adjacent chunks when concatenating
# the duplicates of each chunk, in ms

# merge_crossfade: the time of fading effects between 2 adjacent chunks when concatenating
# the chunks after the duplicating process, in ms

# crossfade_threshold: the minimum value of crossfade, in ms


# examples
current_audio = AudioSegment.from_file('Cmaj7_chord.mp3')
speed_change_ratio = 0.7
current_audio_slow_down = ae.speed_down(current_audio, speed_change_ratio)
```
