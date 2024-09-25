import requests
import boto3
from pythainlp import word_tokenize

def count_thai_words(text):
    tokens = word_tokenize(text, engine='newmm') 
    return len(tokens)  

def fetch_transcription_result(status, job_uri):
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']

        try:
            response = requests.get(transcript_url)

            if response.status_code == 200:
                transcription_result = response.json()  

                if 'results' in transcription_result and 'transcripts' in transcription_result['results']:
                    transcript_text = transcription_result['results']['transcripts'][0]['transcript']

                    word_count = count_thai_words(transcript_text)  

                    s3 = boto3.client('s3')
                    bucket_name = job_uri.split('/')[2]
                    file_key = '/'.join(job_uri.split('/')[3:])
                    file_info = s3.head_object(Bucket=bucket_name, Key=file_key)
                    file_size = file_info['ContentLength'] 

                    return {
                        'transcribed_text': transcript_text,
                        'file_size': file_size,  
                        'word_count': word_count  
                    }
                else:
                    return None
            else:
                return None
        except Exception as e:
            return None
    else:
        return None
