import os
from dotenv import load_dotenv
from fastapi import FastAPI
from routers.upload import router as upload_router

load_dotenv()  # This loads the variables from .env

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Interview Rejection Analysis API",
    description="Backend pipeline for interview audio upload, transcription, and segmentation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload_router, tags=["Upload & Transcription"])

# Health check endpoint
@app.get("/", tags=["Health Check"])
def home():
    return {
        "status": "Server running successfully 🚀"
    }