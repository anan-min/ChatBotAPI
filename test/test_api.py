from app.providers import OpenAIProvider
from pathlib import Path
import requests

url = 'http://127.0.0.1:5000/'

def test_openai_api_flow():
    # Instantiate the provider
    provider = OpenAIProvider()

    # Define the path to the audio file
    audio_file_path = Path(__file__).parent.parent / 'app' / 'data' / 'test' / 'voice.wav'

    # Open the file in binary read mode
    with open(audio_file_path, "rb") as audio_file:
        # Define the files dictionary for the multipart/form-data request
        files = {
            'audio_file': (audio_file_path.name, audio_file, 'audio/wav')
        }
        
        # Make the POST request with the audio file
        response = requests.post(url, files=files)
        
        # Check the response status
        if response.status_code == 200:
            print("Success: Received response from server")
            print(response.json())  # Print JSON response if JSON received
        else:
            print(f"Error: Server responded with status code {response.status_code}")
            print(response.text)  # Print response body for non-200 responses

# Call the function to test the API
test_openai_api_flow()
