from src.llm.bedrock_client import generate

def analyze_profile(resume_text: str) -> str:
    prompt = f"""
You are a career analyst.

IMPORTANT:
- Do NOT use LaTeX, math notation, or \\boxed.
- Do NOT say "The final answer is".
- Output ONLY these headings: SUMMARY, SKILLS, TARGET ROLES, MISSING SKILLS, 4 WEEK ROADMAP, JOB SEARCH KEYWORDS.
- If something is missing, write N/A.
- Do not add any other sections.

Resume:
{resume_text}

Format exactly like this:

SUMMARY:
...

SKILLS:
- ...

TARGET ROLES:
- ...

MISSING SKILLS:
- ...

4 WEEK ROADMAP:
Week 1: ...
Week 2: ...
Week 3: ...
Week 4: ...

JOB SEARCH KEYWORDS:
- ...
"""
    return generate(prompt)
