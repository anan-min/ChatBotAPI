from utils import files_handler
from quart import send_file, current_app, jsonify
from utils.session_manager import SessionManager
import asyncio
import time 
import base64
class ResponseProcessor:
    def __init__(self) -> None:
        pass

    async def process(self, session: SessionManager ):
        audio_response = session.get_query_speech()
        text_response = session.get_query_text()
        file_path = files_handler.save_audio_file(audio_response)
        print(f"\nSpeech response: {file_path}")
        async def cleanup():
            await asyncio.sleep(1)
            files_handler.delete_file(file_path)

        start_time = time.time()
        with open(file_path, "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")

        # Prepare response data
        response_data = {
            "text": text_response,
            "audio_base64": audio_base64,  # Base64 encoded audio data
            "mime_type": "audio/wav"  # Mime type for the audio
        }


        end_time = time.time()
        print(f"Response processing without process took {end_time - start_time} seconds to complete")

        current_app.add_background_task(cleanup)   
        return  jsonify(response_data)
