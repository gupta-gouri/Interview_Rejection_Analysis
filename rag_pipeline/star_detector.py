def detect_star(text: str):
    # Basic keyword check for STAR method
    keywords = {
        "situation": ["situation", "background", "problem", "context"],
        "task": ["task", "responsibility", "goal", "objective"],
        "action": ["action", "implemented", "developed", "built", "did", "worked"],
        "result": ["result", "outcome", "consequence", "improved", "%", "achieved"]
    }
    
    found = {}
    score = 0
    text_lower = text.lower()
    
    for section, kw_list in keywords.items():
        count = sum(1 for kw in kw_list if kw in text_lower)
        found[section] = count > 0
        if count > 0:
            score += 1
            
    # Normalize score to 1-5 (roughly)
    # 4 sections, if all 4 found, score = 5. if 0 found, score = 1.
    final_score = max(1, min(5, score + 1))
    
    return {
        "structure_score": final_score,
        "components_found": found
    }
