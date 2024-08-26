import streamlit as st


def page1():
    st.write(st.session_state.foo)


def page2():
    st.write(st.session_state.bar)
    st.divider()


def page3():
    st.write(st.session_state.bar)


# Widgets shared by all the pages
st.sidebar.selectbox("Foo", ["A", "B", "C"], key="foo")
st.sidebar.checkbox("Bar", key="bar")

pages = {
    "Your account": [st.Page(page1, title='page1'), st.Page(page2, title='page2')],
    "Resources": [st.Page(page3, title='page3')]
}

pg = st.navigation(pages)
pg.run()
