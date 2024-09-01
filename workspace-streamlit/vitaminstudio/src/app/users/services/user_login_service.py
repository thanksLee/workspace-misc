from typing import Optional

from common.services.common_service import CommonService

from core.databases.server.transaction_manager import TransactionManager
from core.utilities.misc import get_pwd
from core.constants.global_const import CURRENT_USER

from ..mappers.user_mapper import UserMapper
from ..schemas.dto.user_request_dto import LoginFormDTO
from ..schemas.vo.user_vo import UserVO
from ..schemas.dto.user_response_dto import UserResponseDTO, UserDetailSchema


class UserLoginService(CommonService):
    def __init__(self, tr_manager: TransactionManager):
        super().__init__(tr_manager)
        self._user_form: LoginFormDTO = None

    def user_login_check(self, user_form: LoginFormDTO):
        '''
        사용자 로그인 체크를 하는 함수

        Args:
        - user_form : form 에서 넘어온 변수 Object

        Returns
        - json

        - success
        {
            "status": 200
            "message": 'You have successfully logged in'
            "code" : "VITAMIN_SUCCESS_003"
            "detail": {
                "user_id": 'admin',
                "user_type_cd": 9,
                "user_type_cd_nm": '관리자'
            }
        }

        - fail
        {
            "status": 400
            "message": 'Login has failed.'
            "code" : "VITAMIN_ERROR_003"
            "detail": {}
        }
        '''
        self._user_form = user_form
        with self._tr_manager.get_transaction() as tran_session:
            qry_result: Optional[UserVO] = UserMapper(tran_session).select_user_login(user_form.login_id)

            if not qry_result:
                return self.__build_response(self._ret_status.FAIL, self._vs_msg.VS_ERROR_002)

            qry_result = qry_result[0]
            self._app_logger.debug(f'qry_result : {qry_result}')

            # 비밀번호 비교
            if not self.__pwd_compare(qry_result.login_pwd):
                return self.__build_response(self._ret_status.FAIL, self._vs_msg.VS_ERROR_004)

            # 사용자 사용 여부
            if qry_result.use_yn != 'Y':
                return self.__build_response(self._ret_status.FAIL, self._vs_msg.VS_ERROR_005)

            # 성공 응답
            _detail = UserDetailSchema(
                user_id=user_form.login_id,
                user_type_cd=qry_result.user_type_cd,
                user_type_cd_nm=qry_result.user_type_cd_nm,
                login_status=True
            )

            # session에 정보를 저장
            self._session_state_manager.set_session_state(CURRENT_USER, _detail.to_dict())
            self._app_logger.debug(self._session_state_manager.get_session_state())

            return self.__build_response(self._ret_status.SUCCESS, self._vs_msg.VS_SUCCESS_003, _detail.to_dict())

    def __pwd_compare(self, source_login_pwd: str) -> bool:
        '''
        source 와 parameter 로 넘어온 비밀번호하는 함수

        Args:
            - source_login_pwd : 사용자가 입력한 비밀번호

        Returns
            - 비밀번호가 일치하면 True, 그렇지 않으면 False
        '''
        tmp_login_pwd = get_pwd(self._base_config.security_hash_key, self._user_form.login_id, self._user_form.login_pwd)
        return source_login_pwd == tmp_login_pwd

    def __build_response(self, status, message, detail=None) -> dict:
        '''
        응답을 생성하는 함수

        Args:
            - status : 응답 상태 코드
            - message : 응답 메시지
            - detail : 응답에 포함할 상세 정보

        Returns
            - dict 형태의 응답
        '''
        return UserResponseDTO(
            status=status.value,
            message=message.value,
            code=message.name,
            detail=detail
        ).to_dict()
