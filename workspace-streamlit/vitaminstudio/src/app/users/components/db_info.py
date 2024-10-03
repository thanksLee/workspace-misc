import streamlit as st

from core.sessions.schemas import CurrentDBConnDTO
from core.constants.global_enum import ServerType, SERVER_TYPE, SERVER_DB, ServerDB
from core.configs.base import local_db_config
from core.utilities.files import get_file_list
from core.utilities.misc import get_database_url

from ..schemas.dto.request import DBServerDTO
from ..controllers import UserController


class DBInfoForm:
    def __init__(self):
        self._server_type: str = ''
        self._db_type: str = ''
        self._db_url: str = ''
        self._db_conn_status: bool = False
        self._db_schema: str = ''

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
            elif self._db_type == ServerDB.POSTGRESQL.value:
                self.pg_form()
            elif self._db_type == ServerDB.ORACLE.value:
                self.oracle_form()
            return True

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
            self._db_url: str = get_database_url(self._db_type, f'{db_file_path}/{sqlite_db_list}')
            self.__build_db_conn()

    def oracle_form(self):
        pass

    def pg_form(self):
        pg_col_1, pg_col_2 = st.columns([3, 1])
        with pg_col_1:
            db_host = st.text_input(label='host', placeholder='host', label_visibility='collapsed')

        with pg_col_2:
            db_port = st.text_input(label='port', placeholder='port', label_visibility='collapsed')

        pg_col_3, pg_col_4, pg_col_5 = st.columns([2, 3, 2])

        with pg_col_3:
            db_user = st.text_input(label='user', placeholder='user', label_visibility='collapsed')

        with pg_col_4:
            db_pwd = st.text_input(label='password', placeholder='password', type='password', label_visibility='collapsed')

        with pg_col_5:
            db_schema = st.text_input(label='schema', placeholder='schema', label_visibility='collapsed')

        pg_col_6, pg_col_7 = st.columns([3, 1])

        with pg_col_6:
            db_name = st.text_input(label='database', placeholder='database', label_visibility='collapsed')

        with pg_col_7:
            conn_db = st.button(
                label=":factory: Connect DB",
                type="primary",
                use_container_width=True,
            )

        if conn_db:
            self._db_url = get_database_url(self._db_type, f'{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}')
            self._db_schema = db_schema
            self.__build_db_conn()

    def __build_db_conn(self):
        with st.spinner('VitaminStudio Table 및 데이터 생성중...'):
            db_conn_info = CurrentDBConnDTO(server_type=self._server_type,
                                            db_type=self._db_type,
                                            db_url=self._db_url,
                                            db_conn_status=False,
                                            db_schema=self._db_schema
                                            )

            user_controller = UserController(db_conn_info.db_url)
            ret_val = user_controller.handle_db_conn_click(db_conn_info)

            st.toast(ret_val, icon='🔥')
