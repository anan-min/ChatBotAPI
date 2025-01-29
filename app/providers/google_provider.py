import os
import asyncio
from pathlib import Path
from google.cloud import texttospeech, speech_v1 as speech
from google.cloud import language_v1
from app.configs.google_config import api_credentials, voice_configs, audio_configs, transcribe_configs
import soundfile as sf  
import librosa
import audioread
import numpy as np
import scipy

class GoogleProvider:
    def __init__(self) -> None:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_credentials
        self.tts_client = texttospeech.TextToSpeechClient()
        self.stt_client = speech.SpeechClient()
        self.language_client = language_v1.LanguageServiceClient()

    # Making transcribe_audio_file async
    async def transcribe_audio_file(self, audio_file_path, transcribe_configs=transcribe_configs):
        # Convert audio sample rate if needed (make sure this is non-blocking too)
        convert_audio_file_path = await asyncio.to_thread(self.convert_audio_sample_rate, audio_file_path)

        # Read audio content from the converted audio file
        with open(convert_audio_file_path, "rb") as audio_file:
            audio_content = audio_file.read()
        
        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(**transcribe_configs)

        # Request transcription and process the response
        response = await asyncio.to_thread(self.stt_client.recognize, config=config, audio=audio)
        
        # Process the transcription result
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

        # Call the API to generate the speech
        response = await asyncio.to_thread(self.tts_client.synthesize_speech, input=synthesis_input, voice=voice, audio_config=audio_config)
    
        # Return the generated audio content
        return response.audio_content

    # def convert_audio_sample_rate(self, input_file_path, target_sample_rate=16000):
    #     # Load the audio file with librosa
    #     audio_data, original_sample_rate = librosa.load(input_file_path, sr=None)
        
    #     # Resample the audio to the target sample rate
    #     audio_resampled = librosa.resample(audio_data, orig_sr=original_sample_rate, target_sr=target_sample_rate)

    #     # Save the resampled audio as a WAV file
    #     output_file_path = os.path.splitext(input_file_path)[0] + ".wav"
    #     sf.write(output_file_path, audio_resampled, target_sample_rate)
    #     return output_file_path


    def convert_audio_sample_rate(self, input_file_path, target_sample_rate=16000):
        # Open the audio file with audioread
        with audioread.audio_open(input_file_path) as f:
            original_sample_rate = f.samplerate  # Get the sample rate from audioread
            # Read the audio data from the file (concatenate chunks into bytes)
            audio_data = b''.join([chunk for chunk in f])

        # Convert the audio data into a numpy array with the appropriate dtype
        audio_data = np.frombuffer(audio_data, dtype=np.int16)

        # Resample the audio to the target sample rate
        num_samples = int(len(audio_data) * target_sample_rate / original_sample_rate)
        audio_resampled = scipy.signal.resample(audio_data, num_samples).astype(np.int16)

        # Save the resampled audio as a WAV file
        output_file_path = os.path.splitext(input_file_path)[0] + ".wav"
        sf.write(output_file_path, audio_resampled, target_sample_rate)
        
        return output_file_path


