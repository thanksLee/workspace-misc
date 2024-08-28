import streamlit as st

from .worddict_view import WordDictView
from .termdict_view import TermDictView
from .domaindict_view import DomainDictView


class WordDictMainView:
    def __init__(self):
        pass

    def word_dict_view(self):
        WordDictView().render()

    def term_dict_view(self):
        TermDictView().render()

    def domain_dict_view(self):
        DomainDictView().render()

    def render(self):
        st.write('VitaminStudio - Worddict Main')
