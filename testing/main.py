from testing_speech_recognition import SpeechRecognitionModel
from testing_whisper import WhisperModel
from testing_wav2vec import Wav2Vec2Model
import json
import os
import tkinter as tk
from tkinter import filedialog
import time



def select_folder():
    new_path = filedialog.askdirectory()
    if new_path:
        folder_path.set(new_path)

def save_transcription(output_path: str, file_name: str, transcript: str, elapsed_time: float):
    """Saves transcription output to a JSON file with a unique serial number."""
    if not os.path.exists(output_path):
        with open(output_path, "w", encoding="utf-8") as json_file:
            json.dump({"results": []}, json_file, ensure_ascii=False, indent=4)

    with open(output_path, "r+", encoding="utf-8") as json_file:
        data = json.load(json_file)
        result_entry = {
            "file_name": file_name,
            "transcript": transcript,
            "elapsed_time": elapsed_time
        }
        data["results"].append(result_entry)
        json_file.seek(0)
        json.dump(data, json_file, ensure_ascii=False, indent=4)
        json_file.truncate()

def transcribe():
    audio_folder = folder_path.get()
    if not audio_folder:
        result_text.set("Please select an audio folder.")
        return
    
    output_dir = "testing/output/output.json"
    serial_number = 1
    while os.path.exists(output_dir):
        base, ext = os.path.splitext("testing/output/output")
        output_dir = f"{base}_{serial_number}{ext}.json"
        serial_number += 1

    print(f"Output will be saved to: {output_dir}")
    model_choice = model_var.get()

    output = {"model": model_choice, "results": []}
    with open(output_dir, "w", encoding="utf-8") as json_file:
        json.dump(output, json_file, ensure_ascii=False, indent=4)

    total_time_start = time.time()

    folder_size = len(os.listdir(folder_path.get()))
    current_file = 0

    if model_choice == "Speech Recognition":
        model = SpeechRecognitionModel()
    elif model_choice == "Whisper":
        model = WhisperModel()
    elif model_choice == "Wav2Vec":
        model = Wav2Vec2Model()
    else:
        print("Please select a model.")
        return

    for file_name in os.listdir(folder_path.get()):
        current_file += 1
        print("Processing file:", file_name, f"({current_file}/{folder_size})")

        start_time = time.time()
        if file_name.lower().endswith(('.wav', '.mp3', '.flac')):
            full_path = os.path.join(folder_path.get(), file_name)
            transcript = model.transcribe(full_path)
            end_time = time.time()
            elapsed_time = end_time - start_time
            save_transcription(output_dir, file_name, transcript, elapsed_time)
            print(f"Transcription for {file_name} completed in {elapsed_time:.2f} seconds.")
        else:
            print(f"File {file_name} is not a valid audio file.")
            continue
    total_time_taken = time.time() - total_time_start
    with open(output_dir, "r+", encoding="utf-8") as json_file:
        data = json.load(json_file)
        data["total_time_taken"] = total_time_taken
        json_file.seek(0)
        json.dump(data, json_file, ensure_ascii=False, indent=4)
        json_file.truncate()
    print(f"Done! Total time taken: {total_time_taken:.2f} seconds")

# GUI
root = tk.Tk()
root.title("Speech Recognition GUI")
root.geometry("450x300")

folder_path = tk.StringVar()
model_var = tk.StringVar(value="Model 1")
result_text = tk.StringVar()

# File selection button
folder_button = tk.Button(root, text="Select Folder", command=select_folder)
folder_button.pack(pady=10)

folder_label = tk.Label(root, textvariable=folder_path, wraplength=500)
folder_label.pack(pady=5)

# Model selection
model_frame = tk.LabelFrame(root, text="Select Model")
model_frame.pack(pady=10)

for model in ["Speech Recognition", "Whisper", "Wav2Vec"]:
    tk.Radiobutton(model_frame, text=model, variable=model_var, value=model).pack(anchor="w")

# Transcribe button
transcribe_button = tk.Button(root, text="Transcribe", command=transcribe)
transcribe_button.pack(pady=10)

root.mainloop()
