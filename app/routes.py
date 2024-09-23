from quart import Quart, request, send_file, after_this_request
from app.services import (TranscribeProcessor, QueryProcessor, SpeechProcessor, RequestProcessor)
from app.services.response_processor import ResponseProcessor
from app.utils import files_handler
import time 

def setup_routes(app: Quart):
    files_handler.delete_temp_files()
    transcribe_processor = TranscribeProcessor()
    query_processor = QueryProcessor()
    speech_processor = SpeechProcessor()
    request_processor = RequestProcessor()
    response_processor = ResponseProcessor()


    @app.route("/", methods=["POST"])
    async def index():
        start_time = time.time()
        request_data = await request_processor.process(request)
        end_time = time.time()
        print(f"Request processing took {end_time - start_time} seconds to complete")

        start_time = time.time()
        text = await transcribe_processor.process(request_data)
        end_time = time.time()
        print(f"Transcription took {end_time - start_time} seconds to complete")
        print(f"Transcribed text: {text}")

        start_time = time.time()
        query_response = await query_processor.process(request_data, text)
        end_time = time.time()
        print(f"Query processing took {end_time - start_time} seconds to complete")
        print(f"Query response: {query_response}")


        audio_response = await speech_processor.process(request_data, query_response)

        return await response_processor.process(audio_response)
