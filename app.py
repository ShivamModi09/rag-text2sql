from fastapi import FastAPI
from pydantic import BaseModel
import time

from src.text_to_sql import ask_question

app = FastAPI()

class Query(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "Text-to-SQL API running"}


@app.post("/ask")
def ask(query: Query):

    start = time.time()  # start timer

    sql_query, answer = ask_question(query.question)

    execution_time = round(time.time() - start, 3)  # stop timer

    return {
        "question": query.question,
        "generated_sql": sql_query,
        "result": answer,
        "rows_returned": len(answer) if isinstance(answer, list) else 1,
        "execution_time_sec": execution_time
    }