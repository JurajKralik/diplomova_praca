from testing_speech_recognition import use_speech_recognition
from testing_whisper import use_whisper
from testing_wav2vec import use_wav2vec
import json
import os
import tkinter as tk
from tkinter import filedialog, scrolledtext



def select_file():
    file_path.set(filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.flac")]))

def save_transcription(model_used: str, file_name: str, output: str):
    """Saves transcription output to a JSON file with a unique serial number."""
    
    base_name = f"{model_used}_{os.path.splitext(os.path.basename(file_name))[0]}"
    serial_number = 1
    
    # Serial number
    while os.path.exists(f"{base_name}_{serial_number}.json"):
        serial_number += 1
    
    file_path = f"{base_name}_{serial_number}.json"

    # Save
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({"text": output}, f, ensure_ascii=False, indent=4)

    print(f"Transcription saved to {file_path}")
    return

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
    save_transcription(model_choice, audio_file, transcript)
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
