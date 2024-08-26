import streamlit as st

from sample_01.worddict.views.worddict_main_page import WordDictMainPage
from sample_01.worddict.views.termdict_main_page import TermDictMainPage
from sample_01.worddict.views.domaindict_main_page import DomainDictMainPage
from sample_01.modelqc.views.model_analyze_main_page import ModelAnalyzeMainPage
from sample_01.modelqc.views.model_compare_main_page import ModelCompareMainPage
from sample_01.modelqc.views.model_specification_main_page import ModelSpecificationMainPage
from sample_01.modelqc.views.model_audit_analyze_main_page import ModelAuditAnalyzeMainPage


class MainPage:
    def __init__(self):
        pass

    def word_dict_main_page(self):
        WordDictMainPage().render()

    def term_dict_main_page(self):
        TermDictMainPage().render()

    def domain_dict_main_page(self):
        DomainDictMainPage().render()

    def model_analyze_main_page(self):
        ModelAnalyzeMainPage().render()

    def model_compare_main_page(self):
        ModelCompareMainPage().render()

    def model_specification_main_page(self):
        ModelSpecificationMainPage().render()

    def model_audit_analyze_main_page(self):
        ModelAuditAnalyzeMainPage().render()

    def settings(self):
        st.write('VitaminStudio - Settings')

    def logout(self):
        st.write('VitaminStudio - Logout')

    def render(self):
        st.write('VitaminStudio - Main')

        pages = {
            '데이터 표준화 관리': [
                st.Page(self.word_dict_main_page, title='표준 단어 사전'),
                st.Page(self.term_dict_main_page, title='표준 용어 사전'),
                st.Page(self.domain_dict_main_page, title='표준 도메인 사전'),
            ],
            '모델 품질 관리': [
                st.Page(self.model_analyze_main_page, title='모델 분석'),
                st.Page(self.model_compare_main_page, title='모델 비교'),
                st.Page(self.model_specification_main_page, title='모델 명세'),
                st.Page(self.model_audit_analyze_main_page, title='감리 대응 분석'),
            ],
            '----------------------': [
                st.Page(self.settings, title='설정'),
                st.Page(self.logout, title='로그아웃'),
            ]
        }

        pg = st.navigation(pages)
        pg.run()
