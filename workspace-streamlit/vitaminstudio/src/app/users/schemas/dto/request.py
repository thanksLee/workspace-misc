from pydantic import BaseModel, Field, field_validator


class DBServerDTO(BaseModel):
    server_type: str = Field(..., example='local')
    db_type: str = Field(..., example='sqlite')


class LoginFormDTO(BaseModel):
    login_id: str = Field(..., title='로그인 아이디', min_length=1, max_length=20, example='admin')
    login_pwd: str = Field(..., title='로그인 비밀번호', min_lengh=1, max_length=20, example='password')

    @field_validator('login_id', 'login_pwd')
    def strip_witeespace(cls, value):
        return value.strip()

    @field_validator('login_id')
    def validate_login_id(cls, value):
        if len(value) < 1 or len(value) > 20:
            raise ValueError('Login ID must be between 1 and 20 characters long.')
        return value

    @field_validator('login_pwd')
    def validate_login_pwd(cls, value):
        # 비밀번호 길이 확인
        if len(value) < 1:
            raise ValueError('Password must be at least 1 characters long.')
        return value
