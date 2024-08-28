import streamlit as st

from core.sessions.schemas.current_db_conn_schema import CurrentDBConnSchema
from core.constants.global_enum import ServerType, SERVER_TYPE, SERVER_DB, ServerDB
from core.configs.configs import local_db_config
from core.utilities.files import get_file_list
from core.utilities.misc import get_database_url

from ..schemas.dto.user_dto import DBServerDTO
from ..controllers.user_controller import UserController


class DBInfoForm:
    def __init__(self):
        self._server_type: str = ''
        self._db_type: str = ''
        self._db_url: str = ''
        self._db_conn_status: bool = False

    def render(self) -> DBServerDTO:
        with st.expander(label="VitaminStudio DB Info", expanded=True):
            db_con_col1, db_con_col2 = st.columns(2)

            with db_con_col1:
                self._server_type = st.selectbox(
                    "Selected Server",
                    SERVER_TYPE,
                    index=0,
                    label_visibility="collapsed"
                )

            with db_con_col2:
                self._db_type = st.selectbox(
                    "Selected Database",
                    SERVER_DB[0:1] if self._server_type == ServerType.LOCAL.value else SERVER_DB[1:],
                    index=0,
                    label_visibility="collapsed"
                )

            if self._db_type == ServerDB.SQLITE.value:
                # VitaminStudio table 생성
                self.sqlite_form()

            return DBServerDTO(server_type=self._server_type, db_type=self._db_type)

    def sqlite_form(self):
        sqlite_col1, sqlite_col2, sqlite_col3 = st.columns([2, 1, 1])

        db_list = get_file_list(local_db_config.db_path)
        with sqlite_col1:
            db_file_path = st.text_input(
                label="Database file path",
                value=local_db_config.db_path,
                disabled=True,
                label_visibility="collapsed"
            )
        with sqlite_col2:
            sqlite_db_list = st.selectbox(
                "Selected Database",
                db_list,
                index=0,
                label_visibility="collapsed"
            )

        with sqlite_col3:
            conn_db = st.button(
                label=":factory: Connect DB",
                type="primary",
                use_container_width=True,
            )

        if conn_db:
            with st.spinner('VitaminStudio Table 및 데이터 생성중...'):
                self._db_url: str = get_database_url(self._db_type, f'{db_file_path}/{sqlite_db_list}')

                db_conn_info = CurrentDBConnSchema(server_type=self._server_type,
                                                   db_type=self._db_type,
                                                   db_url=self._db_url,
                                                   db_conn_status=False
                                                   )
                user_controller = UserController(db_conn_info, initialize=True)

                ret_val = user_controller.sqlite_create_db()
                st.toast(ret_val, icon='🔥')

    def oracle_form(self, db_type: str):
        pass

    def pg_form(self, db_type: str):
        pass
