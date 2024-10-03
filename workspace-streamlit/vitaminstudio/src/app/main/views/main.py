import streamlit as st

from core.sessions.session_state_manager import SessionStateManager
from core.constants.global_enum import MenuItem

from common.views import CommonView

from app.worddict.views.main import WordDictMainView
from app.modelqc.views.main import ModelQCMainView


class MainView(CommonView):
    def __init__(self, session_state_manager):
        super().__init__(session_state_manager)
        self._word_dict_main_page = WordDictMainView()
        self._model_qc_main_page = ModelQCMainView()
        self._current_menu_item = self._session_state_manager.get_session_state('current_menu_item')

    def _set_menu_item(self, menu_item: MenuItem):
        self._init_paging_info(menu_item.name)
        self._session_state_manager.set_session_state('current_menu_item', menu_item.name)

    def _init_paging_info(self, menu_item_name: str):
        if menu_item_name != self._current_menu_item:
            self._session_state_manager.set_session_state('current_paging_info', None)

    def dashboard(self):
        self._set_menu_item(MenuItem.MENU_0000)
        st.write('VitaminStudio - Dashboard')

    def word_dict_view(self):
        self._set_menu_item(MenuItem.MENU_0001)
        self._word_dict_main_page.word_dict_view()

    def term_dict_view(self):
        self._set_menu_item(MenuItem.MENU_0002)
        self._word_dict_main_page.term_dict_view()

    def domain_dict_view(self):
        self._set_menu_item(MenuItem.MENU_0003)
        self._word_dict_main_page.domain_dict_view()

    def model_analyze_view(self):
        self._set_menu_item(MenuItem.MENU_0004)
        self._model_qc_main_page.model_analyze_view()

    def model_compare_view(self):
        self._set_menu_item(MenuItem.MENU_0005)
        self._model_qc_main_page.model_compare_view()

    def model_specification_view(self):
        self._set_menu_item(MenuItem.MENU_0006)
        self._model_qc_main_page.model_specification_view()

    def model_audit_analyze_view(self):
        self._set_menu_item(MenuItem.MENU_0007)
        self._model_qc_main_page.model_audit_analyze_view()

    def settings(self):
        self._set_menu_item(MenuItem.MENU_0008)
        st.write('VitaminStudio - Settings')

    def logout(self):
        self._set_menu_item(MenuItem.MENU_0009)
        st.write('VitaminStudio - Logout')

    def lnb_menu(self):
        pages = {
            '🏠 Home': [st.Page(self.dashboard, icon='📈', title=MenuItem.MENU_0000.value)],
            '📟 데이터 표준화 관리': [
                st.Page(self.word_dict_view, icon='✏️', title=MenuItem.MENU_0001.value),
                st.Page(self.term_dict_view, icon='📰', title=MenuItem.MENU_0002.value),
                st.Page(self.domain_dict_view, icon='📇', title=MenuItem.MENU_0003.value),
            ],
            '📲 모델 품질 관리': [
                st.Page(self.model_analyze_view, icon='💣', title=MenuItem.MENU_0004.value),
                st.Page(self.model_compare_view, icon='🍻', title=MenuItem.MENU_0005.value),
                st.Page(self.model_specification_view, icon='📝', title=MenuItem.MENU_0006.value),
                st.Page(self.model_audit_analyze_view, icon='💉', title=MenuItem.MENU_0007.value),
            ],
            '🗻 기타': [
                st.Page(self.settings, icon='🔨', title=MenuItem.MENU_0008.value),
                st.Page(self.logout, icon='🚪', title=MenuItem.MENU_0009.value),
            ]
        }

        pg = st.navigation(pages)
        pg.run()

    def render(self):
        st.write('VitaminStudio - Main View')
        self.lnb_menu()
