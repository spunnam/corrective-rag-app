import streamlit as st
import base64
import gc


def reset_chat():
    st.session_state.messages = []
    gc.collect()


def display_pdf(file, filename=None):
    st.markdown("### PDF Preview: ")
    if filename:
        st.markdown(filename)

    base64_pdf = base64.b64encode(file.read()).decode("utf-8")
    st.markdown(
        f"""<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="440px" type="application/pdf"></iframe>""",
        unsafe_allow_html=True,
    )
