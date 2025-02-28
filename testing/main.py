from testing_speech_recognition import use_speech_recognition
from testing_whisper import use_whisper
from testing_wav2vec import use_wav2vec
import tkinter as tk
from tkinter import filedialog, scrolledtext



def select_file():
    file_path.set(filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.flac")]))

def transcribe():
    audio_file = file_path.get()
    if not audio_file:
        result_text.set("Please select an audio file.")
        return
    
    model_choice = model_var.get()
    if model_choice == "Speech Recognition":
        transcript = use_speech_recognition(audio_file)
    elif model_choice == "Whisper":
        transcript = use_whisper(audio_file)
    elif model_choice == "Wav2Vec":
        transcript = use_wav2vec(audio_file)
    else:
        transcript = "Please select a model."
    
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, transcript)

# GUI
root = tk.Tk()
root.title("Speech Recognition GUI")
root.geometry("600x400")

file_path = tk.StringVar()
model_var = tk.StringVar(value="Model 1")
result_text = tk.StringVar()

# File selection button
file_button = tk.Button(root, text="Select Audio File", command=select_file)
file_button.pack(pady=10)

file_label = tk.Label(root, textvariable=file_path, wraplength=500)
file_label.pack(pady=5)

# Model selection
model_frame = tk.LabelFrame(root, text="Select Model")
model_frame.pack(pady=10)

for model in ["Speech Recognition", "Whisper", "Wav2Vec"]:
    tk.Radiobutton(model_frame, text=model, variable=model_var, value=model).pack(anchor="w")

# Transcribe button
transcribe_button = tk.Button(root, text="Transcribe", command=transcribe)
transcribe_button.pack(pady=10)

# Text output area
text_output = scrolledtext.ScrolledText(root, width=70, height=10, wrap=tk.WORD)
text_output.pack(pady=10)

root.mainloop()
