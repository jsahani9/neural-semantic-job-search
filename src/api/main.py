from __future__ import annotations

from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import Any, Dict, List

from src.services.resume_parser import extract_text_from_pdf
from src.llm.profile_analyzer import analyze_profile
from src.services.adzuna_client import search_jobs
from src.llm.job_matcher import match_jobs

app = FastAPI(title="Neural Semantic Job Search", version="0.1.0")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/match")
async def match_resume_to_jobs(
    resume: UploadFile = File(...),
    keywords: str = "software engineer",
    location: str = "Canada",
    max_results: int = 20,
    top_n: int = 10,
    limit: int = 20,
) -> Dict[str, Any]:
    """
    Upload a resume PDF, fetch jobs from Adzuna, rank them using LLM, return top matches.
    """

    if resume.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    try:
        pdf_bytes = await resume.read()

        # resume_parser expects a BinaryIO-like object with .read()
        class _InMemoryFile:
            def __init__(self, b: bytes):
                self._b = b
                self._used = False

            def read(self):
                if self._used:
                    return b""
                self._used = True
                return self._b

        resume_text = extract_text_from_pdf(_InMemoryFile(pdf_bytes))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {e}")

    try:
        profile_text = analyze_profile(resume_text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile analysis failed: {e}")

    try:
        jobs = search_jobs(
            keywords=keywords,
            location=location,
            max_results=max_results,
            page=1,
            max_days_old=60,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Job fetch failed: {e}")

    try:
        ranked = match_jobs(profile_text, jobs, top_n=top_n, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job matching failed: {e}")

    # Trim descriptions to keep API response small
    for j in ranked:
        if j.get("description"):
            j["description"] = j["description"][:400] + "..."

    return {
        "keywords_used": keywords,
        "location": location,
        "jobs_fetched": len(jobs),
        "top_n": top_n,
        "matches": ranked,
        "profile_preview": profile_text[:800],  # optional: keep response smaller
    }
