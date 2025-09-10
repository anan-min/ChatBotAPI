import os
import asyncio
import time
from google.cloud import texttospeech
from google.cloud import speech
from google.cloud import language_v1
from dotenv import load_dotenv
from providers.google_config import api_credentials

load_dotenv()

# Set your credentials path
# Path to your service account JSON file


class GoogleProvider:
    def __init__(self) -> None:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_credentials
        self.tts_client = texttospeech.TextToSpeechClient()
        self.stt_client = speech.SpeechClient()
        self.language_client = language_v1.LanguageServiceClient()

    async def transcribe_audio_file(self, audio_data, language_code="th-TH", encoding=None, sample_rate_hertz=None):
        """Transcribe audio data using Google Speech-to-Text"""
        start_time = time.time()
        loop = asyncio.get_running_loop()
        transcribed_data = await loop.run_in_executor(
            None,
            self._transcribe_sync,
            audio_data,
            language_code,
            encoding,
            sample_rate_hertz
        )
        end_time = time.time()
        print(f"Transcription took {end_time - start_time:.2f} seconds")
        return transcribed_data

    def _transcribe_sync(self, audio_data, language_code, encoding, sample_rate_hertz):
        """Synchronous transcription helper"""
        audio = speech.RecognitionAudio(content=audio_data)

        # Auto-detect encoding and sample rate if not provided
        if encoding is None:
            # Try to detect common formats based on audio data headers
            if audio_data.startswith(b'RIFF') and b'WAVE' in audio_data[:12]:
                encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16
                if sample_rate_hertz is None:
                    sample_rate_hertz = 16000  # Default for WAV
            elif audio_data.startswith(b'\xff\xfb') or audio_data.startswith(b'ID3'):
                encoding = speech.RecognitionConfig.AudioEncoding.MP3
                sample_rate_hertz = None  # Let Google auto-detect for MP3
            elif audio_data.startswith(b'OggS'):
                encoding = speech.RecognitionConfig.AudioEncoding.OGG_OPUS
                sample_rate_hertz = None  # Let Google auto-detect for OGG
            elif audio_data.startswith(b'fLaC'):
                encoding = speech.RecognitionConfig.AudioEncoding.FLAC
                sample_rate_hertz = None  # Let Google auto-detect for FLAC
            else:
                # Default fallback
                encoding = speech.RecognitionConfig.AudioEncoding.WEBM_OPUS
                sample_rate_hertz = None

        config = speech.RecognitionConfig(
            encoding=encoding,
            language_code=language_code,
            enable_automatic_punctuation=True,
            model="latest_long"  # Use latest model for better accuracy
        )

        # Only set sample rate if provided and not None
        if sample_rate_hertz is not None:
            config.sample_rate_hertz = sample_rate_hertz

        try:
            response = self.stt_client.recognize(config=config, audio=audio)

            # Combine all transcripts
            transcripts = []
            for result in response.results:
                transcripts.append(result.alternatives[0].transcript)

            return " ".join(transcripts)

        except Exception as e:
            print(f"Transcription error: {e}")
            # Try with WEBM_OPUS as fallback
            if encoding != speech.RecognitionConfig.AudioEncoding.WEBM_OPUS:
                config.encoding = speech.RecognitionConfig.AudioEncoding.WEBM_OPUS
                config.sample_rate_hertz = None

                response = self.stt_client.recognize(
                    config=config, audio=audio)
                transcripts = []
                for result in response.results:
                    transcripts.append(result.alternatives[0].transcript)

                return " ".join(transcripts)
            else:
                raise e

    async def speech_synthesis(self, text, language_code=None, voice_name=None):
        """Convert text to speech using Google Text-to-Speech - hardcoded to Thai"""

        # Hardcode to Thai language
        language_code = "th-TH"
        voice_name = "th-TH-Standard-A"  # Thai voice
        print(f"Using Thai TTS: {voice_name}")

        start_time = time.time()
        loop = asyncio.get_running_loop()
        audio_content = await loop.run_in_executor(
            None,
            self._synthesis_sync,
            text,
            language_code,
            voice_name
        )
        end_time = time.time()
        print(f"Speech synthesis took {end_time - start_time:.2f} seconds")
        return audio_content

    def _synthesis_sync(self, text, language_code, voice_name):
        """Synchronous speech synthesis helper"""
        input_text = texttospeech.SynthesisInput(text=text)

        # Let Google auto-detect if no specific voice is provided
        if voice_name is None:
            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code
            )
        else:
            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                name=voice_name,
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
            )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = self.tts_client.synthesize_speech(
            input=input_text,
            voice=voice,
            audio_config=audio_config
        )

        return response.audio_content


# Example usage


async def main():
    provider = GoogleProvider()

    # Text to speech
    text = "Hello, this is a test of Google's text-to-speech service."
    audio_content = await provider.speech_synthesis(text)
    await provider.save_audio_to_file(audio_content, "output.mp3")

    # Speech to text (assuming you have an audio file)
    # transcription = await provider.transcribe_audio_file("input_audio.wav")
    # print(f"Transcription: {transcription}")

    # Text analysis
    analysis = await provider.query_text_file("I love this product! It's amazing and works perfectly.")
    print(f"Analysis: {analysis}")

if __name__ == "__main__":
    asyncio.run(main())
