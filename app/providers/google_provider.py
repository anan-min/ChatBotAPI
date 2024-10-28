import os
import asyncio
import aiofiles
from pathlib import Path
from pydub import AudioSegment
from google.cloud import texttospeech, speech_v1 as speech
from app.configs.google_config import api_credentials, voice_configs, audio_configs, transcribe_configs

class GoogleProvider:
    def __init__(self) -> None:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_credentials
        self.tts_client = texttospeech.TextToSpeechAsyncClient()  # Async client
        self.stt_client = speech.SpeechAsyncClient()  # Async client

    async def transcribe_audio_file(self, audio_file_path):
        standardized_audio_path = await self.convert_audio_sample_rate(audio_file_path)

        async with aiofiles.open(standardized_audio_path, "rb") as audio_file:
            audio_content = await audio_file.read()

        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(**transcribe_configs)

        response = await self.stt_client.recognize(config=config, audio=audio)

        transcribe_text = self.process_response(response)
        return transcribe_text

    def process_response(self, response):
        if not response.results:
            return ""
        transcribed_text = " ".join(result.alternatives[0].transcript for result in response.results)
        return transcribed_text

    async def speech_synthesis(self, text):
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(**voice_configs)
        audio_config = texttospeech.AudioConfig(**audio_configs)

        response = await self.tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        return response.audio_content

    async def convert_audio_sample_rate(self, input_file_path, target_sample_rate=16000):
        loop = asyncio.get_running_loop()

        def sync_convert_audio():
            input_file_str = str(input_file_path)
            if input_file_str.endswith('.mp3'):
                audio = AudioSegment.from_mp3(input_file_str)
            elif input_file_str.endswith('.wav'):
                audio = AudioSegment.from_wav(input_file_str)
            else:
                raise ValueError("Unsupported file format. Please use MP3 or WAV files.")

            audio = audio.set_frame_rate(target_sample_rate).set_channels(1)
            standardized_audio_path = input_file_str.replace('.wav', '_standardized.wav')
            audio.export(standardized_audio_path, format="wav")
            return standardized_audio_path

        standardized_audio_path = await loop.run_in_executor(None, sync_convert_audio)
        return standardized_audio_path

async def main():
    provider = GoogleProvider()
    AUDIO_FILE_PATH = Path(__file__).parent.parent / 'data' / 'test' / 'voice5.wav'
    SAVE_PATH = Path(__file__).parent.parent / 'data' / 'test' / 'test1.wav'

    # Transcribe audio file
    transcribed_text = await provider.transcribe_audio_file(AUDIO_FILE_PATH)
    print("Transcribed Text:", transcribed_text)

    # Synthesize speech
    if transcribed_text:
        audio_content = await provider.speech_synthesis(transcribed_text)
        async with aiofiles.open(SAVE_PATH, 'wb') as out_file:
            await out_file.write(audio_content)
        print(f"Synthesized speech saved to {SAVE_PATH}")

if __name__ == "__main__":
    asyncio.run(main())
