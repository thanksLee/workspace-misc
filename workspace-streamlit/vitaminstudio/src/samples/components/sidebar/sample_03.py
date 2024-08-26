import streamlit as st


def page1():
    st.title("Second page")


def page2():
    st.title("Second page")


pg = st.navigation([
    st.Page(page1, title="First page", icon="🔥"),
    st.Page(page2, title="Second page", icon=":material/favorite:"),
])
pg.run()
