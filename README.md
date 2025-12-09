# Telegram Audio/Video to Voice/Video Note Converter Bot

This bot converts audio and video files to Telegram voice and video notes.

## Features

- Converts various audio formats (MP3, WAV, etc.) to voice notes
- Converts various video formats (MP4, AVI, etc.) to video notes
- Maintains good quality during conversion
- Handles file size limits automatically
- Provides user-friendly feedback

## Setup

1. Create a bot with [@BotFather](https://t.me/BotFather) on Telegram and obtain the bot token
2. Clone this repository
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and add your bot token:
   ```bash
   cp .env.example .env
   # Edit .env and add your bot token
   ```
5. Run the bot: `python main.py`

## Usage

Simply send an audio file to the bot, and it will convert it to a voice note and send it back to you.