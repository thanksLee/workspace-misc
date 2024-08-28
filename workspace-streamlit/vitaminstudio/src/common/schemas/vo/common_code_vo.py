from pydantic import BaseModel, Field
from typing import Optional


class CommonCodeVO(BaseModel):
    key_cd: str = Field(..., examples='B01')
    type_cd: str = Field(..., examples='Y')
    cd_nm_1: str = Field(..., examples='사용')
    cd_nm_2: Optional[str] = None
    use_yn: str = Field(default="Y", pattern=r"^[YN]$")
    dspy_yn: str = Field(default="Y", pattern=r"^[YN]$")
    sort_order: int = Field(..., examples=1)

    class Config:
        from_attributes = True  # 기존 orm_mode의 대체
        # allow_mutation이 기본적으로 False로 설정되므로 더 이상 필요하지 않음

    @property
    def full_code_name(self) -> str:
        return f"{self.type_cd}-{self.key_cd}-{self.cd_nm_1}"
