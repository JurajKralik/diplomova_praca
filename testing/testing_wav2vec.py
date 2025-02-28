from IPython.display import Audio
from scipy.io import wavfile
import numpy as np

file_name = 'test.wav'
Audio(file_name)
data = wavfile.read(file_name)
framerate = data[0]
sounddata = data[1]
time = np.arange(0, len(sounddata))/framerate
print(framerate)
print('Total time:', len(sounddata)/framerate)