import base64
class ResponseProcessor:
    def __init__(self) -> None:
        pass

    def process(self, audio_file, request_data):
        audio_file.seek(0)
        encoded_audio = base64.b64encode(audio_file.read()).decode('utf-8')
        # Create JSON payload
        payload = {
            "stt_provider": "openai",
            "tts_provider": "openai",
            "query_provider": "openai",
            "audio_file": encoded_audio
        }

        return payload