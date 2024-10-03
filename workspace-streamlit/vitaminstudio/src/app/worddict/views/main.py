import streamlit as st

from core.sessions.session_state_manager import SessionStateManager

from .word_dict import WordDictView
from .term_dict import TermDictView
from .domain_dict import DomainDictView


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
