from pydantic import BaseModel, Field, field_validator
from typing import Optional


class CurrentDBConnDTO(BaseModel):
    server_type: str = Field(..., example='local')
    db_type: str = Field(..., example='sqlite')
    db_url: str = Field(..., example='sqlite:///vitamin.db')
    db_conn_status: bool = Field(default=False, example=False)
    db_schema: Optional[str] = Field(default='public', example='public')

    # server_type 필드를 소문자로 변환하는 검증기 추가
    @field_validator('server_type', 'db_type', 'db_schema', mode='before')
    def lowercase_values(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v


class CurrentUserDTO(BaseModel):
    pass


class CurrentPageNavigationDTO(BaseModel):
    pass


class CurrentInfoDTO(BaseModel):
    db_conn: CurrentDBConnDTO
    user: CurrentUserDTO
