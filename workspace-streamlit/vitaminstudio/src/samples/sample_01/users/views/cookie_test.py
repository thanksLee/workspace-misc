import streamlit as st
from streamlit_cookies_controller import CookieController


class CookiesTest:
    def __init__(self):
        self._controller = CookieController()

    def render(self):
        cookie_set_btn = st.button('Set Cookie')
        if cookie_set_btn:
            # Set a cookie
            self._controller.set('cookie_name', 'testing')

            cookie = self._controller.get('cookie_name')
            st.write(cookie)

        cookie_get_btn = st.button('Get Cookie')
        if cookie_get_btn:
            # Get all cookies
            cookies = self._controller.getAll()
            st.write(cookies)

            # Get a cookie
            cookie = self._controller.get('cookie_name')
            st.write(cookie)

        cookie_remove_btn = st.button('remove Cookie')
        if cookie_remove_btn:
            # Remove a cookie
            self._controller.remove('cookie_name')
