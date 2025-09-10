import os
import datetime
import io
from pathlib import Path
import soundfile as sf
import numpy as np
from pydub import AudioSegment
import tempfile
import uuid
import threading

TEMP_PATH = Path(__file__).parent.parent / 'data' / 'temp'


def save_audio_file(byte_data, target_sample_rate=48000, target_format='wav'):
    """
    Saves byte data to an audio file with proper format conversion and sample rate handling.

    :param byte_data: bytes - The audio data in byte format.
    :param target_sample_rate: int - Target sample rate (default: 48000)
    :param target_format: str - Target audio format (default: 'wav')
    :return: str - Path to the saved audio file
    """
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    output_file_path = os.path.join(
        TEMP_PATH, f"audio_{current_time}_{unique_id}.{target_format}")

    if not os.path.exists(TEMP_PATH):
        os.makedirs(TEMP_PATH)

    try:
        # Method 1: Try to process with pydub for better format compatibility
        audio_segment = AudioSegment.from_file(io.BytesIO(byte_data))

        # Convert to target sample rate if needed
        if audio_segment.frame_rate != target_sample_rate:
            audio_segment = audio_segment.set_frame_rate(target_sample_rate)

        # Ensure mono channel for better compatibility
        if audio_segment.channels > 1:
            audio_segment = audio_segment.set_channels(1)

        # Export with specific parameters
        audio_segment.export(
            output_file_path,
            format=target_format,
            parameters=["-ar", str(target_sample_rate), "-ac", "1"]
        )

        print(
            f"Audio saved successfully with sample rate: {target_sample_rate}Hz")
        return output_file_path

    except Exception as e:
        print(f"Pydub processing failed: {e}")

        try:
            # Method 2: Try soundfile with numpy conversion using unique temp file
            temp_unique_id = str(uuid.uuid4())[:8]
            temp_file_path = os.path.join(TEMP_PATH, f"temp_{temp_unique_id}.tmp")
            
            try:
                # Write to unique temp file
                with open(temp_file_path, 'wb') as temp_file:
                    temp_file.write(byte_data)

                # Read with soundfile
                data, original_sr = sf.read(temp_file_path)

                # Convert to mono if stereo
                if len(data.shape) > 1:
                    data = np.mean(data, axis=1)

                # Resample if needed (simple linear interpolation)
                if original_sr != target_sample_rate:
                    data = resample_audio(
                        data, original_sr, target_sample_rate)

                # Save with soundfile
                sf.write(output_file_path, data, target_sample_rate)

                print(
                    f"Audio processed with soundfile: {original_sr}Hz -> {target_sample_rate}Hz")
                return output_file_path
            finally:
                # Clean up temp file safely
                if os.path.exists(temp_file_path):
                    try:
                        os.unlink(temp_file_path)
                    except Exception as cleanup_error:
                        print(f"Warning: Could not delete temp file {temp_file_path}: {cleanup_error}")

        except Exception as e2:
            print(f"Soundfile processing failed: {e2}")

            # Method 3: Fallback - save raw bytes and let the consumer handle it
            fallback_unique_id = str(uuid.uuid4())[:8]
            fallback_path = os.path.join(
                TEMP_PATH, f"audio_{current_time}_{fallback_unique_id}_raw.{target_format}")
            with open(fallback_path, 'wb') as audio_file:
                audio_file.write(byte_data)

            print(f"Fallback: Raw bytes saved to {fallback_path}")
            return fallback_path


def resample_audio(data, original_sr, target_sr):
    """
    Simple resampling using linear interpolation.
    For better quality, consider using librosa.resample() if available.
    """
    if original_sr == target_sr:
        return data

    # Calculate the ratio
    ratio = target_sr / original_sr
    new_length = int(len(data) * ratio)

    # Simple linear interpolation
    old_indices = np.linspace(0, len(data) - 1, new_length)
    new_data = np.interp(old_indices, np.arange(len(data)), data)

    return new_data


def save_audio_file_robust(byte_data, preferred_format='wav'):
    """
    Most robust version that tries multiple approaches and formats.
    """
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4())[:8]

    if not os.path.exists(TEMP_PATH):
        os.makedirs(TEMP_PATH)

    # Try different formats in order of preference
    formats_to_try = [preferred_format, 'wav', 'mp3', 'flac', 'm4a']

    for fmt in formats_to_try:
        try:
            output_file_path = os.path.join(
                TEMP_PATH, f"audio_{current_time}_{unique_id}.{fmt}")

            # Use pydub to detect and convert
            audio = AudioSegment.from_file(io.BytesIO(byte_data))

            # Standard processing
            audio = audio.set_frame_rate(48000)
            audio = audio.set_channels(1)  # Mono
            audio = audio.set_sample_width(2)  # 16-bit

            # Export
            audio.export(output_file_path, format=fmt)

            print(f"Successfully saved as {fmt} format with 48kHz sample rate")
            return output_file_path

        except Exception as e:
            print(f"Failed to save as {fmt}: {e}")
            continue

    # Last resort: raw bytes
    raw_unique_id = str(uuid.uuid4())[:8]
    raw_path = os.path.join(TEMP_PATH, f"audio_{current_time}_{raw_unique_id}_raw.bin")
    with open(raw_path, 'wb') as f:
        f.write(byte_data)

    print("All format conversions failed, saved as raw binary")
    return raw_path


def get_audio_info(file_path):
    """
    Get audio file information for debugging.
    """
    try:
        # Try with soundfile first
        info = sf.info(file_path)
        return {
            'sample_rate': info.samplerate,
            'channels': info.channels,
            'duration': info.duration,
            'format': info.format,
            'subtype': info.subtype
        }
    except:
        try:
            # Try with pydub
            audio = AudioSegment.from_file(file_path)
            return {
                'sample_rate': audio.frame_rate,
                'channels': audio.channels,
                'duration': len(audio) / 1000.0,  # Convert to seconds
                'format': 'detected_by_pydub'
            }
        except Exception as e:
            return {'error': str(e)}


def delete_file(file_path):
    """Delete a single file safely."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
        return False


def delete_temp_files():
    """Delete all temporary files safely."""
    if not os.path.exists(TEMP_PATH):
        return

    deleted_count = 0
    for file in os.listdir(TEMP_PATH):
        file_path = os.path.join(TEMP_PATH, file)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

    print(f"Deleted {deleted_count} temporary files")


# Usage example:
if __name__ == "__main__":
    # Example usage
    # with open("some_audio_file.mp3", "rb") as f:
    #     byte_data = f.read()
    #
    # saved_path = save_audio_file_robust(byte_data)
    # audio_info = get_audio_info(saved_path)
    # print(f"Audio info: {audio_info}")
    pass
