import os 
import time
import csv
from pathlib import Path
from pythainlp import word_tokenize
from collections import Counter
import sys
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir.parent))
from app.providers import AmazonProvider


reports_path = Path(__file__).parent.parent / 'app' / 'data' / 'report' 
sample_voices_path = Path(__file__).parent.parent / 'app' / 'data' / 'sample' 

def count_thai_words(text):
    tokens = word_tokenize(text, engine='newmm')
    word_count = Counter(tokens)
    return len(word_count)


def provider_performance_testing(provider, provider_name, model, max_files=1): 
    csv_path = generate_stt_csv_file_path(provider_name)
    generate_csv(csv_path)

    count = 0 
    for filename in os.listdir(sample_voices_path):
        if count >= max_files:  
            break

        file_path = sample_voices_path / filename
        with open(file_path, "rb") as audio_file:
            job_uri = provider.store_audio_as_uri(file_path)  
            
            if job_uri:
                start_time = time.time()
                transcribed_data = provider.transcribe_audio_file(job_uri) 
                end_time = time.time()
                time_taken = end_time - start_time
                file_size = os.path.getsize(file_path)
                word_count = count_thai_words(transcribed_data)

                print(f"File {count} {filename} took {time_taken} seconds to transcribe and {word_count} words were transcribed.")

                write_csv(csv_path, filename, provider_name, model, time_taken, file_size, word_count, transcribed_data)
                count += 1
            else:
                print(f"Error uploading {filename} to S3.")





#generate

def generate_stt_csv_file_path(provider_name):
    csv_name = f"{provider_name}1_stt.csv"
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
    bucket_name = "speech-to-text-storage"
    provider = AmazonProvider(bucket_name)
    provider_performance_testing(provider, 'amazon', 'transcribe', 1) 