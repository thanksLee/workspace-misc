from pydantic import field_validator, model_validator
from typing import Optional
from common.schemas.vo.base_vo import BaseVO
from core.singletons.common_code_singleton import CommonCodeSingleton


class UserVO(BaseVO):
    login_pwd: str
    use_yn: str
    use_yn_nm: Optional[str] = None
    user_type_cd: str
    user_type_cd_nm: Optional[str] = None

    @field_validator('user_type_cd')
    def validate_user_type_cd(cls, value: str):
        cls._app_logger.debug(f"Validating 'user_type_cd': {value}")
        return value

    @model_validator(mode='after')
    def set_use_yn_nm(cls, values: 'UserVO'):
        cls._app_logger.debug(f"Values before modification: {values.model_dump()}")

        # use_yn_nm 값이 없을 경우 use_yn 값 기반으로 설정
        if values.use_yn_nm is None:
            values.use_yn_nm = CommonCodeSingleton.get_common_code_name(1, 'B01', values.use_yn)

        if values.user_type_cd_nm is None:
            values.user_type_cd_nm = CommonCodeSingleton.get_common_code_name(1, 'B03', values.user_type_cd)

        cls._app_logger.debug(f"Values after modification: {values.model_dump()}")
        return values
