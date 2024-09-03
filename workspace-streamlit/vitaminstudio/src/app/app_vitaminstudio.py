import streamlit as st

from core.databases.local.local_db_manager import local_db_manager
from core.constants.global_enum import ProductInfo
from core.sessions.session_state_manager import SessionStateManager
from core.loggers.logger_manager import app_logger
from core.constants.global_const import CURRENT_USER, CURRENT_DB_CONN

from app.main.views.main_view import MainView
from app.users.views.login_view import LoginView

# 페이지 설정: 탭 이름과 favicon을 설정
st.set_page_config(
    page_title=f"{ProductInfo.NAME.value} {ProductInfo.VERSION.value}",  # 브라우저 탭에 표시될 이름
    page_icon="💊",                # 브라우저 탭에 표시될 아이콘 (이모지나 이미지 URL)
)


class AppVitaminStudio:
    def __init__(self):
        self._session_state_manager = SessionStateManager()
        self._app_logger = app_logger

    def setup_local_db(self):
        """ 로컬 데이터베이스를 설정하는 함수 """
        try:
            local_db_manager.create_local_db()
            local_db_manager.local_db_conn()
        except Exception as e:
            raise RuntimeError(f"Local database setup failed: {str(e)}")

    def render_login_page(self):
        """ 로그인 페이지를 렌더링하는 함수 """
        login_page = st.Page(LoginView().render, title=f'{ProductInfo.TITLE.value} {ProductInfo.VERSION.value}')
        page = st.navigation([login_page])
        page.run()

    def render_main_pages(self):
        """ 로그인 후 사이드바에 페이지를 렌더링하는 함수 """
        home_page = st.Page(MainView().render, title="VitaminStudio - Main")

        page = st.navigation([home_page])
        page.run()

    def handle_exception(self, ex):
        """ 예외 처리 로직 """
        if 'VS_ERROR' in str(ex):
            st.error(ex)
        elif 'VS_WARNING' in str(ex):
            st.warning(ex)
        elif 'VS_SUCCESS' in str(ex):
            st.info(ex)
        else:
            st.error('Application Error!!')
            self._app_logger.error(ex)  # 로깅 목적
            st.write(ex)  # 세부 오류 출력 (개발자용)

    def init(self):
        """ 초기화 함수 """
        try:
            _current_user = self._session_state_manager.get_session_state(CURRENT_USER)
            _current_db_conn = self._session_state_manager.get_session_state(CURRENT_DB_CONN)

            if _current_user is None:
                if _current_db_conn is None:
                    self.setup_local_db()
                self.render_login_page()
            else:
                self.render_main_pages()
            # 세션 상태 디버그 출력 (필요한 경우)
            st.write(self._session_state_manager.get_session_state())
        except Exception as ex:
            self.handle_exception(ex)
            st.stop()


if __name__ == "__main__":
    AppVitaminStudio().init()
