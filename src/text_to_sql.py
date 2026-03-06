import os
from dotenv import load_dotenv

load_dotenv()

from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Connecting MySQL database
host = "localhost"
port = "3306"
username = "root"
password = os.getenv("SQL_PASSWORD")
database_schema = "text_to_sql"

mysql_uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_schema}"

db = SQLDatabase.from_uri(mysql_uri,sample_rows_in_table_info=1)
context = db.get_table_info()

# Create LLM Prompt template
from langchain_core.prompts import PromptTemplate

template = """
You are an expert SQL generator. INPUTS:
- Schema: {schema}
- Question: {question}

INSTRUCTIONS:
1. Produce **only one** valid MySQL query that answers the Question using the provided Schema.
2. Output **exactly one single-line** SQL statement (no line breaks).
3. Do **not** include any explanations, comments, notes, or surrounding code fences — only the SQL text.
4. Use table and column names exactly as given; do **not** invent columns or tables.
5. If the question cannot be answered from the schema, output a valid query that returns zero rows (for example: `SELECT NULL WHERE 1=0;`).
6. Prefer standard MySQL syntax and keep the query minimal and precise.

Now generate the single-line SQL for the provided inputs."""

prompt = PromptTemplate.from_template(template)

fix_template = """
You are an expert SQL debugger.

Schema:
{schema}

Question:
{question}

The following SQL query produced an error.

SQL:
{sql}

Error:
{error}

Fix the SQL query so it runs correctly using the schema.

Return ONLY the corrected single-line SQL query.
"""

fix_prompt = PromptTemplate.from_template(fix_template)

# get the schema of database
def get_schema(db):
    return db.get_table_info()


# Call the LLM
from langchain_google_genai import ChatGoogleGenerativeAI

GEMINI_API = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    api_key = GEMINI_API)

# Create the SQL query chain using the LLM and the prompt template
sql_chain = (
    RunnablePassthrough.assign(schema=lambda _: get_schema(db))
    | prompt
    | llm
    | StrOutputParser()
)

fix_chain = (
    RunnablePassthrough.assign(schema=lambda _: get_schema(db))
    | fix_prompt
    | llm
    | StrOutputParser()
)


# Basic SQL safety guardrail - allows only single SELECT queries
def validate_sql(query: str):    
    q = query.strip().upper()
    # Block multiple queries
    if ";" in q:
        raise ValueError("Multiple SQL statements are not allowed")
    # Block dangerous commands
    forbidden = ["DROP", "DELETE", "UPDATE", "ALTER", "TRUNCATE", "INSERT"]
    for word in forbidden:
        if word in q:
            raise ValueError(f"Unsafe SQL detected: {word}")
    # Allow only SELECT queries
    if not q.startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed")
    return query

def ask_question(question: str):
    result = sql_chain.invoke({"question": question})
    safe_query = validate_sql(result)
    try:
        answer = db.run(safe_query)
    # Self-Correction Loop (Agentic behavior)
    except Exception as e:
        fixed_sql = fix_chain.invoke({
            "question": question,
            "sql": safe_query,
            "error": str(e)
        })
        fixed_sql = validate_sql(fixed_sql)
        answer = db.run(fixed_sql)
        return fixed_sql, answer
    return result, answer