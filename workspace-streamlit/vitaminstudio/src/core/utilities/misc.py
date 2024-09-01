import hashlib
import json
from typing import List, TypeVar, Optional

from core.constants.global_enum import ServerDB

T = TypeVar('T')


def get_database_url(db_type: str, database_url: str) -> str | None:
    """
    데이터베이스에 연결할 URL 조합

    Args:
    - db_type : local or server
    - database_url : DB에 접속할 URL

    Returns:
    - database_url : 완성된 DB 접속 URL

    ex)
        get_database_url('sqlite', './volumes/database/vitamin.db')
        -> sqlite:///./volumes/database/vitamin.db
    """
    if db_type == ServerDB.SQLITE.value:
        return f'sqlite:///{database_url}'
    else:
        return None


def get_pwd(hash_key: str, salt_key: str, pwd: str) -> str:
    """
    단방향 암호화를 생성하는 함수

    Args:
    - hash_key : 공통으로 사용하는 hash key
    - salt_key : 해당 함수를 호출하는 구분자 key
    - pwd : 암호화 시킬 값

    Returns:
    - password_hash : 단방향 암호화된 hash 값

    ex)
        get_pwd('vataminstudio', 'admin', '3')
        -> 89b1c3b33f584b45c12e91d1b79c894dfdef1842b...
    """
    hash_pwd = f'{hash_key}{salt_key}{pwd}'
    password_hash = hashlib.sha512(hash_pwd.encode("utf-8")).hexdigest()
    # print(f'password_hash : {password_hash}')

    return password_hash


def model_result_to_json(result: List[T]) -> Optional[str]:
    """
    모델 인스턴스 목록을 JSON 문자열로 변환하는 유틸리티 함수.

    :param result: 모델 인스턴스 목록.
    :return: JSON 형식의 문자열 또는 None.
    """
    if not result:
        return None

    # 각 모델 인스턴스를 dict로 변환한 후 JSON 문자열로 변환
    json_result = json.dumps([item.dict() for item in result], ensure_ascii=False)

    return json_result
