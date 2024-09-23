from quart import Quart, request, send_file, after_this_request
from app.services import (TranscribeProcessor, QueryProcessor, SpeechProcessor, RequestProcessor)
from app.services.response_processor import ResponseProcessor
from app.utilities import files_handler

def setup_routes(app: Quart):
    files_handler.delete_temp_files()
    transcribe_processor = TranscribeProcessor()
    query_processor = QueryProcessor()
    speech_processor = SpeechProcessor()
    request_processor = RequestProcessor()
    response_processor = ResponseProcessor()


    @app.route("/", methods=["POST"])
    async def index():
        request_data = await request_processor.process(request)
        text = await transcribe_processor.process(request_data)
        query_response = await query_processor.process(request_data, text)
        audio_response = await speech_processor.process(request_data, query_response)
        return await response_processor.process(audio_response)
