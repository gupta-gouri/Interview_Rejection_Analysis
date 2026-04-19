import os
from dotenv import load_dotenv

# Define base path dynamically and load .env from backend folder
base_path = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_path, ".env")
load_dotenv(env_path)  # This loads the variables from .env

from fastapi import FastAPI
from backend.routers.upload import router as upload_router

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