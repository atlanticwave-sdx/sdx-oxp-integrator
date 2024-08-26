import pytest
from models.port import Port

# Sample valid and invalid values for testing
VALID_PORT_ID = "urn:sdx:port:valid_id"
INVALID_PORT_ID = "invalid_id"
VALID_NAME = "Valid_Name"
INVALID_NAME_SHORT = "AB"
INVALID_NAME_LONG = "A" * 31
INVALID_NAME_INVALID_CHARS = "Invalid_Name#"
VALID_NODE = "ValidNode"
INVALID_NODE = None
VALID_TYPE = "10GE"
INVALID_TYPE = "5GE"
VALID_MTU = 1500
INVALID_MTU = -1
VALID_STATUS = "up"
INVALID_STATUS = "unknown"
VALID_STATE = "enabled"
INVALID_STATE = "unknown"

def test_port_initialization():
    """Test the initialization of the Port class."""
    port = Port(
        port_id=VALID_PORT_ID,
        name=VALID_NAME,
        node=VALID_NODE,
        type=VALID_TYPE,
        mtu=VALID_MTU,
        status=VALID_STATUS,
        state=VALID_STATE
    )
    
    assert port.port_id == VALID_PORT_ID
    assert port.name == VALID_NAME
    assert port.node == VALID_NODE
    assert port.type == VALID_TYPE
    assert port.mtu == VALID_MTU
    assert port.status == VALID_STATUS
    assert port.state == VALID_STATE

def test_port_id_validation():
    """Test validation for port_id property."""
    port = Port()
    
    with pytest.raises(ValueError):
        port.port_id = INVALID_PORT_ID
    
    port.port_id = VALID_PORT_ID
    assert port.port_id == VALID_PORT_ID

def test_name_validation():
    """Test validation for name property."""
    port = Port()
    
    with pytest.raises(ValueError):
        port.name = INVALID_NAME_SHORT
    
    with pytest.raises(ValueError):
        port.name = INVALID_NAME_LONG
    
    with pytest.raises(ValueError):
        port.name = INVALID_NAME_INVALID_CHARS
    
    port.name = VALID_NAME
    assert port.name == VALID_NAME

def test_node_validation():
    """Test validation for node property."""
    port = Port()
    
    with pytest.raises(ValueError):
        port.node = INVALID_NODE
    
    port.node = VALID_NODE
    assert port.node == VALID_NODE

def test_type_validation():
    """Test validation for type property."""
    port = Port()
    
    with pytest.raises(ValueError):
        port.type = INVALID_TYPE
    
    port.type = VALID_TYPE
    assert port.type == VALID_TYPE

def test_mtu_validation():
    """Test validation for mtu property."""
    port = Port()
    port.mtu = VALID_MTU
    assert port.mtu == VALID_MTU

def test_status_validation():
    """Test validation for status property."""
    port = Port()
    
    with pytest.raises(ValueError):
        port.status = INVALID_STATUS
    
    port.status = VALID_STATUS
    assert port.status == VALID_STATUS

def test_state_validation():
    """Test validation for state property."""
    port = Port()
    
    with pytest.raises(ValueError):
        port.state = INVALID_STATE
    
    port.state = VALID_STATE
    assert port.state == VALID_STATE

def test_from_dict():
    """Test the from_dict class method."""
    dict_input = {
        "port_id": VALID_PORT_ID,
        "name": VALID_NAME,
        "node": VALID_NODE,
        "type": VALID_TYPE,
        "mtu": VALID_MTU,
        "status": VALID_STATUS,
        "state": VALID_STATE
    }
    
    port = Port.from_dict(dict_input)
    
    assert port.port_id == VALID_PORT_ID
    assert port.name == VALID_NAME
    assert port.node == VALID_NODE
    assert port.type == VALID_TYPE
    assert port.mtu == VALID_MTU
    assert port.status == VALID_STATUS
    assert port.state == VALID_STATE
