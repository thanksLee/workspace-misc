from core.singletons.common_code_store import CommonCodeStore
from core.exceptions import CommonCodeValueError
import json


class BaseSchema:
    def to_dict(self) -> dict:
        """Convert the instance to a dictionary."""
        return self.__dict__

    def to_json(self) -> str:
        """Convert the instance to a JSON string."""
        return json.dumps(self.to_dict())

    def _common_code_exists(self, key: str, value: str) -> None:
        # 공통코드에 존재하는지 체크
        _items = CommonCodeStore.get_common_code_exists(key)

        if value not in _items:
            raise CommonCodeValueError()

    def _common_code_name(self, flg: int, key: str, value: str) -> str:
        ret_val = CommonCodeStore.get_common_code_name(flg, key, value)

        if ret_val is None or ret_val == '':
            raise CommonCodeValueError()

        return ret_val
