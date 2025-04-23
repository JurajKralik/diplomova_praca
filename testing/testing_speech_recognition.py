import speech_recognition

class SpeechRecognitionModel:
    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()

    def transcribe(self, file: str) -> str:
        with speech_recognition.AudioFile(file) as source:
            audio = self.recognizer.record(source)
            try:
                text: str = self.recognizer.recognize_google(audio, show_all=False)
                text = text.lower()
            except speech_recognition.UnknownValueError:
                # Cannot understand the audio - too noisy or unclear
                text = None
            else:
                text: str = self.recognizer.recognize_google(audio)
                text = text.lower()
            
            return text