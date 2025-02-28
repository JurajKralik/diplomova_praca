from IPython.display import Audio
from scipy.io import wavfile
import numpy as np
import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer


def use_wav2vec(file: str) -> str:
    # Check if file exists
    try:
        with open(file) as r:
            print("# File found")
    except FileNotFoundError:
        print("# File not found")
        exit()

    Audio(filename=file)
    data = wavfile.read(file)
    framerate = data[0]
    sounddata = data[1]
    time = np.arange(0, len(sounddata))/framerate
    print(framerate)
    print('# Total time:', len(sounddata)/framerate)

    # Model
    tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
    print('# Model loaded')

    input_audio, _ = librosa.load(file, sr=16000)
    input_values = tokenizer(input_audio, return_tensors="pt").input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    text: str = tokenizer.batch_decode(predicted_ids)[0]
    text = text.lower()
    print('# Done')
    return text
