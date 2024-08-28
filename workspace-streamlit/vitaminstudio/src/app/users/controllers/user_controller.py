from common.controllers.common_controller import CommonController

from core.databases.server.db_connection_manager import db_manager
from core.sessions.schemas.current_db_conn_schema import CurrentDBConnSchema

from ..services.user_init_service import UserInitService
from ..services.user_login_service import UserLoginService
from ..schemas.dto.user_dto import LoginFormDTO


class UserController(CommonController):
    def __init__(self, db_conn_info: CurrentDBConnSchema, initialize: bool | None = False):

        # 최초 DB 접속을 하는 거라면...
        if initialize:
            db_manager.add_db_manager(db_conn_info.db_type, db_conn_info.db_url)

        super().__init__(db_conn_info.db_type)

        # Server로 접속하여 Database 및 Table을 생성하는 것이므로
        # 새로운 DB Connection을 한다.
        self._db_conn_info: CurrentDBConnSchema = db_conn_info

        self._user_init_service = UserInitService(self._tr_manager)

    def sqlite_create_db(self):
        qry_result = self._user_init_service.sql_file_execute(self._db_conn_info.db_type)

        return qry_result

    def user_login(self, user_form: LoginFormDTO):
        ret_val = UserLoginService(self._tr_manager).user_login_check(user_form)
        return ret_val
