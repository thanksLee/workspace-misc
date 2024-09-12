import streamlit as st


from common.components.page_navigation import CommonPageNavigation
from core.sessions.session_state_manager import SessionStateManager

from ..components.filter import WordDictFilterForm
from ..components.list import WordDictListForm


class WordDictView:
    def __init__(self):
        self._session_state_manager = SessionStateManager
        self._current_db_conn = self._session_state_manager.get_session_state('current_db_conn')
        self._db_url = self._current_db_conn['db_url']

    def render(self):
        st.write('VitaminStudio - Worddict Main')

        if self._current_db_conn is not None:
            word_dict_filter_form = WordDictFilterForm(self._db_url)
            word_dict_filter_form.render()
            ret_val = word_dict_filter_form.handle_search()
            WordDictListForm(self._db_url).render(ret_val)

            if len(ret_val) > 0:
                total_cnt = ret_val[0]["total_cnt"]
                CommonPageNavigation(self._session_state_manager, total_cnt).render()

            # self._list_form()
