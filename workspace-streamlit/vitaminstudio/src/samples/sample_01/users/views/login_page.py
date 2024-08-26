import streamlit as st


class LoginPage:
    def __init__(self):
        pass

    def render(self):
        st.write('VitaminStudio - Login')

        login_button = st.button('Login')

        if login_button:
            st.session_state['login_in'] = True
            st.rerun()
