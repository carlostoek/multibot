# API Reference

## Main Module (`main.py`)

### Bot Handlers

#### `cmd_start(message: types.Message)`

**Description**: Handles the /start command and provides initial instructions to users.

**Parameters**:
- `message: types.Message` - The incoming message object

**Returns**: Sends a welcome message to the user

---

#### `handle_audio_document(message: types.Message)`

**Description**: Processes audio files sent as documents, converts them to voice notes, and sends them back to the user.

**Parameters**:
- `message: types.Message` - The incoming message object containing the audio document

**Process**:
1. Downloads the audio file
2. Checks if the format is supported
3. Converts the audio to OPUS format
4. Verifies the file size is within Telegram's limit
5. Sends the converted voice note back to the user
6. Cleans up temporary files

**Error Handling**: Provides specific error messages for unsupported formats, file size limits, and conversion failures.

---

#### `handle_audio(message: types.Message)`

**Description**: Processes audio files sent as the audio type (not document), converts them to voice notes, and sends them back.

**Parameters**:
- `message: types.Message` - The incoming message object containing the audio

**Process**:
1. Downloads the audio file
2. Converts the audio to OPUS format
3. Verifies the file size is within Telegram's limit
4. Sends the converted voice note back to the user
5. Cleans up temporary files

**Error Handling**: Provides specific error messages for file size limits and conversion failures.

---

#### `handle_video_document(message: types.Message)`

**Description**: Processes video files sent as documents, converts them to video notes, and sends them back to the user.

**Parameters**:
- `message: types.Message` - The incoming message object containing the video document

**Process**:
1. Downloads the video file
2. Checks if the format is supported
3. Converts the video to square MP4 format for video notes
4. Verifies the file size is within Telegram's video note limit
5. Sends the converted video note back to the user
6. Cleans up temporary files

**Error Handling**: Provides specific error messages for unsupported formats, file size limits, and conversion failures.

---

#### `handle_video(message: types.Message)`

**Description**: Processes video files sent as the video type (not document), converts them to video notes, and sends them back.

**Parameters**:
- `message: types.Message` - The incoming message object containing the video

**Process**:
1. Downloads the video file
2. Converts the video to square MP4 format for video notes
3. Verifies the file size is within Telegram's video note limit
4. Sends the converted video note back to the user
5. Cleans up temporary files

**Error Handling**: Provides specific error messages for file size limits and conversion failures.

---

## Audio Converter Module (`audio_converter.py`)

#### `convert_audio_to_voice_note(input_path: str) -> str`

**Description**: Converts an audio file to OPUS format suitable for Telegram voice notes.

**Parameters**:
- `input_path: str` - Path to the input audio file

**Returns**:
- `str: Path` to the converted OPUS file

**Audio Parameters**:
- Sample Rate: 48000Hz
- Channels: 1 (Mono)
- Bitrate: 64k
- Application: voip (optimized for voice)

**Raises**:
- `Exception`: If FFmpeg conversion fails
- `Exception`: If output file is not created or is empty

---

#### `convert_video_to_video_note(input_path: str) -> str`

**Description**: Converts a video file to MP4 format suitable for Telegram video notes (square format).

**Parameters**:
- `input_path: str` - Path to the input video file

**Returns**:
- `str: Path` to the converted MP4 file

**Video Parameters**:
- Codec: H.264
- Format: Square (cropped to minimum of width/height)
- Max Size: 1280px
- Max Duration: 60 seconds
- Max File Size: 8MB

**Raises**:
- `Exception`: If FFmpeg conversion fails
- `Exception`: If no video stream is found
- `Exception`: If output file is not created or is empty

---

#### `get_file_size(path: str) -> int`

**Description**: Gets the file size in bytes.

**Parameters**:
- `path: str` - Path to the file

**Returns**:
- `int: File` size in bytes

---

#### `is_supported_audio_format(file_path: str) -> bool`

**Description**: Checks if the file format is supported for audio conversion.

**Parameters**:
- `file_path: str` - Path to the file

**Returns**:
- `bool: True` if format is supported for audio, False otherwise

**Supported Audio Formats**:
- .mp3, .wav, .flac, .aac, .m4a, .wma, .ogg, .opus

---

#### `is_supported_video_format(file_path: str) -> bool`

**Description**: Checks if the file format is supported for video conversion.

**Parameters**:
- `file_path: str` - Path to the file

**Returns**:
- `bool: True` if format is supported for video, False otherwise

**Supported Video Formats**:
- .mp4, .avi, .mov, .mkv, .wmv, .flv, .webm, .m4v, .3gp

---

#### `is_supported_format(file_path: str) -> bool`

**Description**: Checks if the file format is supported for conversion (either audio or video).

**Parameters**:
- `file_path: str` - Path to the file

**Returns**:
- `bool: True` if format is supported, False otherwise

---

## Constants

#### `TELEGRAM_FILE_SIZE_LIMIT`

**Value**: 20 * 1024 * 1024 (20MB in bytes)

**Description**: Maximum file size allowed for general Telegram files

#### `TELEGRAM_VIDEO_NOTE_SIZE_LIMIT`

**Value**: 8 * 1024 * 1024 (8MB in bytes)

**Description**: Maximum file size allowed for Telegram video notes