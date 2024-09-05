import streamlit as st
import pandas as pd
from typing import Optional


class WordDictListForm:
    def __init__(self, db_url: str):
        self._db_url = db_url

    def render(self, word_dict_values: Optional[list]):
        # list_header_container = st.container(border=True)
        # with list_header_container:
        #    pass
        self.load_word_dict_list(word_dict_values)

    def load_word_dict_list(self, values: Optional[list]):
        if values:
            # list_columes = values[0].keys
            # st.write(list_columes)
            df = pd.json_normalize(values)
            st.dataframe(df, hide_index=True)
