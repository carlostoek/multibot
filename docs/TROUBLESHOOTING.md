# Troubleshooting Guide

## Common Issues

### Bot Not Responding

**Symptoms**: 
- The bot doesn't reply to messages
- Commands like /start don't work

**Solutions**:
1. **Check the bot token**: Verify that your `BOT_TOKEN` in the `.env` file is correct
2. **Check internet connection**: Ensure your server/host has internet access
3. **Check if the bot is blocked**: Make sure the bot isn't blocked by the user
4. **Review logs**: Check console output for any error messages
5. **Check BotFather settings**: Ensure the bot doesn't have privacy mode enabled if you expect it to see all messages

### Audio Conversion Fails

**Symptoms**:
- Bot reports conversion errors
- "FFmpeg conversion failed" messages

**Solutions**:
1. **Verify FFmpeg installation**:
   ```bash
   ffmpeg -version
   ```
   If this command fails, FFmpeg is not installed or not in the system PATH.

2. **Install FFmpeg**:
   - Ubuntu/Debian: `sudo apt install ffmpeg`
   - CentOS/RHEL: `sudo yum install ffmpeg`
   - macOS: `brew install ffmpeg`
   - Termux: `pkg install ffmpeg`

3. **Check file permissions**: Ensure the application has write permissions to create temporary files

4. **Check audio file integrity**: Try with a known good audio file to verify the conversion process works

### File Too Large Error

**Symptoms**:
- Bot reports files are too large even when they seem small
- "Converted audio is too large" messages

**Solutions**:
1. **Understand Telegram's limits**: Telegram voice notes must be under 20MB
2. **Compress original files**: If original audio files are large, they may still be large after conversion
3. **Check original file size**: Files over 20MB will not be processed
4. **Consider alternative formats**: Some formats compress better than others

### Unsupported Format Error

**Symptoms**:
- Bot reports unsupported format
- Audio or video files are not processed

**Supported Audio Formats**:
- MP3 - MPEG Audio Layer III
- WAV - Waveform Audio File Format
- FLAC - Free Lossless Audio Codec
- AAC - Advanced Audio Coding
- M4A - MPEG-4 Audio
- WMA - Windows Media Audio
- OGG - Ogg Vorbis
- OPUS - Opus Interactive Audio Codec

**Supported Video Formats**:
- MP4 - MPEG-4 Part 14
- AVI - Audio Video Interleave
- MOV - QuickTime File Format
- MKV - Matroska Video
- WMV - Windows Media Video
- FLV - Flash Video
- WEBM - WebM Multimedia File
- M4V - iTunes Video
- 3GP - 3GPP Multimedia File

**Solutions**:
1. **Convert to supported format**: Use audio/video software to convert before sending
2. **Verify file extension**: Ensure the file has the correct extension
3. **Check file integrity**: Corrupted files may not be recognized properly

## Error Messages

### "Unsupported file format. Please send an audio file (MP3, WAV, FLAC, etc.)"

**Cause**: The file format is not supported by the bot.

**Solution**: Send an audio file in one of the supported formats.

### "Failed to convert the audio file. Please ensure it's in a valid audio format."

**Cause**: FFmpeg failed to process the audio file, possibly due to corruption or an unsupported codec.

**Solution**: Try with a different audio file to verify the issue.

### "Conversion failed. The audio file may be corrupted or in an unsupported format."

**Cause**: The output file was not created or was empty after conversion.

**Solution**: Check the original file integrity and try again.

### "No video stream found"

**Cause**: The video file does not contain a valid video stream.

**Solution**: Verify that the file is actually a video file and not just an audio file with a video extension.

### "File is too large" or "Converted audio is too large"

**For Audio**: The file exceeds Telegram's 20MB limit.
**Solution**: Reduce the original file size before sending.

### "Converted video is too large"

**For Video**: The converted video exceeds Telegram's 8MB limit for video notes.
**Solution**: Send a shorter video clip or reduce the resolution before sending.

### Video conversion fails with FFmpeg error

**Cause**: Issues with video format, codec, or file corruption.

**Solution**: Try with a different video file to ensure the file is valid and properly formatted.

## Debugging Steps

1. **Enable debug logging**: Modify the logging level in `main.py`:
   ```python
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Test FFmpeg manually**:
   ```bash
   ffmpeg -i input.mp3 -c:a libopus -ar 48000 -ac 1 -b:a 64k -application voip output.ogg
   ```

3. **Check file download**: Ensure the bot can download files from Telegram by checking network connectivity.

4. **Verify temporary directories**: Make sure the system has permissions to create temporary files.

## Performance Considerations

- **Large files**: Very large files will take longer to download, convert, and upload
- **CPU usage**: Audio conversion is CPU intensive
- **Memory usage**: Large files require more memory during processing
- **Network usage**: Files are downloaded and uploaded, consuming bandwidth

## Getting Help

If you encounter issues not covered in this guide:

1. Check the GitHub repository for known issues
2. Review the code in `main.py` and `audio_converter.py` for additional error handling
3. Ensure all dependencies are properly installed as per the configuration guide