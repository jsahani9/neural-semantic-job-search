# Neural Semantic Job Search Engine

A neural-semantic job matching system that uses **Meta Llama 3.3 70B Instruct** (via AWS Bedrock) to intelligently match your resume against real Canadian job postings from the **Adzuna API**. Upload a PDF resume, get AI-powered profile analysis, and receive ranked job matches with explainability scores.

## Why This Project Exists

Most job platforms rely on keyword matching, which fails to capture real candidate intent, transferable skills, and career trajectory.

This project explores how large language models can be used as **semantic reasoning engines** to:

- Understand resumes beyond surface keywords  
- Infer implicit skills and experience  
- Evaluate role fit holistically  
- Provide explainable ranking decisions  

The goal was to build a realistic applied GenAI system that mirrors how modern AI-powered recruitment tools could be architected in production.


---

## How It Works

```
Resume (PDF)
    │
    ▼
┌──────────────────┐
│  Resume Parser   │  ← PyMuPDF text extraction
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Profile Analyzer │  ← Llama 3.3 70B analyzes skills, gaps, roadmap
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Adzuna API      │  ← Fetches real Canadian job postings
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Job Matcher     │  ← Llama 3.3 70B scores each job 0-100
└────────┬─────────┘
         │
         ▼
   Ranked Results
   (with explanations)
```

### Neural-Semantic Matching Protocol

1. **Profile Intelligence** - Extract text from resume PDF using PyMuPDF
2. **Semantic Understanding** - Llama 3.3 70B analyzes skills, experience, target roles, skill gaps, and generates a 4-week learning roadmap
3. **Job Aggregation** - Fetch relevant Canadian job postings via Adzuna API
4. **Neural Matching** - Llama scores each job (0-100) with human-readable explanations
5. **Smart Filtering** - Automatically caps senior-level roles (by title keywords and years-of-experience requirements)
6. **Ranked Output** - Returns top N matches sorted by score

---
## Engineering Highlights

- Modular service-oriented architecture (API / LLM / services layers)
- Deterministic + LLM hybrid ranking pipeline
- Seniority-aware role filtering
- Cost-controlled Top-K LLM scoring
- Structured prompt outputs for reliable parsing
- Dockerized multi-service deployment
- Real-world API integration (Adzuna + AWS Bedrock)
- Human-readable match explanations
---
## Tech Stack

| Layer | Technology |
|-------|-----------|
| **LLM** | Meta Llama 3.3 70B Instruct (AWS Bedrock) |
| **Backend API** | FastAPI |
| **Frontend UI** | Streamlit |
| **Job Data** | Adzuna API (Canadian market) |
| **Resume Parsing** | PyMuPDF |
| **HTTP Client** | httpx |
| **Deployment** | Docker + Docker Compose |

---

## Project Structure

```
neural-semantic-job-search/
├── src/
│   ├── api/
│   │   └── main.py              # FastAPI endpoints (/health, /match)
│   ├── llm/
│   │   ├── bedrock_client.py    # AWS Bedrock Llama 3.3 70B wrapper
│   │   ├── profile_analyzer.py  # Resume → structured profile analysis
│   │   └── job_matcher.py       # Semantic job scoring & ranking
│   └── services/
│       ├── resume_parser.py     # PDF text extraction (PyMuPDF)
│       └── adzuna_client.py     # Adzuna job search API client
├── app/
│   └── streamlit_app.py         # Streamlit web UI
├── docker/
│   ├── Dockerfile.api           # FastAPI container
│   ├── Dockerfile.streamlit     # Streamlit container
│   └── docker-compose.yml       # Multi-container orchestration
├── requirements.txt
├── .env                         # API keys (not committed)
└── README.md
```

---

## Prerequisites

- **Python 3.12+**
- **AWS Account** with Bedrock access to `meta.llama3-3-70b-instruct-v1:0`
- **AWS CLI** configured (`aws configure`)
- **Adzuna API** credentials ([sign up here](https://developer.adzuna.com/))
- **Docker** (optional, for containerized deployment)

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/neural-semantic-job-search.git
cd neural-semantic-job-search
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
# AWS Bedrock
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=meta.llama3-3-70b-instruct-v1:0

# Adzuna API
ADZUNA_APP_ID=your_app_id_here
ADZUNA_APP_KEY=your_app_key_here
```

### 5. Configure AWS Credentials

Make sure your AWS CLI is configured with access to Bedrock:

```bash
aws configure
# Enter your AWS Access Key, Secret Key, and Region
```

Verify Bedrock access:

```bash
aws bedrock list-foundation-models --region us-east-1 --query "modelSummaries[?modelId=='meta.llama3-3-70b-instruct-v1:0'].modelId"
```

---

## Running Locally

### Start the FastAPI Backend

```bash
uvicorn src.api.main:app --reload --port 8000
```

API will be available at:
- Swagger docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### Start the Streamlit Frontend

In a **separate terminal**:

```bash
streamlit run app/streamlit_app.py
```

UI will be available at: http://localhost:8501

---

## Running with Docker

### 1. Create `.env` File

Make sure your `.env` file exists in the project root (see setup step 4).

### 2. Build and Run

```bash
docker compose -f docker/docker-compose.yml up --build
```

This starts two containers:

| Service | Port | URL |
|---------|------|-----|
| FastAPI Backend | 8000 | http://localhost:8000/docs |
| Streamlit Frontend | 8501 | http://localhost:8501 |

### 3. Stop Containers

```bash
docker compose -f docker/docker-compose.yml down
```

> **Note:** The Docker setup mounts your local `~/.aws` credentials into the API container (read-only) for Bedrock access.

---

## API Reference

### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

### `POST /match`

Upload a resume PDF and get ranked job matches.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resume` | file | required | PDF resume file |
| `keywords` | string | `"software engineer"` | Job search keywords |
| `location` | string | `"Canada"` | Job location filter |
| `max_results` | int | `20` | Max jobs to fetch from Adzuna |
| `top_n` | int | `10` | Number of top matches to return |
| `limit` | int | `20` | Max jobs to score with LLM (cost control) |

**Example using curl:**

```bash
curl -X POST "http://localhost:8000/match?keywords=python+developer&location=Toronto&top_n=5&limit=5" \
  -F "resume=@/path/to/your/resume.pdf"
```

**Response:**
```json
{
  "keywords_used": "python developer",
  "location": "Toronto",
  "jobs_fetched": 20,
  "top_n": 5,
  "matches": [
    {
      "title": "Junior Python Developer",
      "company": "TechCorp",
      "location": "Toronto, Ontario",
      "description": "We are looking for a junior developer...",
      "match_score": 82,
      "match_reason": "Strong alignment with Python skills and entry-level requirements."
    }
  ],
  "profile_preview": "SUMMARY:\nComputer Science graduate with..."
}
```

---

## Key Features

- **Semantic Matching** - Goes beyond keyword matching; Llama 3.3 70B understands context, implicit skills, and career trajectory
- **Senior Role Filtering** - Automatically detects and caps scores for senior-level roles (by title keywords like "Senior", "Lead", "Principal" and by years-of-experience requirements in descriptions)
- **Profile Analysis** - Generates professional summary, identifies skill gaps, suggests target roles, and creates a 4-week learning roadmap
- **Cost Optimized** - Llama 3.3 70B costs ~$0.00072/1K tokens (~$1 total project cost vs $7+ with Claude). Configurable `limit` parameter to control how many jobs get scored
- **Real Job Data** - Live job postings from Adzuna API (Canadian market)
- **Explainable Results** - Every match includes a human-readable reason explaining the score

---

## Cost Breakdown

| Model | Cost per 1K Tokens | Estimated Total |
|-------|-------------------|-----------------|
| Llama 3.3 70B (Bedrock) | $0.00072 | ~$1 |
| Claude 3.5 Sonnet | $0.003 | ~$7+ |
| GPT-4 | $0.03 | ~$30+ |

The `limit` parameter in the API controls how many jobs are scored by the LLM, giving you direct cost control.

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `AWS_REGION` | Yes | AWS region for Bedrock (default: `us-east-1`) |
| `BEDROCK_MODEL_ID` | Yes | Bedrock model ID (`meta.llama3-3-70b-instruct-v1:0`) |
| `ADZUNA_APP_ID` | Yes | Adzuna API application ID |
| `ADZUNA_APP_KEY` | Yes | Adzuna API application key |
| `BACKEND_URL` | No | Backend URL for Streamlit (default: `http://127.0.0.1:8000`) |

---
## Resume Value

This project demonstrates:

- End-to-end GenAI system design
- LLM orchestration in production workflows
- API-driven architecture
- Docker-based deployment
- Prompt engineering for structured outputs
- Real-world data integration
- Explainable AI ranking systems

Built as a portfolio project for Junior AI / Applied ML / GenAI Engineer roles.
---

## 👤 Author

**Jasveen Singh Sahani**  
Junior AI / Applied ML / Generative AI Engineer  

🔗 LinkedIn: https://www.linkedin.com/in/jasveen-singh-sahani-92716b249/
💻 GitHub: https://github.com/jsahani9  

Open to new grad / junior AI & GenAI engineering opportunities (Canada).
---
## License

MIT



