import speech_recognition

class SpeechRecognitionModel:
    def __init__(self, model:str = "google"):
        self.recognizer = speech_recognition.Recognizer()
        self.model = model

    def transcribe(self, file: str) -> str:
        with speech_recognition.AudioFile(file) as source:
            audio = self.recognizer.record(source)
            try:
                if self.model == "google":
                    text: str = self.recognizer.recognize_google(audio, show_all=False)
                elif self.model == "whisper":
                    text: str = self.recognizer.recognize_whisper(audio)
                else:
                    print("Model not supported")
                    return None
                text = text.lower()
            except speech_recognition.UnknownValueError:
                # Cannot understand the audio - too noisy or unclear
                text = None
            except Exception as e:
                print(f"An error occurred: {e}")
                text = None
            
            return text