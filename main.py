import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.filters import Command
from dotenv import load_dotenv
import tempfile
import os
from audio_converter import convert_audio_to_voice_note, convert_video_to_video_note, get_file_size, is_supported_format, is_supported_video_format

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")

# Telegram file size limit (20MB for general files, 8MB for video notes)
TELEGRAM_FILE_SIZE_LIMIT = 20 * 1024 * 1024
TELEGRAM_VIDEO_NOTE_SIZE_LIMIT = 8 * 1024 * 1024  # 8MB for video notes

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Command handler for /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Welcome to the Audio/Video to Voice/Video Note Converter Bot!\n\n"
        "Send me an audio file (MP3, WAV, etc.) to convert it to a Telegram voice note.\n"
        "Send me a video file (MP4, AVI, etc.) to convert it to a Telegram video note."
    )

# Handler for audio documents
@dp.message(lambda message: message.document and (message.document.mime_type.startswith('audio/') or
                                                 is_supported_format('.' + message.document.file_name.split('.')[-1])))
async def handle_audio_document(message: types.Message):
    temp_input_path = None
    output_path = None

    try:
        # Inform user that processing has started
        processing_msg = await message.answer("Processing your audio file...")

        # Get the file info
        file_id = message.document.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path

        # Check file size before downloading (if available)
        if message.document.file_size and message.document.file_size > TELEGRAM_FILE_SIZE_LIMIT:
            await message.reply(
                f"File is too large ({message.document.file_size / (1024*1024):.2f} MB). "
                f"Telegram supports files up to 20 MB."
            )
            await bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)
            return

        # Download the file
        downloaded_file = await bot.download_file(file_path)

        # Create a temporary file for the input audio
        input_ext = '.' + message.document.file_name.split('.')[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=input_ext) as temp_input:
            temp_input.write(downloaded_file.read())
            temp_input_path = temp_input.name

        # Check if the file format is supported
        if not is_supported_format(temp_input_path):
            await message.reply("Unsupported file format. Please send an audio file (MP3, WAV, FLAC, etc.).")
            if temp_input_path and os.path.exists(temp_input_path):
                os.unlink(temp_input_path)
            await bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)
            return

        # Convert the audio to voice note format
        output_path = convert_audio_to_voice_note(temp_input_path)

        # Check file size
        voice_note_size = get_file_size(output_path)
        if voice_note_size > TELEGRAM_FILE_SIZE_LIMIT:
            await message.reply(
                f"Converted audio is too large ({voice_note_size / (1024*1024):.2f} MB). "
                f"Telegram supports voice notes up to 20 MB."
            )
            # Clean up temporary files
            if temp_input_path and os.path.exists(temp_input_path):
                os.unlink(temp_input_path)
            if output_path and os.path.exists(output_path):
                os.unlink(output_path)
            await bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)
            return

        # Send the converted voice note
        await message.reply_voice(FSInputFile(output_path))

        # Clean up temporary files
        if temp_input_path and os.path.exists(temp_input_path):
            os.unlink(temp_input_path)
        if output_path and os.path.exists(output_path):
            os.unlink(output_path)

        # Delete the processing message
        await bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)

    except Exception as e:
        logger.error(f"Error processing audio file: {e}")
        error_msg = "An error occurred while processing your audio file. Please ensure it's a valid audio file."

        # Provide more specific error messages
        if "FFmpeg conversion failed" in str(e):
            error_msg = "Failed to convert the audio file. Please ensure it's in a valid audio format."
        elif "output file was not created" in str(e) or "output file is empty" in str(e):
            error_msg = "Conversion failed. The audio file may be corrupted or in an unsupported format."

        # Clean up files if they exist
        if temp_input_path and os.path.exists(temp_input_path):
            os.unlink(temp_input_path)
        if output_path and os.path.exists(output_path):
            os.unlink(output_path)

        # Send error message to user
        await message.reply(error_msg)


# Handler for audio files sent as audio (not document)
@dp.message(lambda message: message.audio)
async def handle_audio(message: types.Message):
    temp_input_path = None
    output_path = None

    try:
        # Inform user that processing has started
        processing_msg = await message.answer("Processing your audio file...")

        # Get the file info
        file_id = message.audio.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path

        # Check file size before downloading (if available)
        if message.audio.file_size and message.audio.file_size > TELEGRAM_FILE_SIZE_LIMIT:
            await message.reply(
                f"File is too large ({message.audio.file_size / (1024*1024):.2f} MB). "
                f"Telegram supports files up to 20 MB."
            )
            await bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)
            return

        # Download the file
        downloaded_file = await bot.download_file(file_path)

        # Create a temporary file for the input audio
        input_ext = '.mp3'  # Default extension for audio type
        if hasattr(message.audio, 'file_name') and message.audio.file_name:
            input_ext = '.' + message.audio.file_name.split('.')[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=input_ext) as temp_input:
            temp_input.write(downloaded_file.read())
            temp_input_path = temp_input.name

        # Convert the audio to voice note format
        output_path = convert_audio_to_voice_note(temp_input_path)

        # Check file size
        voice_note_size = get_file_size(output_path)
        if voice_note_size > TELEGRAM_FILE_SIZE_LIMIT:
            await message.reply(
                f"Converted audio is too large ({voice_note_size / (1024*1024):.2f} MB). "
                f"Telegram supports voice notes up to 20 MB."
            )
            # Clean up temporary files
            if temp_input_path and os.path.exists(temp_input_path):
                os.unlink(temp_input_path)
            if output_path and os.path.exists(output_path):
                os.unlink(output_path)
            await bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)
            return

        # Send the converted voice note
        await message.reply_voice(FSInputFile(output_path))

        # Clean up temporary files
        if temp_input_path and os.path.exists(temp_input_path):
            os.unlink(temp_input_path)
        if output_path and os.path.exists(output_path):
            os.unlink(output_path)

        # Delete the processing message
        await bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)

    except Exception as e:
        logger.error(f"Error processing audio file: {e}")
        error_msg = "An error occurred while processing your audio file. Please ensure it's a valid audio file."

        # Provide more specific error messages
        if "FFmpeg conversion failed" in str(e):
            error_msg = "Failed to convert the audio file. Please ensure it's in a valid audio format."
        elif "output file was not created" in str(e) or "output file is empty" in str(e):
            error_msg = "Conversion failed. The audio file may be corrupted or in an unsupported format."

        # Clean up files if they exist
        if temp_input_path and os.path.exists(temp_input_path):
            os.unlink(temp_input_path)
        if output_path and os.path.exists(output_path):
            os.unlink(output_path)

        # Send error message to user
        await message.reply(error_msg)


# Handler for video documents
@dp.message(lambda message: message.document and (message.document.mime_type.startswith('video/') or
                                                 is_supported_video_format('.' + message.document.file_name.split('.')[-1])))
async def handle_video_document(message: types.Message):
    temp_input_path = None
    output_path = None

    try:
        # Inform user that processing has started
        processing_msg = await message.answer("Processing your video file...")

        # Get the file info
        file_id = message.document.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path

        # Check file size before downloading (if available)
        if message.document.file_size and message.document.file_size > TELEGRAM_FILE_SIZE_LIMIT:
            await message.reply(
                f"File is too large ({message.document.file_size / (1024*1024):.2f} MB). "
                f"Telegram supports files up to 20 MB."
            )
            await bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)
            return

        # Download the file
        downloaded_file = await bot.download_file(file_path)

        # Create a temporary file for the input video
        input_ext = '.' + message.document.file_name.split('.')[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=input_ext) as temp_input:
            temp_input.write(downloaded_file.read())
            temp_input_path = temp_input.name

        # Check if the file format is supported
        if not is_supported_video_format(temp_input_path):
            await message.reply("Unsupported video format. Please send a video file (MP4, AVI, MOV, etc.).")
            if temp_input_path and os.path.exists(temp_input_path):
                os.unlink(temp_input_path)
            await bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)
            return

        # Convert the video to video note format
        output_path = convert_video_to_video_note(temp_input_path)

        # Check file size
        video_note_size = get_file_size(output_path)
        if video_note_size > TELEGRAM_VIDEO_NOTE_SIZE_LIMIT:
            await message.reply(
                f"Converted video is too large ({video_note_size / (1024*1024):.2f} MB). "
                f"Telegram video notes must be under 8 MB."
            )
            # Clean up temporary files
            if temp_input_path and os.path.exists(temp_input_path):
                os.unlink(temp_input_path)
            if output_path and os.path.exists(output_path):
                os.unlink(output_path)
            await bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)
            return

        # Send the converted video note
        await message.reply_video_note(FSInputFile(output_path))

        # Clean up temporary files
        if temp_input_path and os.path.exists(temp_input_path):
            os.unlink(temp_input_path)
        if output_path and os.path.exists(output_path):
            os.unlink(output_path)

        # Delete the processing message
        await bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)

    except Exception as e:
        logger.error(f"Error processing video file: {e}")
        error_msg = "An error occurred while processing your video file. Please ensure it's a valid video file."

        # Provide more specific error messages
        if "FFmpeg video conversion failed" in str(e):
            error_msg = "Failed to convert the video file. Please ensure it's in a valid video format."
        elif "output file was not created" in str(e) or "output file is empty" in str(e):
            error_msg = "Video conversion failed. The video file may be corrupted or in an unsupported format."
        elif "No video stream found" in str(e):
            error_msg = "The file does not contain a valid video stream."

        # Clean up files if they exist
        if temp_input_path and os.path.exists(temp_input_path):
            os.unlink(temp_input_path)
        if output_path and os.path.exists(output_path):
            os.unlink(output_path)

        # Send error message to user
        await message.reply(error_msg)


# Handler for video files sent as video (not document)
@dp.message(lambda message: message.video)
async def handle_video(message: types.Message):
    temp_input_path = None
    output_path = None

    try:
        # Inform user that processing has started
        processing_msg = await message.answer("Processing your video file...")

        # Get the file info
        file_id = message.video.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path

        # Check file size before downloading (if available)
        if message.video.file_size and message.video.file_size > TELEGRAM_FILE_SIZE_LIMIT:
            await message.reply(
                f"File is too large ({message.video.file_size / (1024*1024):.2f} MB). "
                f"Telegram supports files up to 20 MB."
            )
            await bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)
            return

        # Download the file
        downloaded_file = await bot.download_file(file_path)

        # Create a temporary file for the input video
        input_ext = '.mp4'  # Default extension for video type
        if hasattr(message.video, 'file_name') and message.video.file_name:
            input_ext = '.' + message.video.file_name.split('.')[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=input_ext) as temp_input:
            temp_input.write(downloaded_file.read())
            temp_input_path = temp_input.name

        # Convert the video to video note format
        output_path = convert_video_to_video_note(temp_input_path)

        # Check file size
        video_note_size = get_file_size(output_path)
        if video_note_size > TELEGRAM_VIDEO_NOTE_SIZE_LIMIT:
            await message.reply(
                f"Converted video is too large ({video_note_size / (1024*1024):.2f} MB). "
                f"Telegram video notes must be under 8 MB."
            )
            # Clean up temporary files
            if temp_input_path and os.path.exists(temp_input_path):
                os.unlink(temp_input_path)
            if output_path and os.path.exists(output_path):
                os.unlink(output_path)
            await bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)
            return

        # Send the converted video note
        await message.reply_video_note(FSInputFile(output_path))

        # Clean up temporary files
        if temp_input_path and os.path.exists(temp_input_path):
            os.unlink(temp_input_path)
        if output_path and os.path.exists(output_path):
            os.unlink(output_path)

        # Delete the processing message
        await bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)

    except Exception as e:
        logger.error(f"Error processing video file: {e}")
        error_msg = "An error occurred while processing your video file. Please ensure it's a valid video file."

        # Provide more specific error messages
        if "FFmpeg video conversion failed" in str(e):
            error_msg = "Failed to convert the video file. Please ensure it's in a valid video format."
        elif "output file was not created" in str(e) or "output file is empty" in str(e):
            error_msg = "Video conversion failed. The video file may be corrupted or in an unsupported format."
        elif "No video stream found" in str(e):
            error_msg = "The file does not contain a valid video stream."

        # Clean up files if they exist
        if temp_input_path and os.path.exists(temp_input_path):
            os.unlink(temp_input_path)
        if output_path and os.path.exists(output_path):
            os.unlink(output_path)

        # Send error message to user
        await message.reply(error_msg)


if __name__ == "__main__":
    print("Starting bot...")
    asyncio.run(dp.start_polling(bot))