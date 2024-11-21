import os
import time
import csv
from pathlib import Path
from pythainlp import word_tokenize
from collections import Counter
from app.providers import OpenAIProvider
from app.providers import AmazonProvider
from app.providers.google_provider import GoogleProvider
from app.providers.ollama_provider import OllamaProvider
import pandas as pd 
import asyncio


audio_dir_path = Path(__file__).parent.parent / 'app' / 'data' / 'sample'
report_dir_path = Path(__file__).parent.parent / 'app' / 'data' / 'report'
th_questions_path = report_dir_path / 'thai_questions_1k.csv'


df = pd.read_csv(th_questions_path)
questions_list = df['Question'].tolist()
print(questions_list)


def count_thai_words(text):
    tokens = word_tokenize(text, engine='newmm')
    word_count = Counter(tokens)
    return len(word_count)


async def generate_stt_openai_report(csv_file_name):
    max_count = 10
    count = 0
    openai_provider = OpenAIProvider()

    csv_file_path = report_dir_path / f"{csv_file_name}.csv"

    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["File Number", "File Name",
                            "File Size (bytes)", "Time Taken (s)", "Word Count", "Transcribed Text"])

        for filename in os.listdir(audio_dir_path):
            if count > max_count:
                break
            file_path = audio_dir_path / filename
            file_size = os.path.getsize(file_path)
            start_time = time.time()
            transcribed_data = await openai_provider.transcribe_audio_file(file_path)
            end_time = time.time()
            time_taken = end_time - start_time
            word_count = count_thai_words(transcribed_data)

            print(f"File {count} file size: {file_size} bytes  {filename} {file_size} bytes took {time_taken} seconds to transcribe and {
                word_count} words were transcribed.")
            count += 1

            csv_writer.writerow(
                [count, filename, file_size, time_taken, word_count, transcribed_data])


async def generate_stt_amazon_report(csv_filename):
    max_count = 10
    count = 0
    amazon_provider = AmazonProvider('speech-to-text-storage')

    csv_file_path = report_dir_path / f"{csv_filename}.csv"

    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["File Number", "File Name",
                            "File Size (bytes)", "Time Taken (s)", "Word Count", "Transcribed Text"])

        for filename in os.listdir(audio_dir_path):
            if count > max_count:
                break
            file_path = audio_dir_path / filename
            file_size = os.path.getsize(file_path)
            start_time = time.time()
            transcribed_data = await amazon_provider.transcribe_audio_file(file_path)
            end_time = time.time()
            time_taken = end_time - start_time
            word_count = count_thai_words(transcribed_data)

            print(f"File {count} file size: {file_size} bytes  {filename} {file_size} bytes took {time_taken} seconds to transcribe and {
                word_count} words were transcribed. transcribed text {transcribed_data}")
            count += 1

            csv_writer.writerow(
                [count, filename, file_size, time_taken, word_count, transcribed_data])


def generate_stt_google_report(csv_filename):
    max_count = 10
    count = 0
    google_provider = GoogleProvider()

    csv_file_path = report_dir_path / f"{csv_filename}.csv"

    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["File Number", "File Name",
                            "File Size (bytes)", "Time Taken (s)", "Word Count", "Transcribed Text"])

        for filename in os.listdir(audio_dir_path):
            if count > max_count:
                break
            file_path = audio_dir_path / filename
            file_size = os.path.getsize(file_path)
            start_time = time.time()
            transcribed_data = google_provider.transcribe_audio_file(file_path)
            end_time = time.time()
            time_taken = end_time - start_time
            word_count = count_thai_words(transcribed_data)

            print(f"File {count} file size: {file_size} bytes  {filename} {file_size} bytes took {time_taken} seconds to transcribe and {
                word_count} words were transcribed. transcribed text {transcribed_data}")
            count += 1

            csv_writer.writerow(
                [count, filename, file_size, time_taken, word_count, transcribed_data])

def generate_stt_ollama_report(csv_filename):
    pass 
