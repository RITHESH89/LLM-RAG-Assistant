import streamlit as st

def sidebar():
    st.sidebar.title("⚙️ Settings")

    st.sidebar.markdown("###  About")
    st.sidebar.info(
        "Upload PDFs and ask questions.\n"
        "Uses RAG (Retrieval-Augmented Generation)."
    )

    if st.sidebar.button(" Clear Chat"):
        st.session_state.chat_history = []
