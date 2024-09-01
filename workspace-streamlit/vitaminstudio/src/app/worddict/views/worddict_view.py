import streamlit as st


from core.sessions.session_state_manager import SessionStateManager

from ..components.word_dict_filter_form import WordDictFilterForm
from ..components.word_ditc_list_form import WordDictListForm


class WordDictView:
    def __init__(self):
        self._session_state_manager = SessionStateManager
        self._current_db_conn = self._session_state_manager.get_session_state('current_db_conn')
        self._db_url = self._current_db_conn['db_url']

    def render(self):
        st.write('VitaminStudio - Worddict Main')

        if self._current_db_conn is not None:
            ret_val = WordDictFilterForm(self._db_url).render()
            WordDictListForm(self._db_url).render(ret_val)

            # self._list_form()
