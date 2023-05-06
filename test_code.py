import ast
import datetime

import code
from typing import Iterable, Any, Optional, Generator, List


def test_chunks():
    input_list = [1, 2, 3, 4, 5, 6, 7, 8]
    chunk_size = 3
    expected_output = [[1, 2, 3], [4, 5, 6], [7, 8]]
    chunk_generator = code.chunks(input_list, chunk_size)
    for i in range(len(expected_output)):
        output_chunk = next(chunk_generator)
        assert output_chunk == expected_output[i]


def test_flat():
    input_list = [[1, 2, 3], [4, 5, 6, 7, 8]]
    expected_output = [1, 2, 3, 4, 5, 6, 7, 8]
    output = code.flat(input_list)
    assert output == expected_output


def test_has_recursive_calls():
    func1 = """
def plus_1(x):
    return x + 1
    """
    def_func1 = ast.parse(func1).body[0]
    assert code.has_recursive_calls(def_func1) == False

    func2 = """
def fibonancci(x):
    if x <= 1:
        return x
    else:
        fibonacci(x)
        return fibonancci(x-1) + fibonancci(x)
    """
    def_func2 = ast.parse(func2).body[0]
    assert code.has_recursive_calls(def_func2) == True


def test_parse_iso_date_time():
    iso_date_time = '2023-05-05T10:04:06'
    expected_date_time = datetime.datetime(2023, 5, 5, 10, 4, 6, 0)
    assert code.parse_iso_datetime(iso_date_time) == expected_date_time

    iso_date_time = '2023-05-05T10:04:06Z'
    expected_date_time = datetime.datetime(2023, 5, 5, 10, 4, 6, 0)
    assert code.parse_iso_datetime(iso_date_time) == expected_date_time

    iso_date_time = ''
    assert code.parse_iso_datetime(iso_date_time) == None


def test_if_logs_has_any_of_commands():
    log = [
        'INFO: User Alice logged in',
        'WARNING: Invalid password for user Bob',
        'ERROR: Connection failed',
        'DEBUG: Starting server',
    ]

    commands = ['User', 'Invalid', 'Failed']
    assert code.if_logs_has_any_of_commands(log, commands) == True


def test_extract_all_constants_from_ast():
    code_instance = '''
MESSAGE = "Hello, world!"
COUNT = 10
           '''

    ast_tree = ast.parse(code_instance)
    expected_output = ['Hello, world!']
    assert code.extract_all_constants_from_ast(ast_tree) == expected_output


def test_is_camel_case_word():
    word = 'Thanh'
    assert code.is_camel_case_word(word) == False
    word = 'THanh'
    assert code.is_camel_case_word(word) == True


def test_split_camel_case_words():
    word = "HELLo world"
    assert code.split_camel_case_words(word) == ['h', 'e', 'l', 'lo world']


def test_is_path_in_exclude_list():
    exclude_list = ['test', 'exclude']
    path1 = 'path/to/test/file.txt'
    assert code.is_path_in_exclude_list(path1, exclude_list) == True


def test_get_full_class_name():
    class MyClass:
        pass

    instance = MyClass()
    assert code.get_full_class_name(instance) == 'test_code.MyClass'
    instance = str()
    assert code.get_full_class_name(instance) == 'str'


def tes_max_with_default():
    lst = [1, 3, 5]
    assert code.max_with_default(lst) == 5
    lst = []
    assert code.max_with_default(lst, 3) == 3
    items = []
    default = 0
    assert code.max_with_default(items, default) == 0

    # Test when items are empty and default is None
    items = []
    assert code.max_with_default(items) is None


def test_is_python_class_name():
    class_name = 'String'
    assert code.is_python_class_name(class_name) == True
    class_name = 'string'
    assert code.is_python_class_name(class_name) == False
