import streamlit as st

from sample_01.worddict.views.worddict_page import WordDictPage
from sample_01.worddict.views.termdict_page import TermDictPage
from sample_01.worddict.views.domaindict_page import DomainDictPage


class WordDictMainPage:
    def __init__(self):
        pass

    def word_dict_page(self):
        WordDictPage().render()

    def term_dict_page(self):
        TermDictPage().render()

    def domain_dict_page(self):
        DomainDictPage().render()

    def render(self):
        st.write('VitaminStudio - Worddict Main')
