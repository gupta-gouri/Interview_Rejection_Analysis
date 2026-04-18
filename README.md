# Interview Rejection Analysis

A two-part system for analysing interview recordings and evaluating candidate responses to help identify patterns that lead to interview rejection.

---

## Project Structure

```
Interview_Rejection_Analysis/
├── main.py                        # FastAPI application entry point
├── config.py                      # Shared configuration (paths, model, limits)
├── requirements.txt               # Root app dependencies
├── routers/
│   └── upload.py                  # /upload endpoint (audio ingest)
├── services/
│   ├── whisper_service.py         # Whisper-based audio transcription
│   └── segmentation_service.py   # Transcript chunking / timeline formatting
├── utils/
│   └── time_formatter.py          # Seconds → mm:ss helper
├── temp_audio/                    # Temporary storage for uploaded audio (auto-created)
└── backend/
    ├── main.py                    # CLI evaluation pipeline entry point
    ├── requirements.txt           # Backend-specific dependencies
    ├── services/
    │   ├── llm_service.py         # Gemini LLM scoring (clarity, depth, etc.)
    │   ├── star_detector.py       # Keyword-based STAR method detector
    │   ├── role_weighting.py      # Role-specific score weighting
    │   └── weakness_analyzer.py  # Weakness ranking by severity
    └── utils/
        └── parser.py              # Safe JSON parser for LLM output
```

---

## Part 1 — Audio Upload & Transcription (FastAPI)

Accepts an audio file plus job metadata, transcribes it with [OpenAI Whisper](https://github.com/openai/whisper), and returns a segmented timeline.

### Setup

```bash
pip install -r requirements.txt
```

### Run

```bash
uvicorn main:app --reload
```

### API

#### `POST /upload`

| Field              | Type   | Description                              |
|--------------------|--------|------------------------------------------|
| `file`             | file   | Audio file (`.wav`, `.mp3`, `.m4a`, `.mp4`) |
| `role`             | string | Job role (e.g. `SDE`, `HR`, `Analyst`)  |
| `experience_level` | string | Experience level (e.g. `junior`, `senior`) |

**Response**

```json
{
  "job_id": "<uuid>",
  "role": "SDE",
  "experience_level": "junior",
  "segments": [
    { "start": "00:00", "end": "00:45", "text": "..." }
  ]
}
```

#### `GET /`

Health-check endpoint. Returns `{ "status": "Server running successfully 🚀" }`.

### Configuration

Environment variables (or defaults in `config.py`):

| Variable        | Default  | Description                           |
|-----------------|----------|---------------------------------------|
| `WHISPER_MODEL` | `small`  | Whisper model size: `tiny/base/small/medium/large` |

---

## Part 2 — LLM Evaluation Pipeline (`backend/`)

A CLI script that scores a candidate answer using the Gemini API and surfaces the most impactful weaknesses.

### Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```
GEMINI_API_KEY=your_api_key_here
```

### Run

```bash
cd backend
python main.py
```

### Pipeline Steps

1. **LLM Evaluation** (`llm_service.py`) — Calls Gemini to score clarity, structure, technical depth, relevance, and communication on a 1–5 scale.
2. **STAR Detection** (`star_detector.py`) — Keyword-based check for Situation / Task / Action / Result components.
3. **Score Merging** — Averages LLM structure score with STAR structure score.
4. **Role-Based Weighting** (`role_weighting.py`) — Applies role-specific weights to produce a final score and per-dimension breakdown.
5. **Weakness Ranking** (`weakness_analyzer.py`) — Identifies dimensions below threshold and ranks them by weighted severity.

### Supported Roles

| Role     | Key Weight          |
|----------|---------------------|
| `SDE`    | `depth_score` (0.35) |
| `HR`     | `communication_score` (0.35) |
| `Analyst`| `clarity_score` (0.30) |

---

## .env

Both sub-projects use `.env` files for secrets. These are excluded from version control via `.gitignore`.

