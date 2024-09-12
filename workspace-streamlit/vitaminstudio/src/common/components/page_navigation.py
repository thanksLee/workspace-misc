import streamlit as st
import math

from core.sessions.session_state_manager import SessionStateManager


class CommonPageNavigation:
    def __init__(self, session_state_manager: SessionStateManager, total_cnt: int = 0, display_cnt: int = 10):
        # 전체 데이터 개수와 페이지당 항목 개수 설정
        self._total_cnt = total_cnt
        # 한 번에 표시할 페이지 번호 개수
        self._pages_per_size = 5
        # 1 ~ self._pages_per_size 만큼의 데이터
        self._page_size = (display_cnt * self._pages_per_size)

        # 전체 페이지 수 계산
        self._total_pages = math.ceil(self._total_cnt / self._page_size)

        self._start_page = 0
        self._end_page = 0

        # Page Navigation 정보 가져오기
        self._session_state_manager = session_state_manager
        self._paging_info: dict = self._session_state_manager.get_session_state('current_paging_info')
        if not self._paging_info:
            self._paging_info = {
                'page_idx': 1,
                'page_next': 0,
                'min_page': 1,
                'max_page': self._pages_per_size
            }
            self._session_state_manager.set_session_state('current_paging_info', self._paging_info)

    def render(self):
        # 현재 페이지와 페이지 그룹
        current_page = self._paging_info['page_idx']
        page_next = self._paging_info['page_next']
        min_page = self._paging_info['min_page']
        max_page = self._paging_info['max_page']

        # 현재 페이지 그룹의 시작 페이지 번호와 끝 페이지 번호 계산
        self._start_page = min_page
        self._end_page = max_page

        cols = st.columns(7)  # 12개의 열을 생성

        # 이전 페이지 그룹 버튼
        if page_next > 0:
            if cols[0].button("◀", use_container_width=True):
                self.handle_pre_page()
                st.rerun()

        # 페이지 번호 버튼을 가로로 배치
        btn_disable: bool = True
        for i, page_num in enumerate(range(self._start_page, self._end_page + 1)):
            if (i+1) == current_page:
                btn_disable = True
            else:
                btn_disable = False
            if cols[i + 1].button(str(page_num), use_container_width=True, disabled=btn_disable):
                self.handle_current_page(page_num)

        # 다음 페이지 그룹 버튼
        if self._end_page < self._total_pages:
            if cols[6].button("▶", use_container_width=True):
                self.handle_next_page()
                st.rerun()

    def handle_current_page(self, page):
        '''페이지 선택 및 출력 함수'''
        self._paging_info["page_idx"] = page

    def handle_next_page(self):
        '''페이지 그룹 변경 함수'''
        self._paging_info["page_next"] = self._paging_info["page_next"] + 1
        self._paging_info["min_page"] = self._start_page + self._pages_per_size
        self._paging_info["max_page"] = self._end_page + self._pages_per_size

    def handle_pre_page(self):
        self._paging_info["page_next"] = self._paging_info["page_next"] - 1
        self._paging_info["min_page"] = self._start_page - self._pages_per_size
        self._paging_info["max_page"] = self._end_page - self._pages_per_size
