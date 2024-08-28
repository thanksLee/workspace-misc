import streamlit as st

from worddict.views.worddict_main_view import WordDictMainView
from modelqc.views.modelqc_main_view import ModelQCMainView


class MainView:
    def __init__(self):
        self._word_dict_main_page = WordDictMainView()
        self._model_qc_main_page = ModelQCMainView()

    def settings(self):
        st.write('VitaminStudio - Settings')

    def logout(self):
        st.write('VitaminStudio - Logout')

    def lnb_menu(self):
        pages = {
            '📟 데이터 표준화 관리': [
                st.Page(self._word_dict_main_page.word_dict_view, icon='✏️', title='표준 단어 사전'),
                st.Page(self._word_dict_main_page.term_dict_view, icon='📰', title='표준 용어 사전'),
                st.Page(self._word_dict_main_page.domain_dict_view, icon='📇', title='표준 도메인 사전'),
            ],
            '📲 모델 품질 관리': [
                st.Page(self._model_qc_main_page.model_analyze_view, icon='💣', title='모델 분석'),
                st.Page(self._model_qc_main_page.model_compare_view, icon='🍻', title='모델 비교'),
                st.Page(self._model_qc_main_page.model_specification_view, icon='📝', title='모델 명세'),
                st.Page(self._model_qc_main_page.model_audit_analyze_view, icon='💉', title='감리 대응 분석'),
            ],
            '🗻 기타': [
                st.Page(self.settings, icon='🔨', title='설정'),
                st.Page(self.logout, icon='🚪', title='로그아웃'),
            ]
        }

        pg = st.navigation(pages)
        pg.run()

    def render(self):
        st.write('VitaminStudio - Main View')
        self.lnb_menu()
