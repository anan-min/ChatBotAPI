from app.utilities import files_handler
import os 
import requests
class ResponseProcessor:
    def __init__(self) -> None:
        pass

    async def process(self, audio_response, request_data):
        audio_reponse_file_path = files_handler.save_audio_file(audio_response)
        return audio_reponse_file_path
            
