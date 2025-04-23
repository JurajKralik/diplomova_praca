import csv, json
from tkinter import filedialog
import os


def get_sentence_for_file(tsv_path, target_filename):
    with open(tsv_path, "r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile, delimiter="\t")

        for row in reader:
            if row["path"].strip() == target_filename:
                # Remove backslashes and double quotes from the sentence
                return (
                    row["sentence"]
                    .strip()
                    .lower()
                    .replace("\\", "")
                    .replace('"', "")
                    .replace(",", "")
                    .replace(".", "")
                )
    return None


def main():
    validated_tsv, result_json, output_json_path = get_file_paths()

    results = get_results(result_json)
    evaluation = []

    for result in results:
        evaluated = compare_result(validated_tsv, result)
        evaluation.append(evaluated)

    with open(output_json_path, "w", encoding="utf-8") as outfile:
        json.dump(evaluation, outfile, ensure_ascii=False, indent=4)

    print(f"Evaluation results saved to {output_json_path}")


def get_file_paths() -> tuple:
    validated_tsv = filedialog.askopenfile()
    if not validated_tsv:
        print("No input file selected.")
        exit()

    result_json = filedialog.askopenfile()
    if not result_json:
        print("No output file selected.")
        exit()

    output_folder = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_folder, exist_ok=True)

    result_json_name = os.path.basename(result_json.name)
    output_json_path = os.path.join(output_folder, f"evaluated_{result_json_name}")

    return validated_tsv, result_json, output_json_path


def get_results(result_json):
    with open(result_json.name, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    return data.get("results", [])


def compare_result(validated_tsv, result) -> dict:
	file_name = result.get("file_name", "")
	# Replace .wav with .mp3 to match the validated file format
	mp3_file_name = file_name.replace(".wav", ".mp3")
	sentence = get_sentence_for_file(validated_tsv.name, mp3_file_name)
	transcript = result.get("transcript", "")
    
	if transcript is None:
		matching = sentence == transcript
		print(f"Evaluating file: {file_name} - Transcription missing")
		return {
			"file_name": file_name,
			"sentence": sentence,
			"transcript": transcript,
			"match": matching,
		}
	else:
		transcript = transcript.strip().lower()
		matching = sentence == transcript
		print(f"Evaluating file: {file_name} - Match found: {matching}")

		return {
			"file_name": file_name,
			"sentence": sentence,
			"transcript": transcript,
			"match": matching,
		}


main()
