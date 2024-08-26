import streamlit as st

from sample_01.users.views.login_page import LoginPage
from sample_01.main.views.main_page import MainPage


def init():
    if st.session_state.get('login_in'):
        MainPage().render()
    else:
        LoginPage().render()


if __name__ == '__main__':
    init()
