import os

# -------------------------------
# Project Base Directory
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# -------------------------------
# Storage Configuration
# -------------------------------
UPLOAD_DIR = os.path.join(BASE_DIR, "temp_audio")

# Ensure directory exists automatically
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -------------------------------
# Whisper Model Configuration
# -------------------------------
# Options:
# tiny | base | small | medium | large
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")


# -------------------------------
# Allowed Audio Formats
# -------------------------------
ALLOWED_AUDIO_EXTENSIONS = {"wav", "mp3", "m4a", "mp4"}


# -------------------------------
# Segment Chunk Configuration
# -------------------------------
MAX_SEGMENT_CHAR_LENGTH = 200