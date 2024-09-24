from quart import abort
import base64
from mimetypes import guess_type
from app.utils.request_data import RequestData
from app.utils.session_manager import SessionManager
DEFAULT_PROVIDER = "open_ai"


class RequestProcessor:
    def __init__(self) -> None:
        pass 

    async def process(self, request):

        if 'audio_file' not in await request.files:
            abort(400, description="No audio file part in the request.")

        # Get the file from the request
        audio_file = (await request.files)['audio_file']

        # Read the file's content into memory
        audio_data = audio_file.read()

        # Handle other data from the form
        form_data = await request.form
        stt_provider = form_data.get('stt_provider', DEFAULT_PROVIDER)
        tts_provider = form_data.get('tts_provider', DEFAULT_PROVIDER)
        query_provider = form_data.get('query_provider', DEFAULT_PROVIDER)

        return SessionManager(stt_provider, tts_provider, query_provider, audio_data)