from quart import Quart, request
from app.services import (TranscribeProcessor, QueryProcessor, SpeechProcessor, RequestProcessor)
from app.services.response_processor import ResponseProcessor
from app.utils import files_handler
from app.utils.session_manager import SessionManager

from app.services.sentiment_processor import SentimentProcessor
import asyncio

from app.utils.timing import timing

def setup_routes(app: Quart):
    files_handler.delete_temp_files()
    transcribe_processor = TranscribeProcessor()
    query_processor = QueryProcessor()
    speech_processor = SpeechProcessor()
    request_processor = RequestProcessor()
    response_processor = ResponseProcessor()
    sentimentProcessor = SentimentProcessor()

    @app.route("/", methods=["POST"])
    async def index():
        session: SessionManager = None
        with timing("Request processing"):
            session = await request_processor.process(request)

        with timing("Transcription"):
            await transcribe_processor.process(session)
            print(f"\nTranscribed text: {session.get_transcribe_text()}")

        with timing("Query processing"):
            await query_processor.process(session)
            print(f"\nQuery response: {session.get_query_text()}")

        with timing("Speech processing"):
            await asyncio.gather(
                speech_processor.process(session),
                sentimentProcessor.process(session)
            )


        return await response_processor.process(session)