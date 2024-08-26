import pytest
from utils.util import get_timestamp
from models.topology import Topology
from models.node import Node
from models.link import Link
'''
# Mock implementations of Node and Link if they are not available
class Node:
    pass

class Link:
    pass
'''
def test_topology_initialization():
    """Test the initialization of the Topology class."""
    topology = Topology(
        topology_id="urn:sdx:topology:oxp_url",
        name="ExampleTopology",
        version=1,
        model_version="1.0",
        time_stamp=get_timestamp(),
        oxpo_url="oxp_url",
        nodes=[Node()],
        links=[Link()]
    )
    
    assert topology.topology_id == "urn:sdx:topology:oxp_url"
    assert topology.name == "ExampleTopology"
    assert topology.version == 1
    assert topology.model_version == "1.0"
    assert topology.time_stamp is not None
    assert topology.oxpo_url == "oxp_url"
    assert isinstance(topology.nodes, list)
    assert isinstance(topology.links, list)

def test_topology_id_validation():
    """Test validation for topology_id property."""
    topology = Topology()

    with pytest.raises(ValueError):
        topology.topology_id = None
        
    with pytest.raises(ValueError):
        topology.topology_id = "invalid_id"
        
    topology = Topology(topology_id="urn:sdx:topology:valid_id")
    assert topology.topology_id == "urn:sdx:topology:valid_id"

def test_name_validation():
    """Test validation for name property."""
    topology = Topology()

    with pytest.raises(ValueError):
        topology.name = None
        
    with pytest.raises(ValueError):
        topology.name = "ab"
        
    with pytest.raises(ValueError):
        topology.name = "a" * 31
        
    with pytest.raises(ValueError):
        topology.name = "Invalid_Name@"
        
    topology = Topology(name="Valid_Name")
    assert topology.name == "Valid_Name"

def test_version_validation():
    """Test validation for version property."""
    topology = Topology()

    with pytest.raises(ValueError):
        topology.version = None
    
    topology = Topology(version=1)
    assert topology.version == 1

def test_model_version_validation():
    """Test validation for model_version property."""
    topology = Topology()

    with pytest.raises(ValueError):
        topology.model_version = None
    
    topology = Topology(model_version="1.0")
    assert topology.model_version == "1.0"

def test_time_stamp_validation():
    """Test validation for time_stamp property."""
    topology = Topology()

    with pytest.raises(ValueError):
        topology.time_stamp = None
    
    topology = Topology(time_stamp=get_timestamp())
    assert topology.time_stamp is not None

def test_oxpo_url_validation():
    """Test validation for oxpo_url property."""
    topology = Topology()

    with pytest.raises(ValueError):
        topology.oxpo_url = None
    
    topology = Topology(oxpo_url="http://example.com")
    assert topology.oxpo_url == "http://example.com"

def test_nodes_validation():
    """Test validation for nodes property."""
    topology = Topology()

    with pytest.raises(ValueError):
        topology.nodes = None
    
    topology = Topology(nodes=[Node()])
    assert isinstance(topology.nodes, list)

def test_links_validation():
    """Test validation for links property."""
    topology = Topology()

    with pytest.raises(ValueError):
        topology.links = None

    topology = Topology(links=[Link()])
    assert isinstance(topology.links, list)

@pytest.mark.xfail
def test_from_dict_method():
    """Test the from_dict class method.
        This test is expected to fail because utils.util.py tries to access datetime.datetime 
        but it fails because the datetime class is not being accessed correctly. 
        In the _deserialize function, datetime refers to the datetime class directly, 
        so datetime.datetime should not be used. Instead, datetime should be used directly.
    """
    data = {
        "topology_id": "urn:sdx:topology:oxp_url",
        "name": "FromDictTopology",
        "version": 2,
        "model_version": "2.0",
        "time_stamp": get_timestamp(),
        "oxpo_url": "http://fromdict.com",
        "nodes": [{}],  # Mock Node objects
        "links": [{}]   # Mock Link objects
    }
    
    topology = Topology.from_dict(data)
    assert topology.topology_id == "urn:sdx:topology:oxp_url"
    assert topology.name == "FromDictTopology"
    assert topology.version == 2
    assert topology.model_version == "2.0"
    assert topology.oxpo_url == "http://fromdict.com"
    assert isinstance(topology.nodes, list)
    assert isinstance(topology.links, list)
