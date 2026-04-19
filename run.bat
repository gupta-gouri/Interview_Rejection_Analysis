@echo off
echo Starting Interview Analysis Engine Pipeline...

REM Set PYTHONPATH so all modules (ingestion, rag_pipeline, backend, etc.) can resolve each other
set PYTHONPATH=%cd%

echo Starting FastAPI Backend...
start cmd /k ".venv\Scripts\activate && uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000"

echo Starting React Frontend...
start cmd /k "cd frontend && npm start"

echo Both servers are starting!
echo Backend API will run on http://localhost:8000
echo Frontend will run on http://localhost:3000
