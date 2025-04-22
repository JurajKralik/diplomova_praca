from testing_speech_recognition import use_speech_recognition
from testing_whisper import use_whisper
from testing_wav2vec import use_wav2vec
import json
import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
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
        base, ext = os.path.splitext(output_dir)
        output_dir = f"{base}_{serial_number}{ext}"
        serial_number += 1

    print(f"Output will be saved to: {output_dir}")
    model_choice = model_var.get()

    output = {"model": model_choice, "results": []}
    with open(output_dir, "w", encoding="utf-8") as json_file:
        json.dump(output, json_file, ensure_ascii=False, indent=4)

    total_time_start = time.time()

    folder_size = len(os.listdir(folder_path.get()))
    current_file = 0

    for file_name in os.listdir(folder_path.get()):
        current_file += 1
        print("Processing file:", file_name, f"({current_file}/{folder_size})")

        start_time = time.time()
        if file_name.lower().endswith(('.wav', '.mp3', '.flac')):
            full_path = os.path.join(folder_path.get(), file_name)
            model_choice = model_var.get()
            if model_choice == "Speech Recognition":
                transcript = use_speech_recognition(full_path)
            elif model_choice == "Whisper":
                transcript = use_whisper(full_path)
            elif model_choice == "Wav2Vec":
                transcript = use_wav2vec(full_path)
            else:
                print("Please select a model.")
                return
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            text = f"Transcription for {file_name}:\n{transcript}\nTime taken: {elapsed_time:.2f} seconds"
            text_output.delete(1.0, tk.END)
            text_output.insert(tk.END, text)
            save_transcription(output_dir, file_name, transcript, elapsed_time)
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
root.geometry("600x400")

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

# Text output area
text_output = scrolledtext.ScrolledText(root, width=70, height=10, wrap=tk.WORD)
text_output.pack(pady=10)

root.mainloop()
