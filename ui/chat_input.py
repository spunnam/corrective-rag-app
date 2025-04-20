import asyncio
import time
import streamlit as st
from ui.utils_ui import reset_chat


def handle_chat_input(run_workflow):
    if prompt := st.chat_input("Ask a question about your documents..."):
        log_index = len(st.session_state.workflow_logs)
        st.session_state.messages.append(
            {"role": "user", "content": prompt, "log_index": log_index}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        if st.session_state.workflow:
            result_text, logs = asyncio.run(run_workflow(prompt))
            st.session_state.workflow_logs.append(logs)

            if log_index < len(st.session_state.workflow_logs):
                with st.expander("View Workflow Execution Logs", expanded=False):
                    st.code(st.session_state.workflow_logs[log_index], language="text")

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                words = result_text.split()
                for i, word in enumerate(words):
                    full_response += word + " "
                    message_placeholder.markdown(full_response + "▌")
                    if i < len(words) - 1:
                        time.sleep(0.08)
                message_placeholder.markdown(full_response)

            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )
