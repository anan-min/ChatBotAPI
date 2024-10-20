from pydub import AudioSegment

def convert_audio_sample_rate(input_file, output_file, target_sample_rate=16000):
    if input_file.suffix == '.mp3':
        audio = AudioSegment.from_mp3(input_file)
    elif input_file.suffix == '.wav':
        audio = AudioSegment.from_wav(input_file)
    else:
        raise ValueError("Unsupported file format. Please use MP3 or WAV files.")


    audio = audio.set_frame_rate(target_sample_rate)


    audio.export(output_file, format='wav')