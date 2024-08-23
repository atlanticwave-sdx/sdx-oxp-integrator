import pytest
from models.error_message import ErrorMessage
from utils import util

def test_error_message_initialization():
    """Test the initialization of the ErrorMessage class."""
    error_message = ErrorMessage(
        error_code="404",
        error_message="Not Found"
    )
    
    assert error_message.error_code == "404"
    assert error_message.error_message == "Not Found"

def test_error_code_validation():
    """Test validation for error_code property."""
    error_message = ErrorMessage()
    with pytest.raises(ValueError):
        error_message.error_code=None
    
    error_message = ErrorMessage(error_code="400")
    assert error_message.error_code == "400"

def test_error_message_validation():
    """Test validation for error_message property."""
    error_message = ErrorMessage()
    with pytest.raises(ValueError):
        error_message.error_message=None
    
    error_message = ErrorMessage(error_message="Bad Request")
    assert error_message.error_message == "Bad Request"

def test_from_dict_method():
    """Test the from_dict class method."""
    data = {
        "error_code": "500",
        "error_message": "Internal Server Error"
    }
    error_message = ErrorMessage.from_dict(data)
    assert error_message.error_code == "500"
    assert error_message.error_message == "Internal Server Error"
