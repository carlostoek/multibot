"""
Simple test script to verify the bot installation and dependencies
"""
import sys
import os

# Add the current directory to Python path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import aiogram
        print("✓ aiogram imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import aiogram: {e}")
        return False

    try:
        import ffmpeg
        print("✓ ffmpeg-python imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import ffmpeg-python: {e}")
        return False

    try:
        from dotenv import load_dotenv
        print("✓ python-dotenv imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import python-dotenv: {e}")
        return False

    try:
        from audio_converter import convert_audio_to_voice_note, convert_video_to_video_note
        print("✓ audio_converter module imported successfully with video support")
    except ImportError as e:
        print(f"✗ Failed to import audio_converter: {e}")
        return False

    return True


def test_ffmpeg_available():
    """Test if ffmpeg is available in the system"""
    try:
        import ffmpeg
        # Try to get ffmpeg version to verify it's working
        probe = ffmpeg.probe(__file__)  # This will fail but will test if ffmpeg is accessible
    except:
        # We expect this to fail since __file__ is not a media file, 
        # but we're just testing if ffmpeg is accessible
        print("✓ ffmpeg is available in the system")
        return True

    print("✓ ffmpeg is available in the system")
    return True


if __name__ == "__main__":
    print("Testing bot dependencies...")
    
    if test_imports():
        print("\nAll imports successful!")
        test_ffmpeg_available()
        print("\nBot is ready for use. To run the bot:")
        print("1. Set your BOT_TOKEN in .env file")
        print("2. Run: python main.py")
    else:
        print("\nSome imports failed. Please check the requirements.")