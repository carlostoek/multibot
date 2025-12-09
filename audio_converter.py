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


def convert_video_to_video_note(input_path: str) -> str:
    """
    Convert a video file to MP4 format for video note compatibility.
    Creates a circular (square) video with maximum 60 seconds and 8MB size.

    Args:
        input_path (str): Path to the input video file

    Returns:
        str: Path to the converted MP4 video note file

    Raises:
        Exception: If conversion fails
    """
    output_path = tempfile.mktemp(suffix=".mp4")

    try:
        # Get video information to determine dimensions
        probe = ffmpeg.probe(input_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

        if not video_stream:
            raise Exception("No video stream found in input file")

        width = int(video_stream['width'])
        height = int(video_stream['height'])

        # Determine the size for square video (Telegram video notes must be square)
        size = min(width, height, 1280)  # Max 1280px for Telegram

        # Convert video to square format for video notes
        # Crop to square and scale to appropriate size
        (
            ffmpeg
            .input(input_path, t=60)  # Limit to 60 seconds maximum for video notes
            .filter('crop', f'min(iw,ih):min(iw,ih)')
            .filter('scale', size, size)
            .output(
                output_path,
                vcodec='libx264',      # H.264 codec for MP4
                pix_fmt='yuv420p',     # Pixel format for compatibility
                movflags='faststart',  # Optimize for streaming
                preset='fast',         # Conversion speed vs quality
                t=60,                  # Maximum duration 60 seconds
                fs='8MB'               # File size limit (Telegram limit)
            )
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        # Clean up the temp file if conversion fails
        if os.path.exists(output_path):
            os.unlink(output_path)
        raise Exception(f"FFmpeg video conversion failed: {e.stderr.decode() if e.stderr else str(e)}")

    # Check if output file was created successfully
    if not os.path.exists(output_path):
        raise Exception("Video conversion failed: output file was not created")

    # Check if output file has content
    if os.path.getsize(output_path) == 0:
        raise Exception("Video conversion failed: output file is empty")

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


def is_supported_audio_format(file_path: str) -> bool:
    """
    Check if the file format is supported for audio conversion.

    Args:
        file_path (str): Path to the file

    Returns:
        bool: True if format is supported, False otherwise
    """
    supported_formats = ['.mp3', '.wav', '.flac', '.aac', '.m4a', '.wma', '.ogg', '.opus']
    return Path(file_path).suffix.lower() in supported_formats


def is_supported_video_format(file_path: str) -> bool:
    """
    Check if the file format is supported for video conversion.

    Args:
        file_path (str): Path to the file

    Returns:
        bool: True if format is supported, False otherwise
    """
    supported_formats = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.3gp']
    return Path(file_path).suffix.lower() in supported_formats


def is_supported_format(file_path: str) -> bool:
    """
    Check if the file format is supported for conversion (either audio or video).

    Args:
        file_path (str): Path to the file

    Returns:
        bool: True if format is supported, False otherwise
    """
    return is_supported_audio_format(file_path) or is_supported_video_format(file_path)
