# Configuration Guide

## Environment Variables

The bot requires a Telegram bot token to run. Create a `.env` file in the project root with the following content:

```env
BOT_TOKEN=your_bot_token_here
```

### Obtaining a Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Start a chat with BotFather and use the `/newbot` command
3. Follow the prompts to create your bot
4. Copy the token provided by BotFather
5. Add it to your `.env` file

## Dependencies

### Python Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- aiogram==3.5.0 (Telegram bot framework)
- ffmpeg-python==0.2.0 (FFmpeg wrapper)
- python-dotenv==1.0.0 (Environment variable management)

### System Dependencies

The bot requires FFmpeg to be installed on your system:

#### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
```

#### On CentOS/RHEL:
```bash
sudo yum install ffmpeg
```

#### On macOS:
```bash
brew install ffmpeg
```

#### On Termux (Android):
```bash
pkg install ffmpeg
```

## File Structure

```
multibot/
├── main.py                 # Main bot application
├── audio_converter.py      # Audio conversion functionality
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment file
├── README.md              # Project overview
├── test_bot.py            # Test script
└── docs/                  # Documentation
    └── README.md          # Detailed documentation
```

## Running the Bot

### Development

For development purposes, run:

```bash
python main.py
```

### Production

For production deployment, consider using a process manager like systemd, supervisor, or pm2:

```bash
# Example systemd service file
[Unit]
Description=Telegram Audio to Voice Note Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/multibot
ExecStart=/path/to/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## Troubleshooting

### Common Issues

1. **Bot not responding**: Check that your bot token is correct and the bot is not blocked
2. **Conversion errors**: Ensure FFmpeg is properly installed and in the system PATH
3. **File size errors**: Large files may exceed Telegram's 20MB limit
4. **Unsupported format errors**: Check that the audio file format is supported

### Log Files

The bot logs at INFO level. To enable more detailed logging, modify the logging configuration in `main.py`:

```python
logging.basicConfig(level=logging.DEBUG)  # Change to DEBUG for more detail
```