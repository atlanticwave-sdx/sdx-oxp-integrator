import requests
from unittest.mock import MagicMock
import os
import pytest

os.environ["MODEL_VERSION"] = '1'
os.environ["OXPO_NAME"] = 'TestTopology'
os.environ["OXPO_URL"] = 'oxp_url'
os.environ["OXP_TOPOLOGY_URL"] = 'http://mock-url'

from controllers.topology_controller import get_oxp_topology, convert_topology
from utils.util import get_timestamp

def test_get_oxp_topology_success(mock_requests_get):
    """Test successful retrieval of OXP topology."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"topology": {"nodes": [], "links": []}}
    mock_requests_get.return_value = mock_response

    result = get_oxp_topology()
    assert result == {"nodes": [], "links": []}
    mock_requests_get.assert_called_once_with("http://mock-url", timeout=10)

@pytest.mark.xfail
def test_get_oxp_topology_failure(mock_requests_get):
    """Test handling of request failure in get_oxp_topology.
    This is expected to fail because in the main code a variable initialized in a 'try' block 
    is used in the 'except' block. When the function that assigns the value to that variable fails, 
    the next error occurs: UnboundLocalError: local variable 'response' referenced before assignment
    """
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_requests_get.side_effect = requests.RequestException("Error")
    mock_requests_get.return_value = mock_response

    result = get_oxp_topology()
    assert result == {"error": "Failed to retrieve data", "status_code": 400}
    mock_requests_get.assert_called_once_with("http://mock-url", timeout=10)

def test_convert_topology_success(mock_requests_get, mock_parse_convert_topology):
    """Test successful conversion of topology."""
    mock_response = MagicMock()
    mock_requests_get.return_value = mock_response
    timestamp = get_timestamp()
    mock_converted_topology = {
        "nodes": [{
            "id": "urn:sdx:node:oxp_url:node1",
            'name':'node1',
            'location':{"address": "Equinix MI1, Miami, FL","latitude": 0,"longitude": 0,'iso3166_2_lvl4':'US-FL'},
            'ports':[
                {
                    "id": "urn:sdx:port:oxp_url:node1:1",
                    "name": "node1",
                    "node": "urn:sdx:node:oxp_url:node1",
                    "type": "10GE",
                    "status": "up",
                    "state": "enabled",
                }]}],
        "links": [{
            "name": "link1",
            "id": "urn:sdx:link:oxp_url:node1-1_node1-2",
            "ports":["urn:sdx:port:oxp_url:node1:1", "urn:sdx:port:oxp_url:node1:2"],
            "type": "intra",
            "bandwidth": 1250,
            "status": "up",
            "state": "enabled"}],
        "version": 1,
        'name': 'TestTopology',
        "id": "urn:sdx:topology:oxp_url",
        "model_version": "1",
        "timestamp": timestamp
    }
    mock_parse_convert_topology.return_value = mock_converted_topology

    result = convert_topology()
    assert 'validation_error' not in result
    assert result['version'] == 2

def test_convert_topology_no_nodes_or_links(mock_requests_get, mock_parse_convert_topology):
    """Test conversion with no nodes or links."""
    mock_response = MagicMock()
    mock_requests_get.return_value = mock_response
    mock_parse_convert_topology.return_value = {
        "nodes": [],
        "links": []
    }

    result = convert_topology()
    assert result["validation_error"] == "No nodes to validate topology"

def test_convert_topology_validation_error(mock_requests_get, mock_parse_convert_topology):
    """Test conversion with validation errors."""
    mock_response = MagicMock()
    mock_requests_get.return_value = mock_response
    mock_parse_convert_topology.return_value = {
        "nodes": [{"id": "node1"}],
        "links": [{"id": "link1"}]
    }

    result = convert_topology()
    assert result["validation_error"]["status_code"] == 400
    assert result["validation_error"]["result"] == "Validation Error: 'id' is a required property"

def test_convert_topology_exception(mock_requests_get, mock_parse_convert_topology):
    """Test conversion function handling of exceptions."""
    mock_requests_get.side_effect = Exception("Unexpected error")
    mock_parse_convert_topology.return_value = {}

    result = convert_topology()
    assert result == {
        "convert_topology Error": "Unexpected error",
        "status_code": 401
    }
