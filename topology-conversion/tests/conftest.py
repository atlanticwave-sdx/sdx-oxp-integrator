""" conftest """
import json
import os
import pytest
from requests.models import Response

from controllers.convert_topology import ParseConvertTopology
from utils.util import get_timestamp

@pytest.fixture
def ampath_topology():
    """Build ampath topology json_data"""
    actual_dir = os.getcwd()
    ampath_data = actual_dir + "/topology-conversion/tests/ampath.json"
    with open(ampath_data, encoding="utf8") as json_file:
        data = json.load(json_file)
        json_file.close()
    return data

@pytest.fixture
def oxp_topology():
    """Build oxp topology json_data"""
    actual_dir = os.getcwd()
    ampath_data = actual_dir + "/topology-conversion/tests/oxp_topology.json"
    with open(ampath_data, encoding="utf8") as json_file:
        data = json.load(json_file)
        json_file.close()
    return data

@pytest.fixture
def parser(oxp_topology):
    '''Initializes the ParseConvertTopology instance with this mock data'''
    model_version = os.environ.get("MODEL_VERSION")
    name = os.environ.get("OXPO_NAME")
    version = 1
    topology_id = os.environ.get("OXPO_URL")
    timestamp = get_timestamp()
    converted_topology = ParseConvertTopology(
        topology=oxp_topology,
        version=version,
        timestamp=timestamp,
        model_version=model_version,
        oxp_name=name,
        oxp_url="oxp_url",
        topology_id=topology_id
    )
    return converted_topology

@pytest.fixture
def mock_parse_convert_topology(mocker):
    """Fixture to mock the ParseConvertTopology instance."""
    mock = None
    mock = mocker.patch.object(ParseConvertTopology, 'parse_convert_topology')
    return mock

@pytest.fixture
def mock_requests_get(mocker):
    """Fixture to mock requests.get."""
    return mocker.patch('requests.get')

@pytest.fixture
def mock_json_reader(mocker):
    """Fixture to mock json_reader function"""
    mocker.patch('controllers.operational_controller.json_reader', return_value={
        "switches": {"switch1": {"metadata": {"name": "switch1"}}},
        "interfaces": {"interface1": {"metadata": {"name": "interface1"}}},
        "evcs": {"evc1": {"name": "evc1"}},
        "vlans": {"vlan1": {"name": "vlan1"}}
    })

@pytest.fixture
def mock_requests(mocker):
    """Fixture to mock requests.get and requests.post"""
    def mock_get(url, timeout=10):
        response = Response()
        response.status_code = 200
        content = ""
        if url == "http://mock.url/topology/":
            content = {"topology": {"switches": {}, "links": {}}}
        elif url == "http://mock.url/topology/switches":
            content = {"switches": {}}
        elif url == "http://mock.url/topology/interfaces":
            content = {"interfaces": {}}
        elif url == "http://mock.url/topology/links":
            content = {"links": {}}
        elif url == "http://mock.url/topology/switches/switch1/metadata":
            content = {"metadata": {}}
        elif url == "http://mock.url/topology/interfaces/interface1/metadata":
            content = {"metadata": {}}
        elif url == "http://mock.url/topology/links/link1/metadata":
            content = {"metadata": {}}
        elif url == "http://mock.url/connection/evc":
            content = {"result": "success"}
        response._content = json.dumps(content).encode('utf-8')
        return response

    def mock_post(url, json=None, timeout=10):
        response = Response()
        response.status_code = 200
        response._content = globals()['json'].dumps({"result": "success"}).encode('utf-8')
        return response

    mocker.patch('requests.get', side_effect=mock_get)
    mocker.patch('requests.post', side_effect=mock_post)
