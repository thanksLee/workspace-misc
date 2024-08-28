import streamlit as st

from sample_01.worddict.views.worddict_main_page import WordDictMainPage
from sample_01.modelqc.views.modelqc_main_page import ModelQCMainPage


class MainPage:
    def __init__(self):
        self._word_dict_main_page = WordDictMainPage()
        self._model_qc_main_page = ModelQCMainPage()

    def settings(self):
        st.write('VitaminStudio - Settings')

    def logout(self):
        st.write('VitaminStudio - Logout')

    def lnb_menu(self):
        pages = {
            '📟 데이터 표준화 관리': [
                st.Page(self._word_dict_main_page.word_dict_page, icon='✏️', title='표준 단어 사전'),
                st.Page(self._word_dict_main_page.term_dict_page, icon='📰', title='표준 용어 사전'),
                st.Page(self._word_dict_main_page.domain_dict_page, icon='📇', title='표준 도메인 사전'),
            ],
            '📲 모델 품질 관리': [
                st.Page(self._model_qc_main_page.model_analyze_page, icon='💣', title='모델 분석'),
                st.Page(self._model_qc_main_page.model_compare_page, icon='🍻', title='모델 비교'),
                st.Page(self._model_qc_main_page.model_specification_page, icon='📝', title='모델 명세'),
                st.Page(self._model_qc_main_page.model_audit_analyze_page, icon='💉', title='감리 대응 분석'),
            ],
            '🗻 기타': [
                st.Page(self.settings, icon='🔨', title='설정'),
                st.Page(self.logout, icon='🚪', title='로그아웃'),
            ]
        }

        pg = st.navigation(pages)
        pg.run()

    def render(self):
        st.write('VitaminStudio - Main')
        self.lnb_menu()
