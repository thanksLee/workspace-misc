from .configurable import Configurable


class BaseConfig(Configurable):
    def __init__(self):
        super().__init__('base')
        self._sql_file_path = self.get_config('sql_file_path')
        self._logger_setting_file_path = self.get_config('logger_setting_file_path')
        self._log_file_path = self.get_config('log_file_path')
        self._security_hash_key = self.get_config('security_hash_key')

    @property
    def sql_file_path(self):
        return self._sql_file_path

    @property
    def logger_setting_file_path(self):
        return self._logger_setting_file_path

    @property
    def log_file_path(self):
        return self._log_file_path

    @property
    def security_hash_key(self):
        return self._security_hash_key


base_config = BaseConfig()


class LocalDBConfig(Configurable):
    def __init__(self):
        super().__init__('localdb')
        self._db_type = self.get_config('database_type')
        self._db_path = self.get_config('database_path')
        self._db_name = self.get_config('database_name')

    @property
    def db_type(self):
        return self._db_type

    @property
    def db_path(self):
        return self._db_path

    @property
    def db_name(self):
        return self._db_name


local_db_config = LocalDBConfig()


class ConsoleLoggerConfig(Configurable):
    def __init__(self):
        super().__init__('console_logger')
        self._level = self.get_config('level')
        self._format = self.get_config('format')

    def reload(self):
        super().reload()
        self._level = self.get_config('level')
        self._format = self.get_config('format')

    @property
    def level(self):
        return self._level

    @property
    def format(self):
        return self._format


console_logger_config = ConsoleLoggerConfig()


class AppLoggerConfig(Configurable):
    def __init__(self):
        super().__init__('app_logger')
        self._rotation = self.get_config('rotation')
        self._retention = self.get_config('retention')
        self._level = self.get_config('level')
        self._format = self.get_config('format')

    def reload(self):
        super().reload()
        self._rotation = self.get_config('rotation')
        self._retention = self.get_config('retention')
        self._level = self.get_config('level')
        self._format = self.get_config('format')

    @property
    def rotation(self):
        return self._rotation

    @property
    def retention(self):
        return self._retention

    @property
    def level(self):
        return self._level

    @property
    def format(self):
        return self._format


app_logger_config = AppLoggerConfig()
