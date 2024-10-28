import os
from pydub import AudioSegment
from google.cloud import texttospeech, speech_v1 as speech
from google.cloud import language_v1
from app.configs.google_config import api_credentials, voice_configs, audio_configs, transcribe_configs
import aiofiles  # For async file operations
import asyncio   # For event loop management

class GoogleProvider:
    def __init__(self) -> None:

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_credentials
        self.tts_client = texttospeech.TextToSpeechClient()
        self.stt_client = speech.SpeechClient()
        self.language_client = language_v1.LanguageServiceClient()

    async def transcribe_audio_file(self, audio_file_path, transcribe_configs=transcribe_configs):
        print("01: start transcribe audio file")
        # Convert wav or mp3 audio to standard config and overwrite the original file
        standardized_audio_path = await self.convert_audio_sample_rate(audio_file_path)

        # Load audio content from the file asynchronously
        async with aiofiles.open(standardized_audio_path, "rb") as audio_file:
            audio_content = await audio_file.read()

        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(**transcribe_configs)

        # Request transcribe text with config and audio asynchronously
        print("05: start request transcribe text")
        loop = asyncio.get_event_loop()
        try:
            response = await loop.run_in_executor(None, self.stt_client.recognize, config=config, audio=audio)
        except Exception as e:
            print(f"An error occurred: {e}")


        print(f"06: request transcribe text response: {response}")
        # Process text from response and return it
        transcribe_text = self.process_response(response)
        return transcribe_text
        
    # Generate text from Google API transcribe response 
    def process_response(self, response):
        if not response.results:
            return ""  # Return empty string if no results
        transcribed_text = " ".join(result.alternatives[0].transcript for result in response.results)
        return transcribed_text

    # Speech synthesis method
    def speech_synthesis(self, text, tts_audio_configs=audio_configs, tts_voice_configs=voice_configs):
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(**tts_voice_configs)
        audio_config = texttospeech.AudioConfig(**tts_audio_configs)

        # Call the API with the prepared objects
        response = self.tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    
    # Return the audio content for further processing
        return response.audio_content

    # Convert audio sample rate method
    async def convert_audio_sample_rate(self, input_file_path, target_sample_rate=16000):
        print("02: start convert audio sample rate")
        input_file_path = str(input_file_path)
        
        # Use run_in_executor to handle blocking I/O in a separate thread
        loop = asyncio.get_event_loop()
        
        # Load the audio file and convert it
        audio = await loop.run_in_executor(None, self._load_audio, input_file_path)
        
        # Set the target sample rate and channels
        audio = audio.set_frame_rate(target_sample_rate).set_channels(1)
        
        # Export the audio back to the same path (overwrite)
        output_file = input_file_path  # Overwrite the input file
        await loop.run_in_executor(None, self._export_audio, audio, output_file)
        
        print("Audio sample rate converted.")
        return output_file

    def _load_audio(self, input_file_path):
        print("03: start load audio")
        # Determine file type and load the audio
        if input_file_path.endswith('.mp3'):
            return AudioSegment.from_mp3(input_file_path)
        elif input_file_path.endswith('.wav'):
            return AudioSegment.from_wav(input_file_path)
        else:
            raise ValueError("Unsupported file format. Please use MP3 or WAV files.")

    def _export_audio(self, audio, output_file):
        print("04: start export audio")
        # Export the audio to the specified file
        audio.export(output_file, format="wav")