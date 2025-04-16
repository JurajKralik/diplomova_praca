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

def save_transcription(model_used: str, folder: str, file_name: str, output: str, elapsed_time: float):
    """Saves transcription output to a JSON file with a unique serial number."""
    base_name = f"{os.path.splitext(os.path.basename(file_name))[0]}"
    
    file_path = os.path.join(folder, f"{base_name}.json")

    # Save
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({"text": output, "elapsed_time": elapsed_time, "model_used": model_used}, f, ensure_ascii=False, indent=4)

    print(f"Transcription saved to {file_path}, time taken: {elapsed_time:.2f} seconds")
    return

def transcribe():
    audio_file = folder_path.get()
    if not audio_file:
        result_text.set("Please select an audio file.")
        return
    
    output_dir = create_output_dir()
    total_time_start = time.time()
    model_choice = model_var.get()

    for file_name in os.listdir(folder_path.get()):
        start_time = time.time()
        print("Processing file:", file_name)
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
            save_transcription(model_choice, output_dir, full_path, transcript, elapsed_time)
        else:
            print(f"File {file_name} is not a valid audio file.")
            continue
    total_time_taken = time.time() - total_time_start
    print(f"# Transcription done! Total time taken: {total_time_taken:.2f} seconds")

def create_output_dir():
    # Create output directory with a unique serial number
    output_dir = "testing/output/"
    serial_number = 1
    while os.path.exists(f"{output_dir}{serial_number}"):
        serial_number += 1
    os.makedirs(f"{output_dir}{serial_number}", exist_ok=True)
    return f"{output_dir}{serial_number}"

# GUI
root = tk.Tk()
root.title("Speech Recognition GUI")
root.geometry("600x400")

folder_path = tk.StringVar()
model_var = tk.StringVar(value="Model 1")
result_text = tk.StringVar()

# File selection button
file_button = tk.Button(root, text="Select Folder", command=select_folder)
file_button.pack(pady=10)

file_label = tk.Label(root, textvariable=folder_path, wraplength=500)
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
