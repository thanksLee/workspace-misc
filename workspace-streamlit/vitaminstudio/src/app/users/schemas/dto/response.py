from pydantic import Field, field_validator
from pydantic.dataclasses import dataclass

from common.schemas.dto.response import CommonResponseDTO
from common.schemas import BaseSchema


@dataclass
class UserDetailSchema(BaseSchema):
    user_id: str = Field(title='사용자 아이디')
    user_type_cd: str = Field(title='사용자 유형 코드')
    user_type_cd_nm: str = Field(title='사용자 유형 코드 명')
    login_status: bool = Field(title='로그인 상태', default=False)

    def __post_init__(self):
        super().__init__()


class UserResponseDTO(CommonResponseDTO):
    def __post_init__(self):
        # UserDetailSchema의 인스턴스를 생성하여 detail 필드에 추가
        if isinstance(self.detail, UserDetailSchema):
            # detail이 UserDetailSchema 타입인 경우 딕셔너리로 변환
            self.detail = self.detail.to_dict()
        else:
            raise ValueError("detail must be an instance of UserDetailSchema")
