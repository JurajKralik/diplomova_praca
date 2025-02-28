import speech_recognition


def use_speech_recognition(file: str) -> str:
    recognizer = speech_recognition.Recognizer()
    with speech_recognition.AudioFile(file) as source:
        audio = recognizer.record(source)
        text: str = recognizer.recognize_google(audio)
        text = text.lower()
        return text

def use_microphone():
    while True:
        print("Listening...")
        try:
            with speech_recognition.Microphone() as mic:
                recognizer = speech_recognition.Recognizer()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                text: str = recognizer.recognize_google(audio)
                text = text.lower()

                if text == "stop":
                    print("Stopped")
                    break

                print(text)

        except speech_recognition.UnknownValueError():

            recognizer = speech_recognition.Recognizer()
            continue