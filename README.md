# 📊 rag-text2sql

**AI-Powered Natural Language to SQL with Self-Correction**

![rag-text2sql Demo](demo.gif)

rag-text2sql is a high-performance RAG system that converts natural language questions into validated, self-correcting SQL queries. It bridges the gap between non-technical users and databases by generating precise SQL, applying safety checks, automatically fixing errors, and returning accurate database-backed answers through a production-ready FastAPI, Streamlit, LangChain, RAGAS, and MySQL setup.

---

## Architecture

```text
[ User ] ──▶ [ Streamlit UI ] ──▶ [ FastAPI Backend ]
                                         │
    ┌────────────────────────────────────┘
    ▼
[ LangChain SQL Chain ] ──▶ [ SQL Guardrail ] ──▶ [ Self-Correction Loop ]
                                                         │
    ┌────────────────────────────────────────────────────┘
    ▼
[ MySQL Database ] ──▶ [ RAGAS Evaluation ] ──▶ [ Final Answer ]
```

---

## Tech Stack

| Component        | Technology             |
| ---------------- | ---------------------- |
| Language         | Python 3.11            |
| Backend API      | FastAPI, Uvicorn       |
| Frontend UI      | Streamlit              |
| Orchestration    | LangChain              |
| LLMs             | Google Gemini & Groq   |
| Database	   | MySQL 8.0 & Workbench  |
| Evaluation       | RAGAS                  |
| Containerization | Docker, Docker Compose |

---

## Key Features

* Natural language to SQL generation
* SQL safety guardrail to block unsafe queries
* Automatic SQL self-correction if a query fails
* Real database execution with MySQL
* RAG-based evaluation using RAGAS
* Simple Streamlit-based interface
* Multi-stage Docker setup for cleaner deployment

---

## Project Structure

```text
rag-text2sql/
├── app.py              # FastAPI backend
├── frontend.py         # Streamlit UI
├── src/                # Core logic and SQL chains
├── data/               # DB schema and CSV files
│   ├── init.sql
│   └── *.csv
├── Dockerfile          # Multi-stage build
├── docker-compose.yml  # Service orchestration
├── requirements.txt    # Project Dependencies
├── .env.example
├── README.md
└── .dockerignore
```

---

## How to run

### Option 1: Run with Docker (Recommended)

Use this to launch the full stack: database + API + UI.

```bash
git clone https://github.com/ShivamModi09/rag-text2sql.git
cd rag-text2sql
cp .env.example .env
# Add your API keys to .env
docker compose up -d
```

**Open:**

* UI: `http://localhost:8501`
* API Docs: `http://localhost:8000/docs`

### Option 2: Run locally for development

```bash
# use python 3.11 version
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt 
uvicorn app:app --reload 
streamlit run frontend.py 
```

### After making changes

```bash
docker compose up -d --build
```

### Stop the app

```bash
docker compose down
```

---

## Evaluation

The system is evaluated using **RAGAS** to measure:

* Faithfulness
* Answer relevance
* Context precision
* Context recall

Run evaluation:

```bash
python ragas_evaluation.py
```

Example result:

```json
{
  "maliciousness": 1.0,
  "helpfulness": 4.6,
  "context_precision": 0.8,
  "faithfulness": 0.8667
}
```

---

## Docker / Deployment Highlights

This project uses a **multi-stage build** strategy to optimize cloud deployment and local performance:

* CPU-only optimization to avoid unnecessary GPU drivers
* Pre-seeded MySQL database with schema and source data
* Smaller final image through multi-stage layering
* Final image reduced from **2.1GB** to **516MB**

---

## Author

**Shivam Modi**

Software Developer
