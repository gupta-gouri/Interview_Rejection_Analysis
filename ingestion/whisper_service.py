import whisper
from backend.config import WHISPER_MODEL


# Load Whisper model once at startup
model = whisper.load_model(WHISPER_MODEL)


def transcribe_audio(file_path: str):
    """
    Transcribes an audio file using Whisper and returns timestamped segments.
    Output format:
    [
        {
            "start": float,
            "end": float,
            "text": str
        }
    ]
    """

    result = model.transcribe(file_path)

    segments = []

    for seg in result.get("segments", []):
        segments.append(
            {
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"].strip()
            }
        )

    return segments