import os
from pathlib import Path
from google.cloud import texttospeech, speech_v1 as speech
from google.cloud import language_v1
from app.configs.google_config import api_credentials, voice_configs, audio_configs, transcribe_configs
import soundfile as sf  
import audioread
import scipy.signal 

class GoogleProvider:
    def __init__(self) -> None:

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_credentials
        self.tts_client = texttospeech.TextToSpeechClient()
        self.stt_client = speech.SpeechClient()
        self.language_client = language_v1.LanguageServiceClient()

    def transcribe_audio_file(self, audio_file_path, transcribe_configs=transcribe_configs):
        # Convert wav or mp3 audio to standard config and overwrite the original file
        standardized_audio_path = self.convert_audio_sample_rate_2(audio_file_path)

        # Load audio content from the file
        with open(standardized_audio_path, "rb") as audio_file:
            audio_content = audio_file.read()
        
        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(**transcribe_configs)

        # Request transcribe text with config and audio
        response = self.stt_client.recognize(config=config, audio=audio)

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
    

    def generate_audio_output_file_path(input_file_path, output_file_path):
        input_file_path = Path(input_file_path)
            
        temp_folder = input_file_path.parent / "temp"
        temp_folder.mkdir(exist_ok=True)

        if output_file_path is None:
            output_file_path = temp_folder /  input_file_path.with_suffix('.wav').name

        return str(output_file_path)
    

    def convert_audio_sample_rate(self, input_file_path, target_sample_rate=16000):
        output_file_path = self.generate_audio_output_file_path(input_file_path)

        data, original_sameple_rate = sf.read(input_file_path)

        if input_file_path.suffix != ".wav":
            input_file_path = self.convert_to_wav(input_file_path)

        if original_sameple_rate != target_sample_rate:
            num_samples = int(len(data) * target_sample_rate / original_sameple_rate)
            data = scipy.signal.resample(data, num_samples).astype(data.dtype)

            sf.write(output_file_path, data, target_sample_rate, format='WAV')

        return str(output_file_path)
    
    def convert_to_wav(self, input_file_path):

        output_file_path = input_file_path.with_suffix('.wav').name

        with audioread.audio_open(input_file_path) as input_file:
            data = b"".join(input_file.read_data() for _ in input_file)
            sample_rate = input_file.samplerate

        sf.write(output_file_path, sf.read(data, dtype='int16')[0], sample_rate, format='WAV', subtype='PCM_16')
        
        return output_file_path
            