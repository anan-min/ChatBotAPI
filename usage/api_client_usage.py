from pathlib import Path
import os
import requests
import time 

url = 'http://127.0.0.1:5000/'
AUDIO_FILE_PATH = Path(__file__).parent.parent / 'app' / 'data' / 'test' / 'Recording.wav'
SAVE_PATH = Path(__file__).parent.parent / 'app' / 'data' / 'test' / 'speech1.wav'

def send_audio_file(api_url, file_path):
    """
    Sends an audio file to the specified API endpoint.

    :param api_url: str - The URL of the API endpoint.
    :param file_path: str - The local path to the audio file to be sent.
    :return: dict - The API response as a dictionary.
    """

    start_time = time.time()

    data = {
        'stt_provider': "google",
        'tts_provider': "google",
        'query_provider': "openai"
    }

    # Open the file in binary mode
    with open(file_path, 'rb') as file:
        files = {'audio_file': (os.path.basename(file_path), file, 'audio/wav')}
        response = requests.post(api_url, data=data, files=files)


    end_time = time.time()

    print(f"API call took {end_time - start_time} seconds to complete")
    
    if response.status_code == 200:
        with open(SAVE_PATH, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192): 
                file.write(chunk)
        print(f"File successfully downloaded and saved to {SAVE_PATH}")
    else:
        print(f"Failed to download the file: {response.status_code} - {response.text}")

        
# Call the function to test the API
send_audio_file(url, AUDIO_FILE_PATH)