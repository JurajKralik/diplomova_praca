import csv
from tkinter import filedialog

def get_sentence_for_file(tsv_path, target_filename):
	with open(tsv_path, 'r', encoding='utf-8') as infile:
		reader = csv.DictReader(infile, delimiter='\t')

		for row in reader:
			if row['path'].strip() == target_filename:
				return row['sentence'].strip()

	return None


input_path = filedialog.askopenfile()
if not input_path:
    print("No input file selected.")
    exit()
sentence = get_sentence_for_file(input_path.name, 'common_voice_en_35244283.mp3')
if sentence:
    print(sentence)
else:
    print("Sentence not found.")