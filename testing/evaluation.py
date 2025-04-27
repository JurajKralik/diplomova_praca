import csv, json, os, re
from tkinter import filedialog
from word2number import w2n


SUBSTITUTIONS = {
	"&": "and",
	"@": "at",
	"#": "number",
	"$": "dollar",
	"%": "percent",
	"€": "euro",
	"£": "pound",
	"¢": "cent",
}

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

def get_additional_info_for_file(tsv_path, target_filename):
	with open(tsv_path, "r", encoding="utf-8") as infile:
		reader = csv.DictReader(infile, delimiter="\t")

		for row in reader:
			if row["path"].strip() == target_filename:
				return {
					"age": row.get("age", "").strip(),
					"gender": row.get("gender", "").strip(),
					"accents": row.get("accents", "").strip(),
				}
	return {"age": None, "gender": None, "accents": None}

def get_file_paths() -> tuple:
	print("Please select the validated TSV file:")
	validated_tsv = filedialog.askopenfile()
	if not validated_tsv:
		print("No input file selected.")
		exit()

	print("Please select the result JSON file:")
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
		print(f"Evaluating file: {file_name} - Transcription missing")
		return {
			"file_name": file_name,
			"sentence": sentence,
			"transcript": transcript,
			"match": 0.0,
		}
	else:
		transcript_words = normalize_text(transcript)
		sentence_words = normalize_text(sentence) if sentence else []
		matching = sum(
			min(transcript_words.count(word), sentence_words.count(word))
			for word in set(transcript_words)
		) / max(len(sentence_words), 1)
		print(f"Evaluating file: {file_name} - Match score: {matching:.2f}")

		return {
			"file_name": file_name,
			"sentence": sentence,
			"transcript": transcript,
			"match": matching,
		}
     
def normalize_text(text):
	# Replace symbols with words
	for symbol, word in SUBSTITUTIONS.items():
		text = text.replace(symbol, f" {word} ")

	# Remove punctuation (optional, depends on your use case)
	text = re.sub(r"[^\w\s]", "", text)

	# Lowercase and split
	words = text.lower().strip().split()

	# Try converting word-numbers to digits
	normalized = []
	for word in words:
		try:
			num = w2n.word_to_num(word)
			normalized.append(str(num))
		except ValueError:
			normalized.append(word)

	return normalized


if __name__ == "__main__":
	validated_tsv, result_json, output_json_path = get_file_paths()

	results = get_results(result_json)
	evaluation = []

	for result in results:
		evaluated = compare_result(validated_tsv, result)
		evaluation.append(evaluated)
		mp3_file_name = result["file_name"].replace(".wav", ".mp3")
		additional_info = get_additional_info_for_file(validated_tsv.name, mp3_file_name)
		evaluated.update(additional_info)

	average_match = sum(item["match"] for item in evaluation if "match" in item) / len(evaluation) if evaluation else 0.0
	evaluation.append({"average_match": average_match})
	with open(output_json_path, "w", encoding="utf-8") as outfile:
		json.dump(evaluation, outfile, ensure_ascii=False, indent=4)

	print(f"Evaluation results saved to {output_json_path}")