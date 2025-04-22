import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor


class Wav2Vec2Model:
    def __init__(self):
        self.processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")
        self.model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")

    def transcribe(self, file: str) -> str:
        # Check if file exists
        try:
            with open(file) as r:
                pass
        except FileNotFoundError:
            exit()

        input_audio, _ = librosa.load(file, sr=16000)
        input_values = self.processor(input_audio, sampling_rate=16000, return_tensors="pt").input_values
        logits = self.model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        text: str = self.processor.batch_decode(predicted_ids)[0]
        text = text.lower()

        return text
