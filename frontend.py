import streamlit as st
import requests

st.title("🧠 Text-to-SQL AI")

question = st.text_input("Ask a question about the database")

if st.button("Submit"):

    response = requests.post(
        "http://127.0.0.1:8000/ask",
        json={"question": question}
    )

    result = response.json()

    st.subheader("📌 Question")
    st.write(result["question"])

    st.subheader("🧾 Generated SQL")
    st.code(result["generated_sql"], language="sql")

    st.subheader("📊 Result")
    st.write(result["result"])

    st.subheader("📈 Metadata")
    st.write("Rows returned:", result["rows_returned"])
    st.write("Execution time:", result["execution_time_sec"], "seconds")