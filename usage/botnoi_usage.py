import os
import time
import csv
from pathlib import Path
from pythainlp import word_tokenize
from collections import Counter
import pandas as pd
import sys
import asyncio  # Import asyncio

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir.parent))
from app.providers import BotnoiProvider

reports_path = Path(__file__).parent.parent / 'app' / 'data' / 'report'
dataset_path = Path(__file__).parent.parent / 'app' / 'data' / 'dataset' / 'dataset03_THver.csv'

def load_texts_from_csv(file_path, max_text):
    df = pd.read_csv(file_path)
    texts = df['Customer Comment'].dropna().tolist()[:max_text]
    return texts

def write_to_csv(csv_path, rows):
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Text', 'Provider', 'Model', 'Time Taken (s)', 'Filename'])
        writer.writerows(rows)

async def provider_performance_testing(provider, provider_name, model, max_text=1):
    csv_path = generate_tts_csv_file_path(provider_name)
    results = []

    texts = load_texts_from_csv(dataset_path, max_text)

    for idx, text in enumerate(texts):

        start_time = time.time()
        audio_url = await provider.speech_synthesis(text)  # ใช้ await ในการเรียก coroutine
        end_time = time.time()

        time_taken = end_time - start_time

        if audio_url:
            filename = f"botnoi_tts_{idx + 1}.wav"

            await provider.download_audio_file(audio_url, filename)  # ใช้ await ในการเรียก coroutine

            results.append([text, provider_name, model, time_taken, filename])
        else:
            print(f"Error processing text: {text}")

    write_to_csv(csv_path, results)
    print(f"ผลลัพธ์ถูกบันทึกใน: {csv_path}")

def generate_tts_csv_file_path(provider_name):
    csv_name = f"{provider_name}_tts.csv"
    csv_path = Path(__file__).parent.parent / 'app' / 'data' / 'report' / csv_name
    return csv_path

if __name__ == '__main__':
    provider = BotnoiProvider()
    asyncio.run(provider_performance_testing(provider, 'botnoi', 'voice', 1))  # ใช้ asyncio.run เพื่อรัน asynchronous function
