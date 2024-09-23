import io
from pydub import AudioSegment

def convert_audio_bytes_to_supported_format(audio_bytes, original_format='wav', target_format='mp3'):
    audio_stream = io.BytesIO(audio_bytes)
    audio = AudioSegment.from_file(audio_stream, format=original_format)
    converted_audio_buffer = io.BytesIO()
    audio.export(converted_audio_buffer, format=target_format)
    converted_audio_buffer.seek(0)
    return converted_audio_buffer

