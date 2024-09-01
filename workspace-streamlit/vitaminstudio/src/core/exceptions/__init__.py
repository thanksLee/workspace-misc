

class ExistsDatabase(Exception):
    def __init__(self, message: str = None):

        if message is None:
            message = 'The database is already created.'

        super().__init__(message)


class InstanceNotLoadError(Exception):
    def __init__(self, message: str = None):

        if message is None:
            message = 'The instance has not been loaded.'

        super().__init__(message)


class CommonCodeValueError(Exception):
    def __init__(self, message: str = None):

        if message is None:
            message = 'There is no matching value in the common code.'

        super().__init__(message)
