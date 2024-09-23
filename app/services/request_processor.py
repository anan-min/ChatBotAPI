from quart import abort
from quart import jsonify, abort
from app.utilities.request_data import RequestData
from mimetypes import guess_type


class RequestProcessor:
    def __init__(self) -> None:
        pass 
    async def parse_data(self, request_data):
        request = self.request_data
        
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
            abort(400, description=f"Invalid JSON: {str(e)}")

        audio_file = request_data.get("audio_file")

        if audio_file is None:
            abort(400, jsonify({"message": "No audio file"}))
        file_type, _ = guess_type(audio_file.filename)
        if not file_type.startswith('audio/'):
            abort(400, 'Invalid file format. Only audio files are allowed.')

        return RequestData(
                audio_file=audio_file  
                stt_provider=request_data.get("stt_provider", None),
                tts_provider=request_data.get("tts_provider", None),
                query_provider=request_data.get("query_provider", None),
            )
    