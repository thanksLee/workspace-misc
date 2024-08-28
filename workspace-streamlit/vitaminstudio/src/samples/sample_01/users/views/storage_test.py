import streamlit as st
import json
import uuid
from typing import Any

from sample_01.users.st_local_storage import st_local_storage as st_ls


class StorageTest:
    def __init__(self):
        pass

    def ls_get(self, k, key=None):
        # return st_js_blocking(f"return JSON.parse(sessionStorage.getItem('{k}'));", key)
        return st_ls.get(key)

    def ls_set(self, k, v, key=None):
        # jdata = json.dumps(v, ensure_ascii=False)
        # st_js_blocking(f"sessionStorage.setItem('{k}', JSON.stringify({jdata}));", key)
        st_ls.set(k, v)

    def ls_remove(self, k, key=None):
        # st_js_blocking(f"sessionStorage.removeItem('{k}');", key)
        del st_ls[k]

    def render(self):
        storage_set_btn = st.button('Set Storage')
        if storage_set_btn:
            st.write(st.session_state)
            self.ls_set('storage_name', 'testing')

        storage_get_btn = st.button('Get Storage')
        if storage_get_btn:
            st.write(st.session_state)
            abcd = self.ls_get('storage_name')
            st.session_state['storage_name'] = abcd
            st.write(st.session_state)

        storage_remove_btn = st.button('Remove Storage')
        if storage_remove_btn:
            self.ls_remove('storage_name')

        st.divider()

        test_btn = st.button('session storage test')
        if test_btn:
            ss = st.session_state
            st.write(f'jjjjjjjjjjjjjj : {ss}')
            if ss.get('user_id') is None:
                if "new_user_id" not in ss:
                    ss.new_user_id = str(uuid.uuid4())
                self.ls_set("user_id", ss.new_user_id)
                ss.user_id = ss.new_user_id

            if "user_id" not in ss:
                abcd = self.ls_get("user_id")

                st.write(f'asdfasdfadf : {abcd}')

            st.write(ss)
