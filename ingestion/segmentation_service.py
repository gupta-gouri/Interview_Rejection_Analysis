from backend.config import MAX_SEGMENT_CHAR_LENGTH
from backend.utils.time_formatter import format_timestamp


def segment_transcript(segments, max_chunk_chars=MAX_SEGMENT_CHAR_LENGTH):
    """
    Groups Whisper transcript segments into larger logical chunks
    and converts timestamps into mm:ss format for frontend timeline use.

    Input:
    [
        {"start": float, "end": float, "text": str}
    ]

    Output:
    [
        {"start": "mm:ss", "end": "mm:ss", "text": str}
    ]
    """

    chunked_segments = []

    if not segments:
        return chunked_segments

    current_chunk = {
        "start": format_timestamp(segments[0]["start"]),
        "end": format_timestamp(segments[0]["end"]),
        "text": segments[0]["text"].strip()
    }

    for seg in segments[1:]:

        next_text = seg["text"].strip()

        if len(current_chunk["text"]) + len(next_text) <= max_chunk_chars:
            current_chunk["text"] += " " + next_text
            current_chunk["end"] = format_timestamp(seg["end"])

        else:
            chunked_segments.append(current_chunk)

            current_chunk = {
                "start": format_timestamp(seg["start"]),
                "end": format_timestamp(seg["end"]),
                "text": next_text
            }

    chunked_segments.append(current_chunk)

    return chunked_segments