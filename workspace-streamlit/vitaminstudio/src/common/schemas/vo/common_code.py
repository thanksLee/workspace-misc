from pydantic import BaseModel, Field, model_validator
from typing import Optional


class CommonCodeVO(BaseModel):
    key_cd: str = Field(..., examples='B01')
    type_cd: str = Field(..., examples='Y')
    cd_nm_1: str = Field(..., examples='사용')
    cd_nm_2: Optional[str] = Field(default=None)
    use_yn: str = Field(default="Y", pattern=r"^[YN]$")
    dspy_yn: str = Field(default="Y", pattern=r"^[YN]$")
    sort_order: int = Field(..., examples=1)
    dspy_cd_nm_1: Optional[str] = Field(default=None)
    dspy_cd_nm_2: Optional[str] = Field(default=None)

    class Config:
        from_attributes = True  # 기존 orm_mode의 대체
        # allow_mutation이 기본적으로 False로 설정되므로 더 이상 필요하지 않음

    @property
    def full_code_name(self) -> str:
        return f"{self.type_cd}-{self.key_cd}-{self.cd_nm_1}"

    @model_validator(mode="after")
    def set_display_code_nm(cls, values: 'CommonCodeVO'):
        type_cd = values.type_cd
        cd_nm_1 = values.cd_nm_1
        cd_nm_2 = values.cd_nm_2

        if type_cd == '-':
            type_cd = '0'
            cd_nm_1 = '전체'
            cd_nm_2 = '전체'

        values.dspy_cd_nm_1 = f'{type_cd}:{cd_nm_1}'
        values.dspy_cd_nm_2 = f'{type_cd}:{cd_nm_2}'

        return values

    def to_dict(self) -> dict:
        """Convert the instance to a dictionary."""
        return self.__dict__
