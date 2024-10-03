import streamlit as st
from pydantic import ValidationError
from typing import Optional

from core.sessions.session_state_manager import SessionStateManager
from core.sessions.schemas import CurrentDBConnDTO

from ..controllers import UserController
from ..schemas.dto.request import LoginFormDTO


class LoginForm:
    def __init__(self):
        self._login_id = ""
        self._login_pwd = ""
        self._session_state_manager = SessionStateManager
        self._current_db_conn = self._session_state_manager.get_session_state('current_db_conn')

    def render(self):
        with st.form(key='vitamin_login_form'):
            self._login_id = st.text_input(label='Login ID')
            self._login_pwd = st.text_input(label='Login Password', type='password')

            db_conn_info = self._get_db_conn_info()

            btn_col1, btn_col2 = st.columns([4, 1])
            with btn_col1:
                st.caption('')

            with btn_col2:
                submit_btn = st.form_submit_button('⚡️ Login', use_container_width=True)

            if submit_btn:
                self._handle_login(db_conn_info)

    def _get_db_conn_info(self) -> Optional[CurrentDBConnDTO]:
        ret_val: CurrentDBConnDTO = None
        if self._current_db_conn is not None:
            ret_val = CurrentDBConnDTO(
                server_type=self._current_db_conn['server_type'],
                db_type=self._current_db_conn['db_type'],
                db_url=self._current_db_conn['db_url'],
                db_conn_status=self._current_db_conn['db_conn_status']
            )
        return ret_val

    def _handle_login(self, db_conn_info: CurrentDBConnDTO):
        if db_conn_info is None:
            st.error(":boom: VitaminStudio DB에 접속되지 않았습니다.")
        else:
            # 입력값 유효성 검사
            try:
                with st.spinner('VitaminStudio에 로그인 중입니다.'):
                    user_controller = UserController(db_conn_info.db_url)

                    # 키워드 인자를 사용하여 Pydantic 모델 인스턴스화
                    user_form = LoginFormDTO(login_id=self._login_id, login_pwd=self._login_pwd)

                    ret_val = user_controller.handle_user_login_click(user_form)

                    if ret_val['status'] == 200:
                        st.info(ret_val['message'])

                        # 메인 페이지를 다시 렌더링하기 위해 페이지를 리로드합니다.
                        st.rerun()
                    else:
                        st.error(ret_val['message'])

            except ValidationError as ve:
                # pydantic 유효성 검사 오류 처리
                for error in ve.errors():
                    # st.error(f"입력 오류: {error['loc'][0]} - {error['msg']}")
                    st.toast(f"입력 오류: {error['loc'][0]} - {error['msg']}", icon="🚨")
