from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import tempfile
from pdfminer.high_level import extract_text

# allow importing ai_engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from ai_engine.model.predictor import analyze_resume

app = FastAPI(title="SkillNuron AI API")

# ---------------- CORS (allow frontend) ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Root Test ----------------
@app.get("/")
def root():
    return {"message": "Welcome to SkillNuron AI API"}

# ---------------- Resume Analyzer Endpoint ----------------
@app.post("/analyze-resume")
async def analyze_resume_api(file: UploadFile = File(...)):

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as temp:
        temp.write(await file.read())
        temp_path = temp.name

    # Extract text depending on file type
    if file.filename.lower().endswith(".pdf"):
        text = extract_text(temp_path)

    else:
        # txt/doc fallback
        with open(temp_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

    # Run AI model
    result = analyze_resume(text)

    return result
