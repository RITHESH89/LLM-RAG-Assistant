import streamlit as st
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader

from utils import process_text, create_vectorstore
from components.sidebar import sidebar

load_dotenv()

st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title(" Advanced RAG Chatbot")

sidebar()

# Chat memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_files = st.file_uploader(
    " Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

@st.cache_resource
def build_db(files):
    all_text = ""

    for file in files:
        with open(file.name, "wb") as f:
            f.write(file.read())

        loader = PyPDFLoader(file.name)
        docs = loader.load()

        for doc in docs:
            all_text += doc.page_content

    chunks = process_text(all_text)
    return create_vectorstore(chunks)

if uploaded_files:
    db = build_db(uploaded_files)

    llm = ChatOpenAI(temperature=0)

    qa = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=db.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )

    st.success("✅ Documents processed!")

    query = st.text_input("💬 Ask your question:")

    if query:
        result = qa({
            "question": query,
            "chat_history": st.session_state.chat_history
        })

        answer = result["answer"]
        sources = result["source_documents"]

        # Save chat
        st.session_state.chat_history.append((query, answer))

        # Display answer
        st.markdown("### Answer")
        st.write(answer)

        # Show sources
        st.markdown("###  Sources")
        for i, doc in enumerate(sources):
            st.write(f"Source {i+1}:")
            st.write(doc.page_content[:200] + "...")

# Chat history UI
if st.session_state.chat_history:
    st.markdown("### 🕘 Chat History")
    for q, a in reversed(st.session_state.chat_history):
        st.write(f"**You:** {q}")
        st.write(f"**AI:** {a}")
