import chardet
from pathlib import Path, PurePath


def create_dir(dir_path: str) -> str:
    """
    파일 경로를 포함하여 디렉토리를 생성하는 함수

    Args:
    - dir_path : 파일 경로

    Returns:
    - ret_val : 파일 경로

    ex)
        create_dir('./volumes/database')
        -> ./volumes/database
    """
    ret_val = ''

    p = Path(dir_path)
    if not p.is_dir():
        p.mkdir(exist_ok=True, parents=True)
        ret_val = dir_path

    return ret_val


def get_file_list(dir_path: str) -> list:
    """
    파일 경로에서 파일명 + 확장자를 리스트로 Return 하는 함수

    Args:
    - dir_path : 파일 경로

    Returns:
    - ret_val : 파일 경로

    ex)
        get_file_list('./volumes/database')
        -> ['vitamin_01.db', 'vitamin_02.db']
    """
    ret_val = []

    # 폴더 경로 지정
    folder_path = Path(dir_path)

    # 폴더 안의 파일 목록 가져오기
    for file in folder_path.iterdir():
        if file.is_file():  # 파일만 리스트에 추가
            ret_val.append(file.name)

    return ret_val


def get_file_exists(file_path: str) -> bool:
    """
    파일이 존재하는 체크하는 함수

    Args:
    - file_path : 파일 경로

    Returns:
    - ret_val : True, False

    ex)
        get_file_exists('./volumes/database/vitmain.db')
        -> True
    """
    ret_val: bool = False

    if Path(file_path).exists():
        ret_val = True
    return ret_val


def detect_encoding(file_path: str):
    """
    파일을 읽어서 encoding 검사하는 함수

    Args:
    - file_path : 파일 경로

    Returns:
    - ret_val :

    ex)
        detect_encoding('./sqlscript/sqlite/01_sqlite_create_table.sql')
        ->
    """
    with open(file_path, 'rb') as file:
        raw_data = file.read(100)  # 파일의 일부를 읽어서 인코딩을 감지합니다.
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        return encoding


def load_sql_file(file_path: str) -> list:
    from core.constants.global_const import SQL_LOAD_FILE_EXT
    """
    파일을 읽어서 sql statement 를 추출하는 함수

    Args:
    - file_path : 파일 경로

    Returns:
    - ret_val : list

    ex)
        load_sql_file('./sqlscript/sqlite/01_sqlite_create_table.sql')
        -> ['insert into~~~', 'insert into ~~~']
    """

    # 파일 확장차 추출
    file_ext = get_file_name_split(1, file_path)

    sql_statements = []
    statement = ''

    # 확장자가 .sql 인지 판단
    if file_ext not in SQL_LOAD_FILE_EXT:
        return sql_statements

    # 파일 인코딩 검사
    encoding = detect_encoding(file_path)
    print(f"Detected encoding: {encoding}")

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        # 주석을 무시
        line = line.strip()
        if line.startswith('--') or line == '':
            continue

        statement += ' ' + line
        if statement.endswith(';'):
            sql_statements.append(statement.strip())
            statement = ''

    if statement:
        sql_statements.append(statement.strip())

    return sql_statements


def get_file_name_split(flg: int, file_name: str) -> str:
    """
    flag에 따라서 return 하는 값이 다름
        0 : 확장자를 제외한 나머지 경로
        1 : 확장자 추출

    Args:
    - file_name : 경로를 포함한 파일 명 or 단순 파일명

    Returns:
    - ret_val : .tiff

    ex)
        get_file_name_split(0, './sqlscript/sqlite/01_sqlite_create_table.sql')
        -> ./sqlscript/sqlite/01_sqlite_create_table

        get_file_name_split(1, './sqlscript/sqlite/01_sqlite_create_table.sql')
        -> .sql
    """
    ret_val = None
    split_file_name = str(PurePath(file_name).stem)
    split_file_ext = str(PurePath(file_name).suffix)
    if flg == 0:
        # output : .확장자 없음 (파일 경로가 있으면 파일경로까지 포함.)
        ret_val = split_file_name
    else:
        # output : .확장자
        ret_val = split_file_ext
    return ret_val
