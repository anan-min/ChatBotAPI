import os 
import time
import csv
from pathlib import Path
from pythainlp import word_tokenize
from collections import Counter
from app.providers import GoogleProvider
from app.utils.convert_audio_sample_rate import convert_audio_sample_rate


reports_path = Path(__file__).parent.parent / 'app' / 'data' / 'report' 
sample_voices_path = Path(__file__).parent.parent / 'app' / 'data' / 'sample' 

def count_thai_words(text):
    tokens = word_tokenize(text, engine='newmm')
    word_count = Counter(tokens)
    return len(word_count)


def provider_performance_testing(provider, provider_name, model, max_files=100):
    csv_path = generate_stt_csv_file_path(provider_name)
    generate_csv(csv_path)

    count = 0 
    for filename in os.listdir(sample_voices_path):
        if count >= max_files:
            break
        
        file_path = sample_voices_path / filename

        converted_file_path = file_path.with_name(file_path.stem + '_16k.wav')
        convert_audio_sample_rate(file_path, converted_file_path)

        with open(converted_file_path, "rb") as audio_file:
            start_time = time.time()
            transcribed_data = provider.transcribe_audio_file(converted_file_path)
            end_time = time.time()
            time_taken = end_time - start_time
            file_size = os.path.getsize(file_path)
            word_count = count_thai_words(transcribed_data)
            print(f"File {count} {filename} took {time_taken} seconds to transcribe and {word_count} words were transcribed.")

        write_csv(csv_path, filename, provider_name, model, time_taken, file_size, word_count, transcribed_data)
        
        if os.path.exists(converted_file_path):
            os.remove(converted_file_path)
        
        count += 1

def generate_stt_csv_file_path(provider_name):
    csv_name = f"{provider_name}_stt.csv"
    csv_path = Path(__file__).parent.parent / 'app' / 'data' / 'report' / csv_name
    return csv_path 

def generate_csv(csv_path):
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Filename', 'Provider', 'Model', 'Time Taken (s)', 'File size', 'Word Count' ,'Transcribed Text'])

def write_csv(csv_path, filename, provider, model, time_taken, file_size, word_count, transcribed_text):
    with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([filename, provider, model, time_taken, file_size, word_count, transcribed_text])

if __name__ == '__main__':
    api_credentials = 'app/api/google/demo.json'
    provider = GoogleProvider(api_credentials)
    provider_performance_testing(provider, 'google', 'google', 100)