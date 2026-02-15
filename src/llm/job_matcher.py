"""
Semantic job matching (simple MVP).
Takes profile text + jobs, asks LLM to score each, then ranks.
Uses AWS Bedrock (Llama 3.3 70B) via generate().
"""

from src.llm.bedrock_client import generate


def match_jobs(profile_text: str, jobs: list[dict], top_n: int = 10, limit: int = 20):
    scored_jobs = []

    # Simple senior title detection
    senior_words = ["senior", "lead", "principal", "manager", "director", "staff", "head", "vp", "architect", "chief", "sr"]

    for job in jobs[:limit]:
        title = job.get("title", "N/A")
        company = job.get("company", "N/A")
        location = job.get("location", "N/A")
        description = (job.get("description") or "")[:1200]

        prompt = f"""
You are a job matching expert.

Candidate Profile:
{profile_text}

Job Posting:
Title: {title}
Company: {company}
Location: {location}
Description: {description}

Instructions:
- Give a match score from 0 to 100 on the FIRST line (number only).
- On the SECOND line, explain why in 1–2 sentences.
- Be realistic for an entry-level / new-grad candidate.

Output format (exact):
<number>
<reason>
""".strip()

        try:
            output = generate(prompt) or ""
            lines = output.strip().splitlines()

            # Default values
            score = 0
            reason = "No reason returned."

            # First line = score
            if lines:
                try:
                    score = int(float(lines[0].strip()))
                except:
                    score = 0

            # Second line = reason
            if len(lines) > 1:
                reason = lines[1].strip()

            # Cap senior roles (by title)
            if any(w in title.lower() for w in senior_words):
                score = min(score, 30)
                reason += " (Role appears senior-level.)"

            # Cap roles requiring too many years of experience (by description)
            desc_lower = description.lower()
            for y in range(5, 16):  # 5 years through 15 years
                if f"{y} years" in desc_lower or f"{y}+ years" in desc_lower:
                    score = min(score, 30)
                    reason += " (Looks mid/senior based on years of experience.)"
                    break

            scored_jobs.append({
                **job,
                "match_score": score,
                "match_reason": reason
            })

        except Exception as e:
            scored_jobs.append({
                **job,
                "match_score": 0,
                "match_reason": f"Scoring failed: {e}"
            })

    # Sort highest score first
    scored_jobs.sort(key=lambda x: x["match_score"], reverse=True)

    return scored_jobs[:top_n]
