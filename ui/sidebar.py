import os
import tempfile
import streamlit as st
from core.vector_store import (
    init_vector_store,
    init_embedding_model,
    create_index_from_documents,
)
from core.pdf_ingestion import load_documents_from_directory
from core.utils import load_llm
from core.workflow import CorrectiveRAGWorkflow
from ui.utils_ui import display_pdf


def sidebar_config(session_id):
    st.header("RAG Config")
    st.markdown(
        "[Get your Linkup API key](https://app.linkup.so/sign-up)",
        unsafe_allow_html=True,
    )

    # Inputs
    linkup_api_key = st.text_input("Linkup API Key", type="password")
    groq_api_key = st.text_input("Groq API Key", type="password")

    # Store API keys
    if linkup_api_key:
        os.environ["LINKUP_API_KEY"] = linkup_api_key
        st.success("Linkup API Key stored successfully.")
    if groq_api_key:
        os.environ["GROQ_API_KEY"] = groq_api_key
        st.success("Groq API Key stored successfully.")

    # File Upload
    st.header("Upload your document")
    uploaded_file = st.file_uploader("Choose your `.pdf` file", type="pdf")

    if uploaded_file:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            file_key = f"{session_id}-{uploaded_file.name}"

            if file_key not in st.session_state.get("file_cache", {}):
                documents = load_documents_from_directory(temp_dir)
                vector_store = init_vector_store()
                init_embedding_model()
                index = create_index_from_documents(documents, vector_store)
                llm = load_llm(os.getenv("GROQ_API_KEY"))
                workflow = CorrectiveRAGWorkflow(index=index, llm=llm)
                st.session_state.workflow = workflow
                st.session_state.file_cache[file_key] = workflow
            else:
                st.session_state.workflow = st.session_state.file_cache[file_key]

            st.success("Ready to Chat!")
            display_pdf(uploaded_file, uploaded_file.name)
