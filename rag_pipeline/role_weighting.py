ROLE_WEIGHTS = {
    "SDE": {
        "depth_score": 0.4,
        "clarity_score": 0.2,
        "structure_score": 0.2,
        "communication_score": 0.2
    },
    "HR": {
        "communication_score": 0.4,
        "structure_score": 0.3,
        "clarity_score": 0.2,
        "depth_score": 0.1
    },
    "Analyst": {
          "structure_score": 0.3,
        "depth_score": 0.2,
        "communication_score": 0.2
    }
}

def calculate_weighted_score(scores: dict, role: str):
    weights = ROLE_WEIGHTS.get(role, ROLE_WEIGHTS["SDE"])

    weighted_scores = {}
    final_score = 0

    for key, weight in weights.items():
        value = scores.get(key, 0)
        weighted = value * weight
        weighted_scores[key] = round(weighted, 2)
        final_score += weighted

    return {
        "final_score": round(final_score, 2),
        "breakdown": weighted_scores
    }