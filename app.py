import uuid
import io
import streamlit as st
from dotenv import load_dotenv
from contextlib import redirect_stdout

from ui.sidebar import sidebar_config
from ui.header import render_header
from ui.chat_display import show_chat_history
from ui.chat_input import handle_chat_input
from ui.utils_ui import reset_chat

# Load env + config
load_dotenv()
st.set_page_config(page_title="Corrective RAG Demo", layout="wide")

# Session state
if "id" not in st.session_state:
    st.session_state.id = uuid.uuid4()
    st.session_state.file_cache = {}
if "workflow" not in st.session_state:
    st.session_state.workflow = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "workflow_logs" not in st.session_state:
    st.session_state.workflow_logs = []

# Set reset function globally for button callback
st.session_state["reset_chat"] = reset_chat

# Sidebar: upload, API keys, init workflow
with st.sidebar:
    sidebar_config(st.session_state.id)


# Header: title and branding
render_header()

# Show message history + logs
show_chat_history()


# Chat input and assistant response
async def run_workflow(query):
    f = io.StringIO()
    with redirect_stdout(f):
        result = await st.session_state.workflow.run(query_str=query)
    logs = f.getvalue()
    return result, logs


handle_chat_input(run_workflow)
