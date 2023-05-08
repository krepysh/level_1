import code
import ast
from datetime import datetime


def test_chunks():
    assert list(code.chunks([0, 1, 2], 2)) == [[0, 1], [2]]
    assert list(code.chunks([0, 1, 2, 3], 2)) == [[0, 1], [2, 3]]
    assert list(code.chunks([0, 1, 2, 3], 1)) == [[0], [1], [2], [3]]


def test_flat():
    assert code.flat([[0], [1], [2], [3]]) == [0, 1, 2, 3]
    assert code.flat([[0], [1], [2]]) == [0, 1, 2]
    assert code.flat([[0]]) == [0]


def test_has_recursive_calls():
    st1 = '''
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n-1)
        '''
    st2 = '''
def test_func_no_recursive():
    return True
        '''
    rec = ast.parse(st1).body[0]
    rec2 = ast.parse(st2).body[0]
    assert code.has_recursive_calls(rec) is True
    assert code.has_recursive_calls(rec2) is False


def test_parse_iso_datetime():
    assert code.parse_iso_datetime('2022-05-06T12:34:56.789') == datetime(2022, 5, 6, 12, 34, 56, 789000)
    assert code.parse_iso_datetime('2022-05-06T12:34:56.789Z') == datetime(2022, 5, 6, 12, 34, 56, 789000)
    assert code.parse_iso_datetime('chik-chirik') is None


def test_if_logs_has_any_of_commands():
    log = [
        'command1 --option value',
        'command2',
        'command3 value',
    ]
    assert code.if_logs_has_any_of_commands(log, ['command1', 'command2']) is True
    assert code.if_logs_has_any_of_commands(log, ['command4']) is False


def test_extract_all_constants_from_ast():
    ast_tree = ast.parse('MY_CONSTANT = "value"\nOTHER_CONSTANT = "1,2,3"')
    assert code.extract_all_constants_from_ast(ast_tree) == ['value', '1,2,3'] or ['1,2,3', 'value']


def test_is_camel_case_word():
    assert code.is_camel_case_word('CamelCase') is True
    assert code.is_camel_case_word('camelCase') is True
    assert code.is_camel_case_word('camelcase') is False


def test_split_camel_case_words():
    assert code.split_camel_case_words('CamelCase') == ['camel', 'case']
    assert code.split_camel_case_words('camelCase') == ['camel', 'case']
    assert code.split_camel_case_words('Camelcase') == ['camelcase']


def test_is_path_in_exclude_list():
    assert code.is_path_in_exclude_list('/path/to/excluded/file', ['/path/to/excluded']) is True
    assert code.is_path_in_exclude_list('/path/to/file', ['/path/to/excluded']) is False


def test_get_full_class_name():
    class ShalomClass:
        pass
    obj = ShalomClass
    assert code.get_full_class_name(ShalomClass()) == 'test_code.ShalomClass'
    assert code.get_full_class_name('str') == 'str'


def test_max_with_default():
    assert code.max_with_default([1, 2, 3]) == 3
    assert code.max_with_default([]) == 0
    assert code.max_with_default([], 10) == 10
