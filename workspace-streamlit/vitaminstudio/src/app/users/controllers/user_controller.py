from common.controllers.common_controller import CommonController

from core.databases.server.db_connection_manager import db_manager
from core.sessions.schemas.current_db_conn_schema import CurrentDBConnSchema

from ..services.user_init_service import UserInitService
from ..services.user_login_service import UserLoginService
from ..schemas.dto.user_request_dto import LoginFormDTO


class UserController(CommonController):
    def __init__(self, db_url: str):
        super().__init__(db_url)

    def db_initialize(self, db_conn_info: CurrentDBConnSchema):
        db_manager.add_db_manager(db_conn_info.db_type, db_conn_info.db_url)

    def sqlite_create_db(self, db_type: str):
        _user_init_service = UserInitService(self._tr_manager)
        qry_result = _user_init_service.sql_file_execute(db_type)

        return qry_result

    def user_login(self, user_form: LoginFormDTO):
        ret_val = UserLoginService(self._tr_manager).user_login_check(user_form)
        return ret_val
