import json
from typing import List, Type, TypeVar, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy.engine.row import Row
from typing import Optional

from core.loggers.manager import app_logger

T = TypeVar('T')


class CommonMapper:
    def __init__(self, db_session: Session):
        self._db_session: Session = db_session
        self._app_logger = app_logger

    def map_result_to_model(self, result: List[Dict[str, Any]], model: Type[T]) -> Optional[List[T]]:
        """
        SQLAlchemy 결과를 지정한 모델로 변환하는 유틸리티 함수.

        :param result: SQLAlchemy로부터 반환된 결과 목록.
        :param model: 변환할 모델 클래스.
        :return: 모델 인스턴스 목록.
        """

        ret_val = []

        if result is None:
            return None

        # 결과가 리스트가 아닌 경우 리스트로 변환
        if isinstance(result, Row):
            result = [result]

        # self._app_logger.debug(f'result: {result}')

        # 결과가 하나 이상의 항목을 포함하는 경우 모델 인스턴스를 리스트로 반환
        ret_val = [model(**row._mapping) for row in result]

        return ret_val

    def map_result_to_json(self, result: List[Dict[str, Any]]) -> Optional[str]:
        """
        SQLAlchemy 결과를 지정한 모델로 변환하고 JSON으로 반환하는 유틸리티 함수.

        :param result: SQLAlchemy로부터 반환된 결과 목록.
        :param model: 변환할 모델 클래스.
        :return: JSON 형식의 모델 인스턴스 목록.
        """
        if result is None:
            return None

        # 결과가 Row 객체가 아니라면 리스트로 변환
        if isinstance(result, Row):
            result = [result]

        # 각 row를 직접 dict로 변환하고 이를 JSON으로 직렬화
        json_result = json.dumps(
            [{**row._mapping} for row in result], ensure_ascii=False
        )

        return json_result

    def model_result_to_json(self, result: List[T]) -> Optional[str]:
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
