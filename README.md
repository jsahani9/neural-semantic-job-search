🧠 Neural Semantic Job Search Engine

An end-to-end Generative AI system that matches resumes to live job postings using semantic search, LLM reasoning, and explainable ranking.

Built to demonstrate applied AI engineering skills: document parsing, embeddings, LLM scoring, API orchestration, and production-ready architecture.

🚀 Features

Resume PDF upload + profile extraction

Live job ingestion via Adzuna API

Semantic job matching using embeddings

LLM-based job scoring + reasoning (AWS Bedrock – Llama 3.3 70B)

Seniority-aware ranking (filters Manager / Senior roles)

Explainable match results

Streamlit frontend + FastAPI backend

Fully Dockerized (frontend + API)

Structured profile analysis (skills, summary, experience)

Cost-controlled LLM scoring (Top-K reranking)

🏗 Architecture
Resume PDF
   ↓
Profile Analyzer (LLM)
   ↓
Job Ingestion (Adzuna API)
   ↓
Pre-filtering + Heuristics
   ↓
LLM Job Scoring (Bedrock)
   ↓
Ranked Matches + Explanations
   ↓
Streamlit UI

Stack

Backend

Python

FastAPI

AWS Bedrock (Meta Llama 3.3 70B)

Adzuna Jobs API

Frontend

Streamlit

Infra

Docker / Docker Compose

🧩 Matching Pipeline

Resume PDF → structured profile (summary + skills)

Fetch live jobs from Adzuna

Pre-filter based on:

Role seniority

Title keywords

LLM evaluates Top-K jobs using rubric:

Skill match

Role alignment

Level fit

Jobs returned with:

Score (0–100)

Explanation

Missing skills

This hybrid approach combines deterministic filtering with LLM reasoning for high-quality ranking.

📦 Running Locally
Prerequisites

Docker

AWS credentials with Bedrock access

Environment Variables

Create .env:

AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1

ADZUNA_APP_ID=...
ADZUNA_API_KEY=...

Start Services
docker compose up --build


Then open:

Frontend:

http://localhost:8501


Backend health:

http://localhost:8000/health

📊 Example Output

Ranked job matches

LLM-generated explanations

Resume profile preview

Skill alignment feedback

🎯 Why This Project Matters

This project demonstrates:

Real-world GenAI integration

LLM orchestration with APIs

Prompt engineering + scoring rubrics

Production-ready containerization

Applied ML system design

Explainable AI outputs

Built to reflect how modern AI systems are deployed in industry.

🛠 Future Improvements

Embedding-based retrieval layer (vector DB)

Evaluation metrics (MRR / Recall@K)

Resume tailoring assistant

Job clustering / deduplication

Feedback loop for ranking refinement

👤 Author

Jasveen Singh Sahani
Junior AI / Applied ML Engineer

LinkedIn: <your link>
GitHub: <your repo>
