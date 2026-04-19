@echo off
echo Starting Interview Analysis Engine...

REM Start the backend in a new command window
echo Starting FastAPI Backend...
start cmd /k "cd backend && python -m uvicorn main:app --reload"

REM Start the frontend in a new command window
echo Starting React Frontend...
start cmd /k "cd frontend && npm start"

echo Both servers are starting!
echo Backend will run on http://localhost:8000
echo Frontend will run on http://localhost:3000
