import os
from dotenv import load_dotenv

load_dotenv()  # This loads the variables from .env

# Now your code can access the key
api_key = os.getenv("GEMINI_API_KEY")
print(f"DEBUG: Key found: {os.getenv('GEMINI_API_KEY') is not None}")

from services.llm_service import evaluate_response
from services.star_detector import detect_star
from services.role_weighting import calculate_weighted_score, ROLE_WEIGHTS
from services.weakness_analyzer import identify_weaknesses

if __name__ == "__main__":
    
    sample_answer = """
    I worked on a project where we had performance issues.
    My task was to optimize the system.
    I implemented caching and optimized queries.
    As a result, performance improved by 40%.
    """

    role = "SDE"
    # Added sample metadata for demonstration
    sample_metadata = {
        "pause_duration": 3.5  # seconds
    }

    # Step 1: LLM Evaluation
    llm_scores = evaluate_response(sample_answer)

    # Step 2: STAR Detection
    star_result = detect_star(sample_answer)

    # Step 3: Merge structure scores
    combined_structure = (llm_scores["structure_score"] + star_result["structure_score"]) / 2
    llm_scores["structure_score"] = combined_structure

    # Step 4: Final Role-Based Score
    final_result = calculate_weighted_score(llm_scores, role)

    # Step 5: Weakness Ranking
    role_weights = ROLE_WEIGHTS.get(role, ROLE_WEIGHTS["SDE"])
    weaknesses = identify_weaknesses(llm_scores, role_weights, sample_metadata)

    print("LLM Scores:", llm_scores)
    print("STAR:", star_result)
    print("Final Result:", final_result)
    print("\nWeaknesses (Sorted by Severity):")
    for w in weaknesses:
        print(f"- {w['id']} (Severity: {w['severity']})")