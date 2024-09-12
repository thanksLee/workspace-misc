from threading import Lock


class SingletonMeta(type):
    """
    Singleton 메타클래스: 클래스 인스턴스를 단 하나만 생성하도록 보장합니다.
    """
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
