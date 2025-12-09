# Audio to Voice Note Converter Bot - Documentation

## Overview

The Audio to Voice Note Converter Bot is a Telegram bot that converts audio files (mainly MP3) to Telegram voice notes. The bot accepts various audio formats and converts them to OPUS format suitable for Telegram voice notes.

## Features

- Converts multiple audio formats (MP3, WAV, FLAC, AAC, M4A, WMA, OGG, OPUS) to Telegram-compatible voice notes
- Handles Telegram's file size limitations (20MB maximum)
- Provides user feedback during processing
- Comprehensive error handling with user-friendly messages
- Automatically cleans up temporary files

## Architecture

### Main Components

1. **main.py**: The main bot application using aiogram 3 framework
2. **audio_converter.py**: Audio conversion logic using FFmpeg
3. **requirements.txt**: Python dependencies
4. **docs/**: Documentation files

### File Flow

1. User sends an audio file to the bot
2. Bot downloads the file to a temporary location
3. Audio converter processes the file to OPUS format
4. File size is checked against Telegram's limit
5. Converted voice note is sent back to the user
6. Temporary files are cleaned up

## Configuration

### Environment Variables

- `BOT_TOKEN`: Your Telegram bot token obtained from [@BotFather](https://t.me/BotFather)

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Install system FFmpeg: `apt install ffmpeg`
4. Set up your environment variables in a `.env` file
5. Run the bot: `python main.py`

## Usage

Simply send an audio file (MP3, WAV, etc.) to the bot, and it will convert it to a voice note and send it back to you.

## Error Handling

The bot handles various error scenarios:

- **Unsupported formats**: Notifies user of unsupported audio formats
- **File too large**: Informs user if the file exceeds Telegram's 20MB limit
- **Conversion failure**: Provides specific error messages for conversion issues
- **Corrupted files**: Detects and reports corrupted audio files

## Dependencies

- **aiogram==3.5.0**: Telegram bot framework
- **ffmpeg-python==0.2.0**: Python wrapper for FFmpeg
- **python-dotenv==1.0.0**: Environment variable management

## File Formats Supported

### Input Formats
- MP3 - MPEG Audio Layer III
- WAV - Waveform Audio File Format
- FLAC - Free Lossless Audio Codec
- AAC - Advanced Audio Coding
- M4A - MPEG-4 Audio
- WMA - Windows Media Audio
- OGG - Ogg Vorbis
- OPUS - Opus Interactive Audio Codec

### Output Format
- OGG/OPUS - Optimized for Telegram voice notes (48kHz, mono, 64k bitrate, voip application)

## API Reference

### Main Bot Functions

#### `cmd_start(message: types.Message)`
Handles the /start command and provides instructions to users.

#### `handle_audio_document(message: types.Message)`
Processes audio files sent as documents, converts them to voice notes, and sends them back.

#### `handle_audio(message: types.Message)`
Processes audio files sent as audio type, converts them to voice notes, and sends them back.

### Audio Conversion Functions

#### `convert_audio_to_voice_note(input_path: str) -> str`
Converts an audio file to OPUS format suitable for voice notes.

#### `get_file_size(path: str) -> int`
Returns the file size in bytes.

#### `is_supported_format(file_path: str) -> bool`
Checks if the file format is supported for conversion.