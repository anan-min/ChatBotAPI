from app.utils import files_handler
from quart import send_file, current_app
from app.utils.session_manager import SessionManager
import asyncio
import time 
class ResponseProcessor:
    def __init__(self) -> None:
        pass

    async def process(self, session: SessionManager ):
        audio_response = session.get_query_speech()
        file_path = files_handler.save_audio_file(audio_response)
        async def cleanup():
            await asyncio.sleep(1)
            files_handler.delete_file(file_path)

        start_time = time.time()
        response = await send_file(file_path, mimetype="audio/wav")
        end_time = time.time()
        print(f"Response processing without process took {end_time - start_time} seconds to complete")

        current_app.add_background_task(cleanup)   
        return response