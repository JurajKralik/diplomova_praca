import speech_recognition


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