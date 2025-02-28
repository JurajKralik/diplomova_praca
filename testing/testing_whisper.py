import whisper


file_name = 'C:\\Users\\DAX\\Desktop\\School\\_Diplomová práca\\testing\\test_short.wav'
model = whisper.load_model("turbo")
result = model.transcribe(file_name)
print(result["text"])