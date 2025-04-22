import whisper


class WhisperModel:
    def __init__(self):
        self.model = whisper.load_model("turbo")

    def transcribe(self, file_name: str) -> str:
        result = self.model.transcribe(file_name)
        return result["text"]
