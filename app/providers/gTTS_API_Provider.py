import os
import csv
import time
from collections import Counter
from google.cloud import texttospeech, speech_v1 as speech
from pythainlp import word_tokenize
from pydub import AudioSegment

class GoogleTTSProvider:
    def __init__(self, api_credentials: str) -> None:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_credentials
        self.tts_client = texttospeech.TextToSpeechClient()
        self.stt_client = speech.SpeechClient()

    def synthesize_speech(self, text: str, language_code: str = "th-TH", gender: str = "NEUTRAL", speaking_rate: float = 1.0, pitch: float = 1.0, model: str = "standard") -> bytes:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=getattr(texttospeech.SsmlVoiceGender, gender.upper())
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speaking_rate,
            pitch=pitch,
            effects_profile_id=[model] 
        )

        start_time = time.time()
        response = self.tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        end_time = time.time()
        time_taken = end_time - start_time

        return response.audio_content, time_taken

    def transcribe_audio(self, audio_file_path: str, model: str = "default") -> str:
        with open(audio_file_path, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="th-TH",
            model=model 
        )

        start_time = time.time()
        response = self.stt_client.recognize(config=config, audio=audio)
        end_time = time.time()
        time_taken = end_time - start_time

        transcribed_text = " ".join(result.alternatives[0].transcript for result in response.results)
        return transcribed_text, time_taken
            

    def synthesize_speech(self, text: str, language_code: str = "th-TH", gender: str = "NEUTRAL", speaking_rate: float = 1.0, pitch: float = 1.0) -> bytes:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=getattr(texttospeech.SsmlVoiceGender, gender.upper())
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speaking_rate,
            pitch=pitch
        )

        start_time = time.time()
        response = self.tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        end_time = time.time()
        time_taken = end_time - start_time

        return response.audio_content, time_taken

    def save_audio(self, audio_content: bytes, output_path: str) -> None:
        os.makedirs(os.path.dirname(output_path), exist_ok=True) 
        with open(output_path, "wb") as out:
            out.write(audio_content)
            print(f"Audio content written to file: '{output_path}'")

    def generate_report(self, report_path: str, filename: str, provider: str, model: str, time_taken: float, file_size: int, word_count: int, transcribed_text: str) -> None:
        fieldnames = ['Filename', 'Provider', 'Model', 'Time Taken (s)', 'File size', 'Word Count', 'Transcribed Text']
        
        os.makedirs(os.path.dirname(report_path), exist_ok=True)

        with open(report_path, mode='a', newline='', encoding='utf-8') as report_file:
            writer = csv.DictWriter(report_file, fieldnames=fieldnames)
            if report_file.tell() == 0: 
                writer.writeheader()
            writer.writerow({
                'Filename': filename,
                'Provider': provider,
                'Model': model,
                'Time Taken (s)': time_taken,
                'File size': file_size,
                'Word Count': word_count,
                'Transcribed Text': transcribed_text
            })
            print(f"Report written to file: '{report_path}'")

    def transcribe_audio(self, audio_file_path: str) -> str:
        with open(audio_file_path, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="th-TH"
        )

        start_time = time.time()
        response = self.stt_client.recognize(config=config, audio=audio)
        end_time = time.time()
        time_taken = end_time - start_time

        transcribed_text = " ".join(result.alternatives[0].transcript for result in response.results)
        return transcribed_text, time_taken

def get_unique_audio_filename(base_path: str, extension: str) -> str:
    index = 1
    while True:
        filename = f"{base_path}_{index}{extension}"
        if not os.path.exists(filename):
            return filename
        index += 1

def count_thai_words(text):
    tokens = word_tokenize(text, engine='newmm')
    word_count = Counter(tokens)
    return len(word_count)

def convert_audio_sample_rate(input_file: str, output_file: str, target_sample_rate: int = 16000) -> None:
    audio = AudioSegment.from_wav(input_file)
    audio = audio.set_frame_rate(target_sample_rate)
    audio = audio.set_channels(1)
    audio.export(output_file, format="wav")

def process_stt(tts_provider, audio_input_file, report_file):
    audio_base_path = "app/data/convert16k/voice_16k"
    audio_extension = ".wav"

    converted_audio_file = get_unique_audio_filename(audio_base_path, audio_extension)
    
    convert_audio_sample_rate(audio_input_file, converted_audio_file)

    file_size = os.path.getsize(converted_audio_file)

    transcribed_text, stt_time_taken = tts_provider.transcribe_audio(converted_audio_file)
    word_count = count_thai_words(transcribed_text)

    tts_provider.generate_report(report_file, os.path.basename(converted_audio_file), 'google', 'speech-to-text', stt_time_taken, file_size, word_count, transcribed_text)
    
    return transcribed_text, word_count

def process_tts(tts_provider, transcribed_text, report_file):
    audio_base_path = "app/data/voice/speech"
    audio_extension = ".mp3"
    output_file = get_unique_audio_filename(audio_base_path, audio_extension)

    audio_content, tts_time_taken = tts_provider.synthesize_speech(transcribed_text)
    tts_provider.save_audio(audio_content, output_file)

    filename = os.path.basename(output_file)
    provider = "google"
    model = "text-to-speech"
    file_size = os.path.getsize(output_file)

    tts_provider.generate_report(report_file, filename, provider, model, tts_time_taken, file_size, word_count, transcribed_text)


if __name__ == "__main__":
    api_credentials = 'API/Google/demo.json'
    tts_provider = GoogleTTSProvider(api_credentials)

    audio_input_file = 'app/data/test/voice5.wav'
    report_file = "app/data/report/gttsAPI_report.csv"

    transcribed_text, word_count = process_stt(tts_provider, audio_input_file, report_file)

    process_tts(tts_provider, transcribed_text, report_file)
