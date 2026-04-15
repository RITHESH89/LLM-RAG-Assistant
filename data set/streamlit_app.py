import streamlit as st
from utils import create_vectorstore
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

st.title(" RAG Assistant")

query = st.text_input("Ask something:")

if query:
    with open("data/sample.txt") as f:
        text = f.read()

    db = create_vectorstore(text)
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(),
        retriever=db.as_retriever()
    )

    st.write(qa.run(query))
