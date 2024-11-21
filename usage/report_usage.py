import os
import time
import csv
from pathlib import Path
from pythainlp import word_tokenize
import app.utils.files_handler as files_handler
from collections import Counter
from app.providers import OpenAIProvider
from app.providers import AmazonProvider
from app.providers.google_provider import GoogleProvider
from app.providers.ollama_provider import OllamaProvider
from app.providers.botnoi_provider import BotnoiProvider
import pandas as pd 
import asyncio



audio_dir_path = Path(__file__).parent.parent / 'app' / 'data' / 'sample'
report_dir_path = Path(__file__).parent.parent / 'app' / 'data' / 'report'
th_questions_path = report_dir_path / 'thai_questions_1k.csv'


df = pd.read_csv(th_questions_path)
questions_list = df['Question'].tolist()
print(f"number of questions: {len(questions_list)}")


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

async def generate_query_ollama_report(csv_filename):

    count = 0 

    csv_file_path = report_dir_path / f"{csv_filename}.csv"
    ollama_provider = OllamaProvider()

    model = "llama3.2"
    provider = "ollama-local"

    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Question Number", "Input Word Count",
                            "Output Word Count", "Time Taken (s)", "Provider","Model", "Question", "Answer"])
        for question in questions_list:
            if count >= 10:
                break
            start_time = time.time()
            answer = await ollama_provider.query_text_file(question)
            end_time = time.time()

            time_taken = end_time - start_time
            input_word_count = count_thai_words(question)
            output_word_count = count_thai_words(answer)

            print(f"Question: {question}")
            print(f"Answer: {answer}")
            print(f"Input word count: {input_word_count}")
            print(f"Output word count: {output_word_count}")
            print(f"Time taken: {time_taken} seconds")

            count  += 1

            csv_writer.writerow(
                [count, input_word_count, output_word_count, time_taken, provider, model, question, answer])


async def generate_query_openai_report(csv_filename):

    count = 0 

    csv_file_path = report_dir_path / f"{csv_filename}.csv"
    openai_provider = OpenAIProvider()

    model = "gpt-4o"
    provider = "openai"

    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Question Number", "Input Word Count",
                            "Output Word Count", "Time Taken (s)", "Provider","Model", "Question"])
        for question in questions_list:
            if count >= 10:
                break
            start_time = time.time()
            answer = await openai_provider.query_text_file(question, model)
            end_time = time.time()

            time_taken = end_time - start_time
            input_word_count = count_thai_words(question)
            output_word_count = count_thai_words(answer)

            print(f"Question: {question}")
            print(f"Answer: {answer}")
            print(f"Input word count: {input_word_count}")
            print(f"Output word count: {output_word_count}")
            print(f"Time taken: {time_taken} seconds")

            count  += 1

            csv_writer.writerow(
                [count, input_word_count, output_word_count, time_taken, provider, model, question])




async def generate_tts_openai_report(csv_filename):

    count = 0 

    csv_file_path = report_dir_path / f"{csv_filename}.csv"
    openai_provider = OpenAIProvider()

    model = "tts-1"
    provider = "openai"

    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Question Number", "Word Count",
                            "File size(Mb)", "Time Taken (s)", "Provider", "Model", "Text"])
        for text in questions_list:
            if count >= 10:
                break
            start_time = time.time()
            audio_content = await openai_provider.speech_synthesis(text)
            end_time = time.time()

            file_path = files_handler.save_audio_file(audio_content)
            file_size = os.path.getsize(file_path) / (1024 * 1024)
            files_handler.delete_file(file_path)

            time_taken = end_time - start_time
            word_count = count_thai_words(text)

            count += 1

            csv_writer.writerow(
                [count, word_count, file_size, time_taken, provider, model, text])



def generate_tts_google_report(csv_filename):

    count = 0 

    csv_file_path = report_dir_path / f"{csv_filename}.csv"
    google_provider = GoogleProvider()

    model = "tts-1"
    provider = "openai"

    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Question Number", "Word Count",
                            "File size(Mb)", "Time Taken (s)", "Provider", "Model", "Text"])
        for text in questions_list:
            if count >= 10:
                break
            start_time = time.time()
            audio_content = google_provider.speech_synthesis(text)
            end_time = time.time()

            file_path = files_handler.save_audio_file(audio_content)
            file_size = os.path.getsize(file_path) / (1024 * 1024)
            files_handler.delete_file(file_path)

            time_taken = end_time - start_time
            word_count = count_thai_words(text)

            count += 1

            csv_writer.writerow(
                [count, word_count, file_size, time_taken, provider, model, text])



async def generate_tts_botnoi_report(csv_filename):

    count = 0 

    csv_file_path = report_dir_path / f"{csv_filename}.csv"
    botnoi_provider = BotnoiProvider()

    model = "tts-1"
    provider = "openai"

    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Question Number", "Word Count",
                            "File size(Mb)", "Time Taken (s)", "Provider", "Model", "Text"])
        for text in questions_list:
            if count >= 10:
                break
            start_time = time.time()
            audio_content = await botnoi_provider.speech_synthesis(text)
            end_time = time.time()

            file_path = files_handler.save_audio_file(audio_content)
            file_size = os.path.getsize(file_path) / (1024 * 1024)
            files_handler.delete_file(file_path)

            time_taken = end_time - start_time
            word_count = count_thai_words(text)

            count += 1

            csv_writer.writerow(
                [count, word_count, file_size, time_taken, provider, model, text])


asyncio.run(generate_tts_botnoi_report('tts_botnoi_report'))