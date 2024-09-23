import os 
import datetime
from pathlib import Path

TEMP_PATH = Path(__file__).parent.parent / 'data' / 'temp' 
def save_audio_file(byte_data):
    """
    Saves byte data directly to an audio file. The file extension in `output_file_path`
    should correctly reflect the audio format (e.g., .wav for WAV files or .mp3 for MP3 files).

    :param byte_data: bytes - The audio data in byte format.
    :param output_file_path: str - The path where the audio file will be saved.
    """
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_file_path = os.path.join(TEMP_PATH, f"audio_{current_time}.wav")
    
    with open(output_file_path, 'wb') as audio_file:
        audio_file.write(byte_data)

    return output_file_path

def delete_file(file_path):
    os.remove(file_path)


def delete_temp_files():
    for file in os.listdir(TEMP_PATH):
        file_path = os.path.join(TEMP_PATH, file)
        if os.path.isfile(file_path):
            os.remove(file_path)