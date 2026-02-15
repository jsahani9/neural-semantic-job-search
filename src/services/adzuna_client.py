"""
Adzuna API client for Canadian job search.
"""

from __future__ import annotations

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

BASE_URL = "https://api.adzuna.com/v1/api/jobs/ca/search"


def search_jobs(
    keywords: str,
    location: str = "Canada",
    max_results: int = 20,
    page: int = 1,
    max_days_old: int = 60,
):
    """
    Search for jobs on Adzuna (Canadian market).
    Returns simplified job dictionaries.
    """

    keywords = (keywords or "").strip()
    if not keywords:
        return []

    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        raise RuntimeError("ADZUNA_APP_ID and ADZUNA_APP_KEY must be set in .env")

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": min(max_results, 50),
        "what": keywords,
        "where": location,
        "max_days_old": max_days_old,
        "sort_by": "date",
    }

    url = f"{BASE_URL}/{page}"

    try:
        response = httpx.get(url, params=params, timeout=10.0)
        response.raise_for_status()

        results = response.json().get("results", []) or []

        jobs = []
        for job in results:
            jobs.append(
                {
                    "title": job.get("title", ""),
                    "company": job.get("company", {}).get("display_name", "Unknown"),
                    "location": job.get("location", {}).get("display_name", ""),
                    "description": job.get("description", ""),
                    "salary_min": job.get("salary_min"),
                    "salary_max": job.get("salary_max"),
                    "url": job.get("redirect_url", ""),
                    "created": job.get("created", ""),
                }
            )

        return jobs

    except httpx.HTTPError as e:
        raise RuntimeError(f"Adzuna API error: {str(e)}")
