import ffmpeg
import os
import tempfile
from pathlib import Path


def convert_audio_to_voice_note(input_path: str) -> str:
    """
    Convert an audio file to OPUS format for voice note compatibility.

    Args:
        input_path (str): Path to the input audio file

    Returns:
        str: Path to the converted OPUS file

    Raises:
        Exception: If conversion fails
    """
    fd, output_path = tempfile.mkstemp(suffix=".ogg")
    os.close(fd)

    try:
        # Convert audio to OPUS format with appropriate parameters for voice notes
        (
            ffmpeg
            .input(input_path)
            .output(
                output_path,
                codec='libopus',
                ar=48000,  # Audio sample rate
                ac=1,      # Audio channels (mono for voice notes)
                b='64k',   # Bitrate
                application='voip'  # Optimized for voice
            )
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        # Clean up the temp file if conversion fails
        if os.path.exists(output_path):
            os.unlink(output_path)
        raise Exception(f"FFmpeg conversion failed: {e.stderr.decode() if e.stderr else str(e)}")

    # Check if output file was created successfully
    if not os.path.exists(output_path):
        raise Exception("Conversion failed: output file was not created")

    # Check if output file has content
    if os.path.getsize(output_path) == 0:
        raise Exception("Conversion failed: output file is empty")

    return output_path


def get_file_size(path: str) -> int:
    """
    Get the file size in bytes.
    
    Args:
        path (str): Path to the file
        
    Returns:
        int: File size in bytes
    """
    return os.path.getsize(path)


SUPPORTED_FORMATS = {'.mp3', '.wav', '.flac', '.aac', '.m4a', '.wma', '.ogg', '.opus'}

def is_supported_format(file_path: str) -> bool:
    """
    Check if the file format is supported for conversion.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        bool: True if format is supported, False otherwise
    """
    return Path(file_path).suffix.lower() in SUPPORTED_FORMATS