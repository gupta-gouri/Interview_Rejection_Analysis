from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import uuid
import shutil
import os

from config import UPLOAD_DIR, ALLOWED_AUDIO_EXTENSIONS
from services.whisper_service import transcribe_audio
from services.segmentation_service import segment_transcript


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

    try:
        # Run Whisper transcription
        raw_segments = transcribe_audio(file_path)

        # Run segmentation logic
        segments = segment_transcript(raw_segments)
    finally:
        # Clean up temporary file regardless of success or failure
        if os.path.exists(file_path):
            os.remove(file_path)

    return {
        "job_id": job_id,
        "role": role,
        "experience_level": experience_level,
        "segments": segments
    }