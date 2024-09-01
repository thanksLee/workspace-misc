
def split_str(split_flg: str, input_string: str) -> list:
    """
    문자열을 split_flg 로 분리하여 튜플로 반환하는 함수.

    Args:
    - split_flg (str) : split 할 구분자
    - input_string (str): 분리할 입력 문자열 (예: '1:공공데이터')

    Returns:
    - list: 분리된 문자열의 리스트 (예: ['1', '공공데이터'])
    """
    ret_val = input_string.split(split_flg, 1)

    return ret_val
