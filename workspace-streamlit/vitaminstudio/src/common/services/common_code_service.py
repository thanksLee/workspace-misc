from common.services.common_service import CommonService
from common.mappers.common_code_mapper import CommonCodeMapper

from core.singletons.common_code_singleton import CommonCodeSingleton
from core.exceptions import InstanceNotLoadError


class CommonCodeService(CommonService):
    def __init__(self, tr_manager):
        super().__init__(tr_manager)

        self._common_codes = None

    def get_common_code_list(self):
        # 트랜잭션을 통해 공통 코드를 데이터베이스에서 로드
        with self._tr_manager.get_transaction() as tran_session:
            self._common_codes = CommonCodeMapper(tran_session).select_common_code_list()

        return self._common_codes

    def set_memory_load(self):
        # 메모리에 공통 코드를 로드
        if self._common_codes is None:
            raise InstanceNotLoadError("Common codes are not loaded. Call 'get_common_code_list' first.")
        CommonCodeSingleton.reset_instance(self._common_codes)

    def load_and_set_memory(self):
        # 공통 코드를 로드하고 메모리에 올리는 메서드
        self.get_common_code_list()
        self.set_memory_load()

        # self._app_logger.debug(f'CommonCodeSingleton.get_instance() : {CommonCodeSingleton.get_instance()}')
