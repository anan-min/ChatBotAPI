from quart import Quart, request, jsonify
from app.services import TranscribeProcessor, SpeechProcessor, QueryProcessor, RequestProcessor

def setup_routes(app: Quart):
    transcribe_processor = TranscribeProcessor()
    query_processor = QueryProcessor()
    speech_processor = SpeechProcessor()
    request_processor = RequestProcessor()

    @app.route("/", methods=["POST"])
    async def index():
        request_data = await request_processor.process(request)
        text = await transcribe_processor.process(request_data)
        query_response = await query_processor.process(request_data, text)
        audio_response = await speech_processor.process(request_data, query_response)

        return jsonify(audio_response)
