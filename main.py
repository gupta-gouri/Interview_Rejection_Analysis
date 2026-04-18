from fastapi import FastAPI
from routers.upload import router as upload_router


app = FastAPI(
    title="Interview Rejection Analysis API",
    description="Backend pipeline for interview audio upload, transcription, and segmentation",
    version="1.0.0"
)


# Include routers
app.include_router(upload_router, tags=["Upload & Transcription"])


# Health check endpoint
@app.get("/", tags=["Health Check"])
def home():
    return {
        "status": "Server running successfully 🚀"
    }