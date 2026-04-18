from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
import os

DB_PATH = "vectorstore"

def load_and_store(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(DB_PATH)

def get_answer(query):
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local(DB_PATH, embeddings)

    retriever = db.as_retriever()
    docs = retriever.get_relevant_documents(query)

    context = " ".join([d.page_content for d in docs])

    llm = ChatOpenAI(temperature=0)

    prompt = f"""
    Answer based on the context below:
    {context}

    Question: {query}
    """

    return llm.predict(prompt)
