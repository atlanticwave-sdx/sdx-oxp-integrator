import pytest
from unittest import mock
from typing import List, Dict, Generic, TypeVar

from utils.typing_utils import is_generic, is_dict, is_list

# Define type variables for testing
T = TypeVar('T')
        
@pytest.mark.parametrize("klass, expected", [
    (List[int], True),    # Test if List[int] is recognized as a generic class
    (Dict[str, int], True), # Test if Dict[str, int] is recognized as a generic class
    (int, False),          # Test if int is not recognized as a generic class
    (Generic[T], True),   # Test if Generic[T] is recognized as a generic class
])
def test_is_generic_python_3_6(klass, expected):
    """Test `is_generic` function behavior with Python 3.6 (mocked version)"""
    with mock.patch('sys.version_info', (3, 6)):
        result = is_generic(klass)
        assert result == expected
        
@pytest.mark.parametrize("klass, expected", [
    (List[int], True),    # Test if List[int] is recognized as a generic class
    (Dict[str, int], True), # Test if Dict[str, int] is recognized as a generic class
    (int, False),          # Test if int is not recognized as a generic class
    (Generic[T], True),   # Test if Generic[T] is recognized as a generic class
])
def test_is_generic(klass, expected):
    """
    Test the `is_generic` function.
    
    This test verifies that the `is_generic` function correctly identifies
    whether a class is a generic class or not, based on the provided input.
    """
    result = is_generic(klass)
    assert result == expected

@pytest.mark.parametrize("klass, expected", [
    (Dict[str, int], True),  # Test if Dict[str, int] is recognized as a dict
    (List[int], False),      # Test if List[int] is not recognized as a dict
    (Dict[str, Dict[str, int]], True),  # Test nested dictionary
])
def test_is_dict_python_3_6(klass, expected):
    """Test `is_dict` function behavior with Python 3.6 (mocked version)"""
    with mock.patch('sys.version_info', (3, 6)):
        result = is_dict(klass)
        assert result == expected

@pytest.mark.parametrize("klass, expected", [
    (Dict[str, int], True),  # Test if Dict[str, int] is recognized as a dict
    (List[int], False),      # Test if List[int] is not recognized as a dict
    (Dict[str, Dict[str, int]], True),  # Test nested dictionary
])
def test_is_dict(klass, expected):
    """
    Test the `is_dict` function.
    
    This test verifies that the `is_dict` function correctly identifies
    whether a class is a dictionary type or not, based on the provided input.
    """
    result = is_dict(klass)
    assert result == expected

@pytest.mark.parametrize("klass, expected", [
    (List[int], True),   # Test if List[int] is recognized as a list
    (Dict[str, int], False), # Test if Dict[str, int] is not recognized as a list
    (List[List[int]], True),  # Test nested list
])
def test_is_list_python_3_6(klass, expected):
    """Test `is_list` function behavior with Python 3.6 (mocked version)"""
    with mock.patch('sys.version_info', (3, 6)):
        result = is_list(klass)
        assert result == expected

@pytest.mark.parametrize("klass, expected", [
    (List[int], True),   # Test if List[int] is recognized as a list
    (Dict[str, int], False), # Test if Dict[str, int] is not recognized as a list
    (List[List[int]], True),  # Test nested list
])
def test_is_list(klass, expected):
    """
    Test the `is_list` function.
    
    This test verifies that the `is_list` function correctly identifies
    whether a class is a list type or not, based on the provided input.
    """
    result = is_list(klass)
    assert result == expected
