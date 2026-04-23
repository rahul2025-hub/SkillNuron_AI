"""FastAPI main application entry point."""
import tempfile
from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pdfminer.high_level import extract_text

from ai_engine.model.predictor import analyze_resume
from .routers import auth, skills, jobs

app = FastAPI(title="SkillNuron AI API")

# ---------------- CORS (allow frontend) ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Include Routers ----------------
app.include_router(auth.router, prefix="/api/v1")
app.include_router(skills.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")


# ---------------- Root Test ----------------
@app.get("/")
def root() -> dict:
    """Root endpoint for API health check."""
    return {"message": "Welcome to SkillNuron AI API"}


# ---------------- Resume Analyzer Endpoint ----------------
@app.post("/analyze-resume")
async def analyze_resume_api(file: UploadFile = File(...)) -> dict:
    """Analyze a resume PDF/TXT file and return AI-powered insights."""
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as temp:
        temp.write(await file.read())
        temp_path = temp.name

    try:
        # Extract text depending on file type
        if file.filename.lower().endswith(".pdf"):
            text = extract_text(temp_path)
        else:
            # txt fallback
            with open(temp_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()

        # Run AI model
        result = analyze_resume(text)
        return result
    finally:
        # Clean up temporary file
        Path(temp_path).unlink(missing_ok=True)
