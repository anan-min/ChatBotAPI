import logging
from google.cloud import texttospeech

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_configs(voice_configs, audio_configs):
    # Test voice configurations
    try:
        language_code = voice_configs.get("language_code")
        ssml_gender = voice_configs.get("ssml_gender")

        # Validate language code
        if not language_code:
            raise ValueError("Language code is required.")
        logging.info(f"Language code: {language_code}")

        # Validate ssml gender
        if ssml_gender not in [
            texttospeech.SsmlVoiceGender.NEUTRAL,
            texttospeech.SsmlVoiceGender.MALE,
            texttospeech.SsmlVoiceGender.FEMALE,
        ]:
            raise ValueError("Invalid SSML gender.")
        logging.info(f"SSML gender: {ssml_gender}")

    except Exception as e:
        logging.error(f"Voice configuration error: {e}")

    # Test audio configurations
    try:
        audio_encoding = audio_configs.get("audio_encoding")
        speaking_rate = audio_configs.get("speaking_rate")
        pitch = audio_configs.get("pitch")
        effects_profile_id = audio_configs.get("effects_profile_id")

        # Validate audio encoding
        if audio_encoding not in [
            texttospeech.AudioEncoding.MP3,
            texttospeech.AudioEncoding.LINEAR16,
        ]:
            raise ValueError("Invalid audio encoding.")
        logging.info(f"Audio encoding: {audio_encoding}")

        # Validate speaking rate
        if not (0.25 <= speaking_rate <= 4.0):
            raise ValueError("Speaking rate must be between 0.25 and 4.0.")
        logging.info(f"Speaking rate: {speaking_rate}")

        # Validate pitch
        if not (-20.0 <= pitch <= 20.0):
            raise ValueError("Pitch must be between -20.0 and 20.0.")
        logging.info(f"Pitch: {pitch}")

        # Validate effects profile ID
        if effects_profile_id != "standard":  # Assuming "standard" is a valid profile
            raise ValueError("Invalid effects profile ID.")
        logging.info(f"Effects profile ID: {effects_profile_id}")

    except Exception as e:
        logging.error(f"Audio configuration error: {e}")

# Example usage
if __name__ == "__main__":
    voice_configs = {
        "language_code": "th-TH",
        "ssml_gender": getattr(texttospeech.SsmlVoiceGender, "NEUTRAL")
    }

    audio_configs = {
        "audio_encoding": texttospeech.AudioEncoding.MP3,
        "speaking_rate": 1.0,
        "pitch": 1.0,
        "effects_profile_id": "standard"
    }

    test_configs(voice_configs, audio_configs)