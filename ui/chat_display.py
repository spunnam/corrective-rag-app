import streamlit as st


def show_chat_history():
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

        # Attach logs for user messages, if any
        if (
            message["role"] == "user"
            and "log_index" in message
            and i < len(st.session_state.messages) - 1
        ):
            log_index = message["log_index"]
            if log_index < len(st.session_state.workflow_logs):
                with st.expander("View Workflow Execution Logs", expanded=False):
                    st.code(st.session_state.workflow_logs[log_index], language="text")
