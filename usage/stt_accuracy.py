import os
import pandas as pd
import asyncio
from difflib import SequenceMatcher
from app.providers.amazon_provider import AmazonProvider  


AUDIO_FOLDER = "app/data/botnoi_test"
CSV_REPORT_PATH = "app/data/report/botnoi_tts.csv"
RESULTS_CSV_PATH = "app/data/report/transcription_results.csv"  
BUCKET_NAME = "speech-to-text-storage"  


def load_expected_transcripts(csv_path):
    try:
        df = pd.read_csv(csv_path)
        return df[['Filename', 'Text']]
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_path}")
        return None

def find_mismatched_words(actual, expected):
    actual_words = actual.split()
    expected_words = expected.split()

    matcher = SequenceMatcher(None, actual_words, expected_words)
    mismatches = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag != 'equal':  # ส่วนที่ไม่ตรงกัน
            mismatches.extend(actual_words[i1:i2])

    return mismatches

def calculate_levenshtein_distance(actual, expected):
    matcher = SequenceMatcher(None, actual, expected)
    return 1 - matcher.ratio()


def save_results_to_csv(results, output_path):
    df = pd.DataFrame(results, columns=[
        "Provider", "Model","Filename", "Transcript Text", "Expected Text", "Result", 
        "Number of Mismatched Words", "Mismatched Words", 
        "Levenshtein Distance"
    ])
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Results saved to {output_path}")

async def main():
    num_iterations = 100  

    df = load_expected_transcripts(CSV_REPORT_PATH)
    if df is None:
        return

    amazon_provider = AmazonProvider(BUCKET_NAME)

    results = []

    for index, row in df.iterrows():
        if index >= num_iterations:
            break

        filename = row['Filename']
        expected_text = row['Text']
        audio_path = os.path.join(AUDIO_FOLDER, filename)

        print(f"Processing file: {filename}")

        try:
            actual_text = await amazon_provider.transcribe_audio_file(audio_path)

            if actual_text:
                mismatches = find_mismatched_words(actual_text, expected_text)
                num_mismatches = len(mismatches)
                distance = calculate_levenshtein_distance(actual_text, expected_text)
                status = "Correct" if num_mismatches == 0 else "Incorrect"

                print(f"Result: {status}")
                print(f"Number of mismatched words: {num_mismatches}")
                print(f"Mismatched words: {mismatches}")
                print(f"Levenshtein Distance: {distance:.2f}")

                
                results.append((
                    "amazon", "transcribe",filename, actual_text, expected_text, 
                    status, num_mismatches, mismatches, distance
                    
                ))
            else:
                print(f"Failed to transcribe {filename}")
                results.append((
                    "amazon", "transcribe",filename, None, expected_text, "Failed", 
                    0, [], 1.0
                ))
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            results.append((
                "amazon", "transcribe",filename, None, expected_text, f"Error: {e}", 
                0, [], 1.0
            ))

    print("\nSummary of Transcription Results:")
    for result in results:
        print(f"Filename: {result[0]}, Status: {result[3]}, Mismatches: {result[4]}, Levenshtein: {result[6]:.2f}")

    save_results_to_csv(results, RESULTS_CSV_PATH)

if __name__ == "__main__":
    asyncio.run(main())
