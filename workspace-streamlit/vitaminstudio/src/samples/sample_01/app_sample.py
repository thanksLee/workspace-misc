import streamlit as st

from sample_01.users.views.login_page import LoginPage
from sample_01.main.views.main_page import MainPage
from sample_01.users.views.cookie_test import CookiesTest
from sample_01.users.views.storage_test import StorageTest


def init():
    if st.session_state.get('login_in'):
        MainPage().render()
    else:
        LoginPage().render()
        st.divider()
        CookiesTest().render()
        st.divider()
        StorageTest().render()


if __name__ == '__main__':
    init()
