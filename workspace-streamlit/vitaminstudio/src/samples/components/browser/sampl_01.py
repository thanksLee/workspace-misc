import streamlit as st
import uuid
from st_local_storage import st_local_storage as st_ls


def ls_set(k, v, key=None):
    # jdata = json.dumps(v, ensure_ascii=False)
    # st_js_blocking(f"sessionStorage.setItem('{k}', JSON.stringify({jdata}));", key)
    st_ls[k] = v


def ls_get(k, key=None):
    # return st_js_blocking(f"return JSON.parse(sessionStorage.getItem('{k}'));", key)
    return st_ls[k]


def ls_remove(k, key=None):
    # st_js_blocking(f"sessionStorage.removeItem('{k}');", key)
    del st_ls[k]


ss = st.session_state

if st.button('get session storage'):
    if "user_id" not in ss:
        ss.user_id = ls_get("user_id")
        st.write('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
        st.write(ss)

if st.button('se session storage'):
    if ss.get('user_id') is None:
        if "new_user_id" not in ss:
            ss.new_user_id = str(uuid.uuid4())
        ls_set("user_id", ss.new_user_id)
        ss.user_id = ss.new_user_id

if st.button('remove session storage'):
    ls_remove("user_id")
