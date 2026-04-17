import streamlit as st
import os
from dotenv import load_dotenv
from utils import load_and_process, create_vector_store, create_qa_chain

load_dotenv()

st.set_page_config(page_title="RAG Assistant", layout="wide")

st.title(" LLM RAG Assistant")
st.write("Upload a PDF and ask questions from it!")

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("Processing document..."):
        chunks = load_and_process("temp.pdf")
        db = create_vector_store(chunks)
        qa = create_qa_chain(db)

    st.success("Document processed successfully!")

    query = st.text_input("Ask a question")

    if query:
        with st.spinner("Generating answer..."):
            response = qa.run(query)

        st.write("###  Answer:")
        st.write(response)
