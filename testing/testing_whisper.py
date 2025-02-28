import whisper


def use_whisper(file_name: str) -> str:
    model = whisper.load_model("turbo")
    print("# Model loaded")

    result = model.transcribe(file_name)
    print("# Done")
    
    return result
