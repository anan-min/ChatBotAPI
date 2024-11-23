import os
from pydub import AudioSegment
from google.cloud import texttospeech, speech_v1 as speech
from google.cloud import language_v1
from app.configs.google_config import api_credentials, voice_configs, audio_configs, transcribe_configs
import app.utils.files_handler as files_handler
import logging
from pydub import AudioSegment
import os
import mimetypes



class GoogleProvider:
    def __init__(self) -> None:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_credentials
        self.tts_client = texttospeech.TextToSpeechClient()
        self.stt_client = speech.SpeechClient()
        self.language_client = language_v1.LanguageServiceClient()

    # def transcribe_audio_file(self, audio_file_path, transcribe_configs=transcribe_configs):
    #     # Convert wav or mp3 audio to standard config and overwrite the original file
    #     standardized_audio_path = self.convert_audio_sample_rate(audio_file_path)

    #     # Load audio content from the file
    #     with open(standardized_audio_path, "rb") as audio_file:
    #         audio_content = audio_file.read()
        
    #     audio = speech.RecognitionAudio(content=audio_content)
    #     config = speech.RecognitionConfig(**transcribe_configs)

    #     # Request transcribe text with config and audio
    #     response = self.stt_client.recognize(config=config, audio=audio)
    #     # Process text from response and return it
    #     transcribe_text = self.process_response(response)
    #     files_handler.delete_file(standardized_audio_path)
    #     return transcribe_text

    def transcribe_audio_file(self, audio_file_path, transcribe_configs=transcribe_configs):
        try:
            logging.debug(f"Starting transcription for file: {audio_file_path}")
            
            # Convert wav or mp3 audio to standard config and overwrite the original file
            try:
                standardized_audio_path = self.convert_audio_sample_rate(audio_file_path)
                logging.debug(f"Audio file standardized: {standardized_audio_path}")
            except Exception as e:
                logging.error(f"Error during audio standardization: {e}")
                raise ValueError(f"Failed to standardize audio file: {audio_file_path}") from e

            # Load audio content from the file
            try:
                with open(standardized_audio_path, "rb") as audio_file:
                    audio_content = audio_file.read()
                logging.debug("Audio content successfully loaded.")
            except FileNotFoundError as e:
                logging.error(f"Audio file not found: {standardized_audio_path}")
                raise e
            except Exception as e:
                logging.error(f"Error reading audio file: {e}")
                raise e

            # Create recognition audio object
            try:
                audio = speech.RecognitionAudio(content=audio_content)
                config = speech.RecognitionConfig(**transcribe_configs)
                logging.debug("Recognition audio and config objects created.")
            except Exception as e:
                logging.error(f"Error creating recognition objects: {e}")
                raise e

            # Request transcription
            try:
                response = self.stt_client.recognize(config=config, audio=audio)
                logging.debug("STT client recognized audio successfully.")
            except Exception as e:
                logging.error(f"Error during transcription request: {e}")
                raise e

            # Process the response
            try:
                transcribe_text = self.process_response(response)
                logging.debug("Response processed successfully.")
            except Exception as e:
                logging.error(f"Error processing transcription response: {e}")
                raise e

            # Cleanup
            try:
                files_handler.delete_file(standardized_audio_path)
                logging.debug(f"Temporary audio file deleted: {standardized_audio_path}")
            except Exception as e:
                logging.error(f"Error deleting temporary file: {e}")
                # Log error but do not raise; this step is not critical

            return transcribe_text

        except Exception as e:
            logging.error(f"Error in transcribe_audio_file: {e}")
            raise e  # Re-raise the exception for external handling if necessary
        
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
    def convert_audio_sample_rate(self, input_file_path, target_sample_rate=16000):
        input_file_path = str(input_file_path)

        try:
            # Guess the file type
            mime_type, _ = mimetypes.guess_type(input_file_path)

            # Determine file type and load the audio
            if mime_type == "audio/mpeg" or input_file_path.endswith('.mp3'):
                audio = AudioSegment.from_mp3(input_file_path)
            elif mime_type == "audio/wav" or input_file_path.endswith('.wav'):
                audio = AudioSegment.from_wav(input_file_path)
            else:
                raise ValueError(f"Unsupported file format: {input_file_path}. Please use MP3 or WAV files.")

            # Set the target sample rate and channels
            audio = audio.set_frame_rate(target_sample_rate).set_channels(1)

            # Create output file path
            output_file = f"{os.path.splitext(input_file_path)[0]}_converted.wav"

            # Export the audio to the new file
            audio.export(output_file, format="wav")

            return output_file

        except Exception as e:
            # Log and raise the error for debugging
            raise RuntimeError(f"Error converting audio file: {input_file_path}. Details: {str(e)}")