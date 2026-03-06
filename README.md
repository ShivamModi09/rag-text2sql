# Text to SQL RAG System

This project converts natural language questions into SQL queries using an LLM and retrieves answers from a database.

## Architecture

User

↓

Streamlit UI

↓

FastAPI Backend

↓

LangChain SQL Chain

↓

SQL Guardrail & Validation  

↓

SQL Self-Correction Loop  

↓

MySQL Database Execution  

↓

RAGAS Evaluation

## Tech Stack

* Python
* FastAPI
* Streamlit
* LangChain
* RAGAS
* Google Gemini & Groq (LLM)
* HuggingFace Embeddings
* MySQL

## Run Locally

### 1. Clone repository

git clone https://github.com/ShivamModi09/rag-text2sql.git  
cd rag-text2sql

### 2. Install dependencies

pip install -r requirements.txt

### 3. Create MySQL database

Create a database named:

text_to_sql

### 4. Import CSV data into MySQL

Import the CSV files from the `data/` folder into the database tables.

Example tables:
- products
- customers
- regions
- sales_order
- state_regions
- 2017_budgets

### 5. Run backend API

uvicorn app:app --reload

### 6. Run frontend UI

streamlit run frontend.py

## Example Question

"What is the budget for Product 12?"

The system converts the question into SQL and queries the database.

## Features

* Natural language → SQL generation
* SQL safety guardrail (blocks unsafe queries)
* Automatic SQL self-correction if query fails
* Database querying
* RAG evaluation using RAGAS
* Simple UI using Streamlit

# Evaluation

The system is evaluated using **RAGAS** to measure:

- Faithfulness
- Answer relevance
- Context precision
- Context recall

Run evaluation:

python ragas_evaluation.py

Example result:

{
 "maliciousness": 1.0,
 "helpfullness": 4.6,
 "context_precision": 0.8,
 "faithfulness": 0.8667
}

## Demo

![Demo](demo.gif)

# Author

Shivam Modi
