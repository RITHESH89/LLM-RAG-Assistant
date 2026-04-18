import streamlit as st
import requests

st.set_page_config(page_title="RAG Assistant")

st.title(" LLM RAG Assistant")

# Upload PDF
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    files = {"file": uploaded_file.getvalue()}
    res = requests.post("http://127.0.0.1:8000/upload", files=files)
    st.success(res.json()["message"])

# Ask Question
query = st.text_input("Ask a question")

if st.button("Get Answer"):
    response = requests.post(
        "http://127.0.0.1:8000/ask",
        json={"question": query}
    )
    st.write(response.json()["answer"])
