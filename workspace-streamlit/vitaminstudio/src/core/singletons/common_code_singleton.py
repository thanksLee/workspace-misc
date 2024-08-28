from threading import Lock
from typing import Optional, List

from common.schemas.vo.common_code_vo import CommonCodeVO
from core.loggers.logger_manager import app_logger
from core.exceptions import InstanceNotLoadError


class CommonCodeSingleton:
    _instance = None
    _lock = Lock()
    _app_logger = app_logger

    @classmethod
    def get_instance(cls) -> List['CommonCodeVO']:
        with cls._lock:
            if cls._instance is None:
                raise InstanceNotLoadError("CommonCodeSingleton is not initialized. Call 'reset_instance' first.")
            return cls._instance

    @classmethod
    def reset_instance(cls, common_codes: List['CommonCodeVO']):
        with cls._lock:
            if cls._instance is not None:
                # raise Exception("CommonCodeSingleton is already initialized and cannot be re-initialized.")
                cls._app_logger.warning("CommonCodeSingleton is already initialized and cannot be re-initialized.")
            if not common_codes:
                raise ValueError("Cannot initialize CommonCodeSingleton with empty codes.")
            cls._instance = common_codes
            cls._app_logger.debug("CommonCodeSingleton has been initialized with common codes.")

    @classmethod
    def clear_instance(cls):
        with cls._lock:
            # This method should be used with caution
            cls._instance = None
            cls._app_logger.debug("CommonCodeSingleton instance has been cleared.")

    @classmethod
    def is_initialized(cls) -> bool:
        return cls._instance is not None

    @classmethod
    def get_all_common_code(cls) -> List['CommonCodeVO']:
        return cls.get_instance()

    @classmethod
    def get_common_code_name(cls, code_nm_flg: int, key_code: str, type_code: str) -> Optional[str]:
        common_codes = cls.get_all_common_code()

        for code in common_codes:
            if code.key_cd == key_code and code.type_cd == type_code:
                if code_nm_flg == 1:
                    return code.cd_nm_1
                elif code_nm_flg == 2:
                    return code.cd_nm_2
        return None

    @classmethod
    def get_common_codes_by_key(cls, key_code: str) -> List['CommonCodeVO']:
        common_codes = cls.get_all_common_code()
        filtered_codes = []

        for code in common_codes:
            if code.key_cd == key_code:
                filtered_codes.append(code)
            elif filtered_codes:
                break
        return filtered_codes
