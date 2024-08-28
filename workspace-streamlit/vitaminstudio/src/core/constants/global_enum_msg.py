from enum import Enum, unique


@unique
class VSMessage(Enum):
    VS_SUCCESS_001 = 'The database has been successfully created.'
    VS_SUCCESS_002 = 'You have connected to the selected database.'
    VS_SUCCESS_003 = 'You have successfully logged in.'

    VS_ERROR_001 = 'The database is already created.'
    VS_ERROR_002 = 'The user does not exist.'
    VS_ERROR_003 = 'Login has failed.'
    VS_ERROR_004 = 'The password does not match.'
    VS_ERROR_005 = 'The user account is suspended.'


@unique
class ResultStatus(Enum):
    SUCCESS = 200
    FAIL = 400
