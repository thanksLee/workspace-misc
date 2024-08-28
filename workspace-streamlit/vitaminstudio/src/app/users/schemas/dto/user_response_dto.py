from pydantic.dataclasses import dataclass
from common.schemas.dto.common_response_dto import CommonResponseDTO


@dataclass
class UserDetailSchema:
    user_id: str
    user_type_cd: str
    user_type_cd_nm: str
    login_status: bool = False

    def to_dict(self) -> dict:
        return self.__dict__


class UserResponseDTO(CommonResponseDTO):
    def __post_init__(self):
        # UserDetailSchema의 인스턴스를 생성하여 detail 필드에 추가
        if isinstance(self.detail, UserDetailSchema):
            # detail이 UserDetailSchema 타입인 경우 딕셔너리로 변환
            self.detail = self.detail.to_dict()
        else:
            raise ValueError("detail must be an instance of UserDetailSchema")
