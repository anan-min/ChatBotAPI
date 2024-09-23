from quart import abort
import base64
from mimetypes import guess_type
from app.utilities.request_data import RequestData

DEFAULT_PROVIDER = "open_ai"


class RequestProcessor:
    def __init__(self) -> None:
        pass 

    async def process(self, request):
        # Get JSON data
        data = request.get_json()
        
        # Extract base64-encoded audio file
        encoded_audio = data['audio_file']
        
        # Decode the audio file
        audio_data = base64.b64decode(encoded_audio)
        
        # You could save this data to a file or process it directly
        with open('received_audio.mp3', 'wb') as audio_file:
            audio_file.write(audio_data)

        # Handle other data
        stt_provider = data.get('stt_provider', DEFAULT_PROVIDER)
        tts_provider = data.get('tts_provider', DEFAULT_PROVIDER)
        query_provider = data.get('query_provider', DEFAULT_PROVIDER)

        return RequestData(stt_provider, tts_provider, query_provider, audio_data)