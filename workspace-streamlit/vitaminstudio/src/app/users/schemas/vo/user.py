from pydantic import Field, field_validator, model_validator
from typing import Optional

from common.schemas.vo.base import BaseVO


class UserVO(BaseVO):
    login_pwd: str = Field(title='로그인 비밀번호')
    use_yn: str = Field(title='사용 여부')
    use_yn_nm: Optional[str] = Field(title='사용 여부 명', default=None)
    user_type_cd: str = Field(title='사용자 유형 코드')
    user_type_cd_nm: Optional[str] = Field(title='사용자 유형 코드 명', default=None)

    @field_validator('use_yn')
    def validate_user_yn(cls, value: str):
        cls._app_logger.debug(f"Validating 'use_yn': {value}")

        # 공통코드에 존재하는지 체크
        cls._common_code_exists('B01', value)

        return value

    @field_validator('user_type_cd')
    def validate_user_type_cd(cls, value: str):
        cls._app_logger.debug(f"Validating 'user_type_cd': {value}")

        # 공통코드에 존재하는지 체크
        cls._common_code_exists('B03', value)

        return value

    @model_validator(mode='after')
    def set_common_code_name(cls, values: 'UserVO'):
        cls._app_logger.debug(f"Values before modification: {values.model_dump()}")

        # use_yn_nm 값이 없을 경우 use_yn 값 기반으로 설정
        if values.use_yn_nm is None:
            values.use_yn_nm = cls._common_code_name(1, 'B01', values.use_yn)

        if values.user_type_cd_nm is None:
            values.user_type_cd_nm = cls._common_code_name(1, 'B03', values.user_type_cd)

        cls._app_logger.debug(f"Values after modification: {values.model_dump()}")
        return values
