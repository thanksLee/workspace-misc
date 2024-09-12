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


@unique
class MenuItem(Enum):
    MENU_0000 = 'Dashboard'
    MENU_0001 = '표준 단어 사전'
    MENU_0002 = '표준 용어 사전'
    MENU_0003 = '표준 도메인 사전'
    MENU_0004 = '모델 분석'
    MENU_0005 = '모델 비교'
    MENU_0006 = '모델 명세'
    MENU_0007 = '감리 대응 분석'
    MENU_0008 = '설정'
    MENU_0009 = '로그아웃'
