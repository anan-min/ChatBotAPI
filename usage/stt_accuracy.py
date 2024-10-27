import os
import pandas as pd
import asyncio
from difflib import SequenceMatcher
from app.providers.amazon_provider import AmazonProvider  
from app.providers.google_provider import GoogleProvider
from app.providers.openai_provider import OpenAIProvider


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


def is_similar_word(word1, word2):
    """ตรวจสอบว่าคำสองคำมีความคล้ายคลึงกันหรือไม่ เช่น การสะกดที่ต่างกันเล็กน้อย หรือคำทับศัพท์ที่ออกเสียงเหมือนกัน"""
    # ปรับให้แยกสระ-วรรณยุกต์ที่ต่างกันออก
    if word1 == word2:
        return True
    elif SequenceMatcher(None, word1, word2).ratio() > 0.85:  # ปรับค่า similarity ตามต้องการ
        return True
    return False


def find_mismatched_words(actual, expected):
    actual_words = actual.split()
    expected_words = expected.split()

    mismatches = []
    for i, (a_word, e_word) in enumerate(zip(actual_words, expected_words)):
        if not is_similar_word(a_word, e_word):
            mismatches.append(a_word)

    # กรณีที่มีจำนวนคำในประโยคไม่ตรงกัน
    if len(actual_words) != len(expected_words):
        extra_words = actual_words[len(expected_words):] if len(actual_words) > len(expected_words) else expected_words[len(actual_words):]
        mismatches.extend(extra_words)

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
    num_iterations = 100  # ปรับตรงนี้

    df = load_expected_transcripts(CSV_REPORT_PATH)
    if df is None:
        return

    provider = OpenAIProvider()

    results = []

    for index, row in df.iterrows():
        if index >= num_iterations:
            break

        filename = row['Filename']
        expected_text = row['Text']
        audio_path = os.path.join(AUDIO_FOLDER, filename)

        print(f"Processing file: {filename}")

        try:
            actual_text = await provider.transcribe_audio_file(audio_path)


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
                    "Openai", "Whisper", filename, actual_text, expected_text, 
                    status, num_mismatches, mismatches, distance
                ))
            else:
                print(f"Failed to transcribe {filename}")
                results.append((
                    "Openai", "Whisper", filename, None, expected_text, "Failed", 
                    0, [], 1.0
                ))
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            results.append((
                "Openai", "Whisper", filename, None, expected_text, f"Error: {e}", 
                0, [], 1.0
            ))

    print("\nSummary of Transcription Results:")
    for result in results:
        print(f"Filename: {result[2]}, Status: {result[5]}, Mismatches: {result[7]}, Levenshtein: {result[8]:.2f}")

    save_results_to_csv(results, RESULTS_CSV_PATH)

if __name__ == "__main__":
    asyncio.run(main())
