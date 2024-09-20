from quart import Quart, request, jsonify, abort
import asyncio
import httpx 
from mimetypes import guess_type
from app.utilities import RequestData


app = Quart(__name__)


@app.route("/", methods=["POST"])
async def index():
    request_data = parse_request(request)  

    transcribe_text = transcribe_data(request_data.get_audio_file(), request_data)

    query_response = query_response(transcribe_text, request_data)

    output_audio_file = convert_to_speech(query_response, request_data)

    return jsonify({"output_audio_file": output_audio_file})

async def convert_to_speech(query_response, request_data):
    pass

async def query_response(transcribe_text, request_data):
    pass
    

async def transcribe_data(audio_file, request_data):
    pass 
    

async def parse_request(request):
    if request is None:
        abort(400, jsonify({"message": "No request"}))
    if request.method != "POST":
        abort(400, jsonify({"message": "Not a POST request"}) )
    if request.headers.get("Content-Type") != "application/json":
        abort(400, jsonify({"message": "Not a JSON request"}))

    try:
        request_data = await request.get_json()
        if request_data is None:
            abort(400, description="No JSON data provided.")
    except Exception as e:
        # If there's an error in reading JSON data
        abort(400, description=f"Invalid JSON: {str(e)}")

    audio_file = request_data.get("audio_file")

    if audio_file is None:
        abort(400, jsonify({"message": "No audio file"}))
    file_type, _ = guess_type(audio_file.filename)
    if not file_type.startswith('audio/'):
        abort(400, 'Invalid file format. Only audio files are allowed.')


    stt_provider_lists = []
    tts_provider_lists = [] 
    query_provider_lists = [] 


    stt_provider = request_data.get("stt_provider")
    tts_provider = request_data.get("tts_provider")
    
    if stt_provider not in stt_provider_lists:
        stt_provider = "openai"
    if tts_provider not in tts_provider_lists:
        tts_provider = "openai"
    if query_provider not in query_provider_lists:
        query_provider = "openai"

    return RequestData(stt_provider, tts_provider, query_provider, audio_file)
