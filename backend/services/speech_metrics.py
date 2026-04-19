import json
import re
from data.filler_words import FILLER_WORDS

# 1️⃣ FILLER DETECTOR
def detect_fillers(transcript):
    total_words = 0
    filler_count = 0
    filler_bursts = 0

    for segment in transcript:
        text = segment["text"].lower()
        words = text.split()
        total_words += len(words)

        segment_fillers = 0
        for filler in FILLER_WORDS:
            # Use regex for whole word match to prevent "uh" matching "uh-huh" incorrectly
            matches = re.findall(r'\b' + re.escape(filler) + r'\b', text)
            segment_fillers += len(matches)
            
        filler_count += segment_fillers
        
        # A burst of fillers in a single segment
        if segment_fillers >= 2:
            filler_bursts += 1

    filler_density = filler_count / total_words if total_words > 0 else 0

    return filler_density, filler_count, filler_bursts


# 2️⃣ PAUSE ANALYZER
def analyze_pauses(transcript):
    pauses = []
    pause_spike_positions = []

    for i in range(1, len(transcript)):
        prev_end = transcript[i-1]["end"]
        curr_start = transcript[i]["start"]

        pause = curr_start - prev_end
        if pause > 0:
            pauses.append(pause)
            if pause > 2.0:
                pause_spike_positions.append({
                    "start": prev_end,
                    "end": curr_start,
                    "duration": round(pause, 2)
                })

    avg_pause_duration = sum(pauses) / len(pauses) if pauses else 0

    return avg_pause_duration, pause_spike_positions


# 3️⃣ SPEECH SPEED (WPM)
def calculate_wpm(transcript):
    if not transcript:
        return 0, 0
        
    total_words = 0
    segment_wpms = []

    for segment in transcript:
        words = len(segment["text"].split())
        total_words += words
        
        duration = segment["end"] - segment["start"]
        if duration > 0:
            segment_wpms.append(words / (duration / 60))

    total_time = transcript[-1]["end"] - transcript[0]["start"]
    minutes = total_time / 60
    speech_speed = total_words / minutes if minutes > 0 else 0
    
    # speed instability (variance across segments)
    if len(segment_wpms) > 1:
        mean = sum(segment_wpms) / len(segment_wpms)
        variance = sum((w - mean) ** 2 for w in segment_wpms) / len(segment_wpms)
        speed_instability = variance ** 0.5
    else:
        speed_instability = 0

    return speech_speed, speed_instability


# 4️⃣ HESITATION SCORE
def calculate_hesitation(pause_spike_positions, filler_bursts, speed_instability):
    
    pause_score = min(len(pause_spike_positions) * 0.2, 1.0)
    filler_score = min(filler_bursts * 0.2, 1.0)
    speed_score = min(speed_instability / 30, 1.0)

    hesitation_score = (pause_score + filler_score + speed_score) / 3

    return round(hesitation_score, 2)


# MAIN FUNCTION
def analyze_speech(transcript):
    filler_density, filler_count, filler_bursts = detect_fillers(transcript)
    avg_pause_duration, pause_spike_positions = analyze_pauses(transcript)
    speech_speed, speed_instability = calculate_wpm(transcript)

    hesitation_score = calculate_hesitation(
        pause_spike_positions, filler_bursts, speed_instability
    )

    result = {
        "filler_density": round(filler_density, 3),
        "filler_count": filler_count,
        "avg_pause_duration": round(avg_pause_duration, 2),
        "pause_spike_positions": pause_spike_positions,
        "speech_speed": round(speech_speed, 2),
        "hesitation_score": hesitation_score
    }
    
    # outputs saved as JSON
    with open('speech_metrics_output.json', 'w') as f:
        json.dump(result, f, indent=4)

    return result