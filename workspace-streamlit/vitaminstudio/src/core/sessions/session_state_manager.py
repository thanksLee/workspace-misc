import streamlit as st


class SessionStateManager:
    @staticmethod
    def get_session_state(ss_key: str = None):
        if ss_key is None:
            return st.session_state
        else:
            return st.session_state.get(ss_key, None)

    @staticmethod
    def set_session_state(ss_key: str, ss_value: any):
        st.session_state[ss_key] = ss_value
