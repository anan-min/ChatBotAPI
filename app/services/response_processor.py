from app.utilities import files_handler
from quart import send_file, current_app
import asyncio
class ResponseProcessor:
    def __init__(self) -> None:
        pass

    async def process(self, audio_response):
        file_path = files_handler.save_audio_file(audio_response)

        async def cleanup():
            await asyncio.sleep(1)
            files_handler.delete_file(file_path)

        response = await send_file(file_path, mimetype="audio/wav")
        current_app.add_background_task(cleanup)  
        return response