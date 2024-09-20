from quart import Quart, request, jsonify
from app.services import TranscribeProcessor, SpeechProcessor, QueryProcessor, RequestProcessor

app = Quart(__name__)
transcribe_processor = TranscribeProcessor()
query_processor = QueryProcessor()
speech_processor = SpeechProcessor()
request_processor = RequestProcessor()

@app.route("/", methods=["POST"])
async def index():
    request_data = request_processor.parse_data(request)
    
    text = transcribe_processor(request_data.get_text(), request_data.get_stt_provider())
    query_response = query_processor(text, request_data.get_query_provider())
    audio_reponse = speech_processor(query_response, request_data.get_tts_provider())

    return jsonify(audio_reponse)


