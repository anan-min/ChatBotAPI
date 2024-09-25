import time
import csv
from fetch_transcription_result import fetch_transcription_result
from start_transcription import start_transcription_job

base_uri = "s3://fordatasample/sample/common_voice_th_"
start_number_str = "001"
start_number = int(start_number_str)

language_code = "th-TH"
num_iterations = 100  # แก้


with open('transcription_results.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Filename', 'Provider', 'Model', 'Time Taken (s)', 'File size', 'Word Count', 'Transcribed Text']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for _ in range(num_iterations):
        job_name = f"Transcription_{start_number_str}"
        job_uri = f"{base_uri}{start_number_str}.mp3"

        start_time = time.time()

        try:
            status = start_transcription_job(job_name, job_uri, language_code)
            
            while status['TranscriptionJob']['TranscriptionJobStatus'] in ['IN_PROGRESS', 'QUEUED']:
                status = start_transcription_job(job_name, job_uri, language_code) 

            end_time = time.time()
            elapsed_time = end_time - start_time  

            if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
                transcribed_result = fetch_transcription_result(status, job_uri)

                writer.writerow({
                    'Filename': job_uri.split('/')[-1],  
                    'Provider': 'amazon',
                    'Model': 'Transcribe',
                    'Time Taken (s)': elapsed_time,
                    'File size': transcribed_result.get('file_size', 'N/A'),  
                    'Word Count': transcribed_result.get('word_count', 'N/A'),
                    'Transcribed Text': transcribed_result.get('transcribed_text', 'N/A')  
                })

            else:
                pass  

        except Exception as e:
            pass  

        start_number += 1  
        start_number_str = f"{start_number:03d}"  
