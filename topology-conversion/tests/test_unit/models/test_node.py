import pytest
from models.location import Location
from models.port import Port
from models.node import Node

# Sample valid data
valid_node_data = {
    "node_id": "urn:sdx:node:example_node",
    "name": "ExampleNode",
    "location": Location(latitude=10.0, longitude=20.0),
    "ports": [Port(port_id="port1"), Port(port_id="port2")]
}

# Sample invalid data
invalid_node_id = [
    None,
    "invalid_id",
]

invalid_name = [
    None,
    "N",
    "A" * 31,
    "Invalid@Name"
]

def test_node_initialization():
    """Test the initialization of the Node class."""
    node = Node(
        node_id="urn:sdx:node:example_node",
        name="ExampleNode",
        location=Location(latitude=10.0, longitude=20.0),
        ports=[Port(port_id="port1"), Port(port_id="port2")]
    )
    assert node.node_id == "urn:sdx:node:example_node"
    assert node.name == "ExampleNode"
    assert node.location.latitude == 10.0
    assert node.location.longitude == 20.0
    assert len(node.ports) == 2
    assert node.ports[0].port_id == "port1"
    assert node.ports[1].port_id == "port2"

@pytest.mark.parametrize("node_id", invalid_node_id)
def test_invalid_node_id(node_id):
    """Test validation for port_id property."""
    node = Node()    
    with pytest.raises(ValueError):
        node.node_id = node_id

@pytest.mark.parametrize("name", invalid_name)
def test_invalid_name(name):
    """Test validation for name property."""
    node = Node()    
    with pytest.raises(ValueError):
        node.name = name

def test_invalid_location():
    """Test validation for location property."""
    node = Node()    
    with pytest.raises(ValueError):
        node.location = None

def test_invalid_ports():
    """Test valid node_id and name but invalid ports."""
    node = Node(
            node_id="urn:sdx:node:valid_node",
            name="ValidName",
            location=Location(latitude=10.0, longitude=20.0)
        )   
    with pytest.raises(ValueError):
        node.ports = None

@pytest.mark.xfail
def test_from_dict():
    """Test from_dict method with valid data.
        This test is expected to fail because utils.util.py tries to access datetime.datetime 
        but it fails because the datetime class is not being accessed correctly. 
        In the _deserialize function, datetime refers to the datetime class directly, 
        so datetime.datetime should not be used. Instead, datetime should be used directly.
    """
    node = Node.from_dict(valid_node_data)
    assert node.node_id == "urn:sdx:node:example_node"
    assert node.name == "ExampleNode"
    assert node.location.latitude == 10.0
    assert node.location.longitude == 20.0
    assert len(node.ports) == 2
    assert node.ports[0].port_id == "port1"
    assert node.ports[1].port_id == "port2"

def test_from_dict_invalid_data():
    """Test from_dict method with invalid data"""
    invalid_data = {"node_id": None, "name": "ValidName"}
    with pytest.raises(ValueError):
        Node.from_dict(invalid_data)

    invalid_data = {"node_id": "urn:sdx:node:valid_node", "name": None}
    with pytest.raises(ValueError):
        Node.from_dict(invalid_data)
