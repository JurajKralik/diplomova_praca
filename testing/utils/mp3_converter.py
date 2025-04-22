from pydub import AudioSegment
import os
from tkinter import filedialog

def convert_mp3_to_wav(input_folder, output_folder):
	os.makedirs(output_folder, exist_ok=True)

	folder_size = len(os.listdir(input_folder))
	current_file = 0
	
	for filename in os.listdir(input_folder):
		current_file += 1
		if filename.endswith('.mp3'):
			mp3_path = os.path.join(input_folder, filename)
			wav_filename = os.path.splitext(filename)[0] + '.wav'
			wav_path = os.path.join(output_folder, wav_filename)

			# Load and convert
			audio = AudioSegment.from_mp3(mp3_path)
			audio.export(wav_path, format='wav')
			print(f"({current_file}/{folder_size}) Converted: {mp3_path} -> {wav_path} ")

# Example usage
input_path = filedialog.askdirectory()
if not input_path:
    print("No input directory selected.")
    exit()
output_path = filedialog.askdirectory()
if not output_path:
    print("No output directory selected.")
    exit()
convert_mp3_to_wav(input_path, output_path)
