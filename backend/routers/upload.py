from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import uuid
import shutil
import os

from backend.config import UPLOAD_DIR, ALLOWED_AUDIO_EXTENSIONS
from ingestion.whisper_service import transcribe_audio
from ingestion.segmentation_service import segment_transcript
from ingestion.speech_metrics import analyze_speech
from rag_pipeline.llm_service import evaluate_response
from rag_pipeline.star_detector import detect_star
from rag_pipeline.role_weighting import calculate_weighted_score, ROLE_WEIGHTS
from rag_pipeline.weakness_analyzer import identify_weaknesses


router = APIRouter()


@router.post("/upload")
async def upload_audio(
    file: UploadFile = File(...),
    role: str = Form(...),
    experience_level: str = Form(...)
):

    # Validate file extension
    if "." not in file.filename:
        raise HTTPException(status_code=400, detail="Invalid file format")

    file_extension = file.filename.split(".")[-1].lower()

    if file_extension not in ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. Allowed formats: {ALLOWED_AUDIO_EXTENSIONS}"
        )

    # Generate unique job ID
    job_id = str(uuid.uuid4())

    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, f"{job_id}.{file_extension}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 1. Run Whisper transcription
    raw_segments = transcribe_audio(file_path)

    # 2. Run segmentation logic
    segments = segment_transcript(raw_segments)

    # 3. Analyze Speech Metrics
    speech_metrics = analyze_speech(raw_segments)

    # 4. Combine text for LLM Evaluation
    full_text = " ".join([seg["text"] for seg in raw_segments])
    
    # 5. LLM Evaluation
    llm_scores = evaluate_response(full_text)

    # 6. STAR Detection
    star_result = detect_star(full_text)

    # 7. Merge structure scores
    combined_structure = (llm_scores.get("structure_score", 0) + star_result.get("structure_score", 0)) / 2
    llm_scores["structure_score"] = combined_structure

    # 8. Final Role-Based Score
    final_result = calculate_weighted_score(llm_scores, role)

    # 9. Weakness Ranking
    role_weights = ROLE_WEIGHTS.get(role, ROLE_WEIGHTS.get("SDE"))
    metadata = {
        "pause_duration": speech_metrics.get("avg_pause_duration", 0)
    }
    weaknesses = identify_weaknesses(llm_scores, role_weights, metadata)

    return {
        "job_id": job_id,
        "role": role,
        "experience_level": experience_level,
        "segments": segments,
        "speech_metrics": speech_metrics,
        "llm_scores": llm_scores,
        "star_result": star_result,
        "final_result": final_result,
        "weaknesses": weaknesses
    }