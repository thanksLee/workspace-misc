from core.sessions.session_state_manager import SessionStateManager


class CommonView:
    def __init__(self, session_state_manager: SessionStateManager):
        self._session_state_manager = session_state_manager
