import os
import asyncio
import aiofiles
from pydub import AudioSegment
from google.cloud import texttospeech, speech_v1 as speech
from google.cloud import language_v1
from app.configs.google_config import api_credentials, voice_configs, audio_configs, transcribe_configs

class GoogleProvider:
    def __init__(self) -> None:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_credentials
        self.tts_client = texttospeech.TextToSpeechAsyncClient()  # Async client
        self.stt_client = speech.SpeechAsyncClient()  # Async client
        self.language_client = language_v1.LanguageServiceClient()

    async def transcribe_audio_file(self, audio_file_path, transcribe_configs=transcribe_configs):
        # Convert and standardize audio
        standardized_audio_path = self.convert_audio_sample_rate(audio_file_path)

        # Load audio content asynchronously
        async with aiofiles.open(standardized_audio_path, "rb") as audio_file:
            audio_content = await audio_file.read()

        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(**transcribe_configs)

        # Make async request to transcribe the audio
        response = await self.stt_client.recognize(config=config, audio=audio)

        # Process and return the transcribed text
        transcribe_text = self.process_response(response)
        return transcribe_text

    def process_response(self, response):
        if not response.results:
            return ""  # Return empty string if no results
        transcribed_text = " ".join(result.alternatives[0].transcript for result in response.results)
        return transcribed_text

    async def speech_synthesis(self, text, tts_audio_configs=audio_configs, tts_voice_configs=voice_configs):
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(**tts_voice_configs)
        audio_config = texttospeech.AudioConfig(**tts_audio_configs)

        # Make async request to synthesize speech
        response = await self.tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

        # Return audio content for further processing
        return response.audio_content

    def convert_audio_sample_rate(self, input_file_path, target_sample_rate=16000):
        input_file_path = str(input_file_path)
        # Convert audio sample rate (synchronous, as pydub doesn't support async)
        if input_file_path.endswith('.mp3'):
            audio = AudioSegment.from_mp3(input_file_path)
        elif input_file_path.endswith('.wav'):
            audio = AudioSegment.from_wav(input_file_path)
        else:
            raise ValueError("Unsupported file format. Please use MP3 or WAV files.")

        # Set the target sample rate and channels
        audio = audio.set_frame_rate(target_sample_rate).set_channels(1)

        # Overwrite the input file with the standardized audio
        audio.export(input_file_path, format="wav")
        
        return input_file_path
