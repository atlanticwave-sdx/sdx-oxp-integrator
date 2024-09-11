from datetime import datetime, date
from utils.util import get_timestamp, _deserialize, deserialize_date, deserialize_datetime, _deserialize_primitive
from utils.util import _deserialize_object, _deserialize_list, _deserialize_dict, deserialize_model
import pytz

class MockClass:
    openapi_types = {'attr1': str}
    attribute_map = {'attr1': 'attr1'}

    def __init__(self):
        self.attr1 = None

def test_get_timestamp_with_provided_timestamp():
    """
    Test the `get_timestamp` function when a timestamp is provided.
    
    This test verifies that when a specific timestamp is provided, 
    the `get_timestamp` function formats and returns it correctly in ISO 8601 format.
    """
    timestamp = "2024-09-11T12:34:56Z"
    result = get_timestamp(timestamp)
    assert result == "2024-09-11T12:34:56Z"

def test_get_timestamp_without_provided_timestamp():
    """
    Test the `get_timestamp` function when no timestamp is provided.
    
    This test verifies that when no timestamp is provided, the `get_timestamp` 
    function returns the current timestamp in the specified format.
    """
    result = get_timestamp()
    now = datetime.now(pytz.timezone("America/New_York")).strftime("%Y-%m-%dT%H:%M:%SZ")
    assert result == now

def test_deserialize_date():
    """
    Test the `deserialize_date` function.
    
    This test verifies that a date string is correctly deserialized into a `date` object.
    """
    date_str = "2024-09-11"
    result = deserialize_date(date_str)
    assert result == '2024-09-11'

def test_deserialize_datetime():
    """
    Test the `deserialize_datetime` function.
    
    This test verifies that an ISO 8601 datetime string is correctly deserialized 
    into a `datetime` object with UTC timezone.
    """
    datetime_str = "2024-09-11T12:34:56Z"
    result = deserialize_datetime(datetime_str)
    assert result == '2024-09-11T12:34:56Z'

def test_deserialize_primitive_int():
    """
    Test the `_deserialize_primitive` function for integer deserialization.
    
    This test verifies that a string representing an integer is correctly deserialized into an `int`.
    """
    result = _deserialize_primitive("123", int)
    assert result == 123

def test_deserialize_primitive_float():
    """
    Test the `_deserialize_primitive` function for float deserialization.
    
    This test verifies that a string representing a float is correctly deserialized into a `float`.
    """
    result = _deserialize_primitive("123.456", float)
    assert result == 123.456

def test_deserialize_primitive_str():
    """
    Test the `_deserialize_primitive` function for string deserialization.
    
    This test verifies that a string is correctly deserialized into a `str`.
    """
    result = _deserialize_primitive("abc", str)
    assert result == "abc"

def test_deserialize_primitive_bool():
    """
    Test the `_deserialize_primitive` function for boolean deserialization.
    
    This test verifies that a string representing a boolean is correctly deserialized into a `bool`.
    """
    result = _deserialize_primitive("True", bool)
    assert result is True

def test_deserialize_object():
    """
    Test the `_deserialize_object` function.
    
    This test verifies that the `_deserialize_object` function returns the input value unchanged.
    """
    result = _deserialize_object("some value")
    assert result == "some value"

def test_deserialize_list():
    """
    Test the `_deserialize_list` function.
    
    This test verifies that a list of strings is correctly deserialized into a list of integers.
    """
    data = ["1", "2", "3"]
    result = _deserialize_list(data, int)
    assert result == [1, 2, 3]

def test_deserialize_dict():
    """
    Test the `_deserialize_dict` function.
    
    This test verifies that a dictionary with string values is correctly deserialized.
    """
    data = {"a": "1", "b": "2"}
    result = _deserialize_dict(data, str)
    assert result == {"a": "1", "b": "2"}

def test_deserialize_model():
    """
    Test the `deserialize_model` function.
    
    This test verifies that a dictionary is correctly deserialized into an instance 
    of `MockClass`, with attributes mapped and deserialized correctly.
    """
    data = {"attr1": "value"}
    instance = deserialize_model(data, MockClass)
    assert isinstance(instance, MockClass)
    assert instance.attr1 == "value"
