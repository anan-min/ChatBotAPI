from quart import jsonify
import base64
from app.utils import files_handler
from app.utils.session_manager import SessionManager
import asyncio
import time
from quart import current_app

class ResponseProcessor:
    def __init__(self) -> None:
        pass

    async def process(self, session: SessionManager):
        start_time = time.time()

        # Define cleanup task
        async def cleanup():
            await asyncio.sleep(1)
            files_handler.delete_file(file_path)

        # Get audio and text from session
        audio_response = session.get_query_speech()
        text_response = session.get_query_text()

        # Save audio file and encode it to base64
        file_path = files_handler.save_audio_file(audio_response)
        with open(file_path, "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")

        # Prepare response data
        response_data = {
            "text": text_response,
            "audio_base64": audio_base64,  # Base64 encoded audio data
            "mime_type": "audio/wav"  # Mime type for the audio
        }

        # Add cleanup task to background
        current_app.add_background_task(cleanup)

        # Measure processing time
        end_time = time.time()
        print(f"Response processing took {end_time - start_time} seconds")

        # Return response as JSON
        return jsonify(response_data)
