from threading import Lock
from typing import Optional, List

from common.schemas.vo.common_code import CommonCodeVO
from core.loggers.manager import app_logger
from core.exceptions import InstanceNotLoadError

from .meta import SingletonMeta


class CommonCodeStore(metaclass=SingletonMeta):
    _instance = None
    _lock = Lock()
    _app_logger = app_logger

    def __init__(self):
        self._common_codes = None  # 공통 코드를 저장하는 인스턴스 변수

    def initialize(self, common_codes: List[CommonCodeVO]):
        with self._lock:
            if self._common_codes is not None:
                self._app_logger.warning("CommonCodeStore is already initialized and cannot be re-initialized.")
                return
            if not common_codes:
                raise ValueError("Cannot initialize CommonCodeStore with empty codes.")
            self._common_codes = common_codes
            self._app_logger.debug("CommonCodeStore has been initialized with common codes.")

    def get_all_common_code(self) -> List['CommonCodeVO']:
        if self._common_codes is None:
            raise InstanceNotLoadError("CommonCodeStore is not initialized.")
        return self._common_codes

    def get_common_code_name(self, code_nm_flg: int, key_code: str, type_code: str) -> Optional[str]:
        common_codes = self.get_all_common_code()

        for code in common_codes:
            if code.key_cd == key_code and code.type_cd == type_code:
                if code_nm_flg == 1:
                    return code.cd_nm_1
                elif code_nm_flg == 2:
                    return code.cd_nm_2
        return None

    def get_common_codes_by_key(self, key_code: str) -> List['CommonCodeVO']:
        common_codes = self.get_all_common_code()
        filtered_codes = []

        for code in common_codes:
            if code.key_cd == key_code:
                filtered_codes.append(code)
            elif filtered_codes:
                break
        return filtered_codes

    def get_common_code_exists(self, key_code: str) -> List[str]:
        common_codes = self.get_all_common_code()
        filtered_codes = []

        for code in common_codes:
            if code.key_cd == key_code:
                filtered_codes.append(code.type_cd)
            elif filtered_codes:
                break
        return filtered_codes

    def clear_instance(self):
        with self._lock:
            self._common_codes = None
            self._app_logger.debug("CommonCodeStore instance has been cleared.")

    def is_initialized(self) -> bool:
        return self._common_codes is not None
