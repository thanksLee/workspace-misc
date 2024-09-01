from pydantic import BaseModel

from common.schemas.base_schema import BaseSchema
from core.loggers.logger_manager import app_logger
from core.singletons.common_code_store import CommonCodeStore
from core.exceptions import CommonCodeValueError


class BaseVO(BaseSchema, BaseModel):
    def __init_subclass__(cls):
        super().__init_subclass__()
        cls._app_logger = app_logger

    @classmethod
    def _common_code_exists(cls, key: str, value: str) -> None:
        # 공통코드에 존재하는지 체크
        _items = CommonCodeStore().get_common_code_exists(key)

        if value not in _items:
            raise CommonCodeValueError()

    @classmethod
    def _common_code_name(cls, flg: int, key: str, value: str) -> str:
        ret_val = CommonCodeStore().get_common_code_name(flg, key, value)

        if ret_val is None or ret_val == '':
            raise CommonCodeValueError()

        return ret_val
