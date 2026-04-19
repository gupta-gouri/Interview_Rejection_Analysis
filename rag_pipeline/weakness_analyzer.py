def identify_weaknesses(scores: dict, weights: dict, metadata: dict = None):
    """
    Identifies and ranks weaknesses based on score severity and role weighting.
    Severity = (Max Score - Current Score) * Weight
    """
    MAX_SCORE = 5
    WEAKNESS_THRESHOLD = 3
    
    # Mapping internal keys to user-friendly weakness IDs
    WEAKNESS_MAP = {
        "depth_score": "technical_depth_low",
        "clarity_score": "unclear_communication",
        "structure_score": "weak_structure_usage",
        "communication_score": "low_confidence_delivery",
        "relevance_score": "off_topic_response"
    }

    weaknesses = []

    # 1. Analyze scores from LLM/STAR
    for key, weight in weights.items():
        score = scores.get(key, 0)
        if score <= WEAKNESS_THRESHOLD:
            severity = round((MAX_SCORE - score) * weight, 2)
            weaknesses.append({
                "id": WEAKNESS_MAP.get(key, f"low_{key}"),
                "severity": severity,
                "score": score
            })

    # 2. Analyze metadata (e.g., pause duration)
    if metadata:
        # Example: high_pause_duration if pauses > 2 seconds
        if metadata.get("pause_duration", 0) > 2.0:
            # Assign a static severity or calculate based on a 'filler' weight
            # For now, let's use a standard impact factor
            weaknesses.append({
                "id": "high_pause_duration",
                "severity": 0.5, # Static impact for demo
                "score": metadata["pause_duration"]
            })

    # Sort by severity descending
    weaknesses.sort(key=lambda x: x["severity"], reverse=True)

    return weaknesses
