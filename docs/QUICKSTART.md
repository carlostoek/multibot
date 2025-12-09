# Quick Start Guide

## Prerequisites

- Python 3.7 or higher
- System with FFmpeg installed
- Telegram Bot Token

## Step-by-step Setup

### 1. Clone or download the repository
```bash
git clone <repository-url>
cd multibot
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Install system FFmpeg
Choose the appropriate command for your system:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**CentOS/RHEL:**
```bash
sudo yum install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Termux (Android):**
```bash
pkg install ffmpeg
```

### 4. Configure the bot
1. Create a copy of the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Edit the `.env` file and add your Telegram bot token:
   ```
   BOT_TOKEN=your_actual_bot_token_here
   ```

### 5. Test the installation
Run the test script to verify all dependencies are working:
```bash
python test_bot.py
```

You should see output confirming all imports are successful and FFmpeg is available.

### 6. Start the bot
```bash
python main.py
```

### 7. Use the bot
1. Open Telegram and find your bot
2. Send the `/start` command to verify the bot is working
3. Send an audio file (MP3, WAV, etc.) to convert to a voice note
4. The bot will process the file and send back a voice note

## Example Usage

1. **Send an MP3 file** as a document or audio
2. The bot will respond with "Processing your audio file..."
3. After conversion, you'll receive the audio as a voice note
4. If there are any issues, you'll receive an appropriate error message

## Next Steps

- Review the [Configuration Guide](CONFIG.md) for more detailed setup information
- Check the [Troubleshooting Guide](TROUBLESHOOTING.md) if you encounter issues
- Read the [API Reference](API.md) if you plan to modify the code