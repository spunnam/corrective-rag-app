import streamlit as st
import base64


def render_header():
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown(
            "<h2 style='color: #0066cc;'>⚙️ Corrective RAG agentic workflow</h2>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div style='display: flex; align-items: center; gap: 10px;'>"
            "<span style='font-size: 28px; color: #666;'>Powered by LlamaIndex</span>"
            "<img src='data:image/png;base64,{}' width='50'></div>".format(
                base64.b64encode(open("./assets/llamaindex.png", "rb").read()).decode()
            ),
            unsafe_allow_html=True,
        )
    with col2:
        st.button("Clear ↺", on_click=st.session_state.get("reset_chat", lambda: None))
