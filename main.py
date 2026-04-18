from backend.services.speech_metrics import analyze_speech

def main():
    # Sample transcript for demonstration
    sample_transcript = [
        {"start": 0, "end": 5, "text": "um I worked on a project"},
        {"start": 7, "end": 12, "text": "it was basically a system"},
        {"start": 15, "end": 20, "text": "uh it was good"}
    ]

    print("--- Speech Metrics Analysis ---")
    result = analyze_speech(sample_transcript)
    
    # Print results to console
    for key, value in result.items():
        print(f"{key}: {value}")
    
    print("\nResults have also been saved to backend/speech_metrics_output.json")

if __name__ == "__main__":
    main()
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
