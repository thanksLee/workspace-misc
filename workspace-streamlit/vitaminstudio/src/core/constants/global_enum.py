from enum import Enum, unique


@unique
class ProductInfo(Enum):
    '''제품과 관련된 Enum'''
    NAME = 'VitaminStudio'
    TITLE = f':pill: {NAME}'
    VERSION = 'v1.0.0'


@unique
class ServerType(Enum):
    '''제품에서 사용할 database 의 위치'''
    LOCAL = 'local'
    SERVER = 'server'

    @classmethod
    def __list_values__(cls):
        return [member.value for member in cls]


@unique
class ServerDB(Enum):
    '''
    - 제품에서 사용할 database server
    - sqlite라면 local에서 사용한다.
    '''
    SQLITE = 'sqlite'
    ORACLE = 'oracle'
    POSTGRESQL = 'postgresql'

    @classmethod
    def __list_values__(cls):
        return [member.value for member in cls]


SERVER_TYPE: list = ServerType.__list_values__()
SERVER_DB: list = ServerDB.__list_values__()


@unique
class LoggerName(Enum):
    APP = 'app'
    CONSOLE = 'console'
    SQL = 'sql'
