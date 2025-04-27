from testing_speech_recognition import SpeechRecognitionModel
from testing_whisper import WhisperModel
from testing_wav2vec import Wav2Vec2Model
import json
import os
import tkinter as tk
from tkinter import filedialog
import time
from concurrent.futures import ProcessPoolExecutor, as_completed


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

def transcribe_file(model_choice, audio_path, file_name):
    if model_choice == "Speech Recognition":
        model = SpeechRecognitionModel()
    elif model_choice == "Whisper":
        model = WhisperModel()
    elif model_choice == "Wav2Vec":
        model = Wav2Vec2Model()
    else:
        raise ValueError("Invalid model choice.")

    start_time = time.time()
    transcript = model.transcribe(audio_path)
    elapsed_time = time.time() - start_time
    return {
        "file_name": file_name,
        "transcript": transcript,
        "elapsed_time": elapsed_time
    }

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

    audio_files = [
        file_name for file_name in os.listdir(audio_folder)
        if file_name.lower().endswith(('.wav', '.mp3', '.flac'))
    ]
    folder_size = len(audio_files)

    # Use multiprocessing
    futures = []
    with ProcessPoolExecutor(max_workers=process_var.get()) as executor:
        for file_name in audio_files:
            full_path = os.path.join(audio_folder, file_name)
            futures.append(executor.submit(transcribe_file, model_choice, full_path, file_name))

        for idx, future in enumerate(as_completed(futures), 1):
            result_entry = future.result()
            save_transcription(output_dir, result_entry["file_name"], result_entry["transcript"], result_entry["elapsed_time"])
            print(f"({idx}/{folder_size}) {result_entry['file_name']} done in {result_entry['elapsed_time']:.2f}s")

    total_time_taken = time.time() - total_time_start
    with open(output_dir, "r+", encoding="utf-8") as json_file:
        data = json.load(json_file)
        data["total_time_taken"] = total_time_taken
        json_file.seek(0)
        json.dump(data, json_file, ensure_ascii=False, indent=4)
        json_file.truncate()

    print(f"Done! Total time taken: {total_time_taken:.2f} seconds")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Speech Recognition GUI")
    root.geometry("400x400")

    folder_path = tk.StringVar()
    model_var = tk.StringVar(value="Model 1")
    result_text = tk.StringVar()

    # File selection button
    folder_button = tk.Button(root, text="Select Folder", command=select_folder)
    folder_button.pack(pady=10)

    folder_label = tk.Label(root, textvariable=folder_path, wraplength=500)
    folder_label.pack(pady=5)
    # Parallel processes selection
    process_frame = tk.LabelFrame(root, text="Parallel Processes")
    process_frame.pack(pady=10)

    max_cores = os.cpu_count()
    process_var = tk.IntVar(value=max_cores)

    tk.Scale(
        process_frame,
        from_=1,
        to=max_cores,
        orient="horizontal",
        variable=process_var,
        label="Number of Processes"
    ).pack()
    # Model selection
    model_frame = tk.LabelFrame(root, text="Select Model")
    model_frame.pack(pady=10)

    for model in ["Speech Recognition", "Whisper", "Wav2Vec"]:
        tk.Radiobutton(model_frame, text=model, variable=model_var, value=model).pack(anchor="w")

    # Transcribe button
    transcribe_button = tk.Button(root, text="Transcribe", command=transcribe)
    transcribe_button.pack(pady=10)

    root.mainloop()
