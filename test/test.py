# test examples
'''
the delay function works really well as expected,
given precise time interval between each delay sound and the number of delay sounds,
you can make custom delay effects on audio files
'''
'''
for the speed_down function, it basically works to some extent,
but still very far from what could be considered good,
you can set the parameters of this function to achieve various of slow down effects of the audio,
the suitable parameters for different audio files to get a good slow down effect might be different
'''

# here are the test codes of delay function

import os
import sys

abs_path = os.getcwd()
os.chdir('../audio_effects')
sys.path.append('.')
import audio_effects as ae

os.chdir(abs_path)
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play_sound

current_audio = AudioSegment.from_file('Cmaj7_chord.mp3')
current_bpm = 130
current_interval = ae.bar_to_real_time(3 / 16, current_bpm, 1) / 1000
current_audio_with_delay = ae.delay(current_audio,
                                    interval=current_interval,
                                    unit=10)
#play_sound(current_audio_with_delay)

# here are the test codes of speed_down function

test_length = len(current_audio)
speed_change_ratio = 0.7
current_audio_slow_down = ae.speed_down(current_audio, speed_change_ratio)
#play_sound(current_audio_slow_down)
#print(len(current_audio_slow_down), len(current_audio) / speed_change_ratio)
