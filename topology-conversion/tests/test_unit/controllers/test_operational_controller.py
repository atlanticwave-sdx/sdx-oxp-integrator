from unittest.mock import patch
from unittest.mock import MagicMock
import pytest

from controllers.operational_controller import (
    get_operational_event,
    get_topology_object,
    post_topology_object,
    get_connection_object,
    post_connection_object,
    json_reader,
    post_oxp_enable_all,
    post_oxp_disable_all,
    get_oxp_switches,
    get_oxp_switch_by_dpid,
    post_oxp_switch_enable,
    post_oxp_switch_disable,
    get_oxp_interfaces,
    get_oxp_interface_by_id,
    post_oxp_interface_enable,
    post_oxp_interface_disable,
    get_oxp_links,
    get_oxp_link_by_id,
    post_oxp_link_enable,
    get_oxp_evcs,
    post_oxp_evc_enable,
    post_oxp_vlan_enable,
    post_oxp_host_enable,
    post_oxp_link_disable
)

def test_get_operational_event(mock_requests):
    '''Test for method get_operational_event'''
    with patch('controllers.operational_controller.OXP_TOPOLOGY_URL', 'http://mock.url/topology/'):
        result = get_operational_event()
        assert result == {"switches": {}, "links": {}}

def test_get_operational_event_http_error(mock_requests):
    '''Test for get_operational_event handling HTTP errors'''
    with patch('controllers.operational_controller.requests.get',\
        MagicMock(return_value=MagicMock(status_code=500))):
        result = get_operational_event()
        assert result == {"error:": "Failed to retrieve data", "status_code:": 500}

def test_get_topology_object(mock_requests):
    '''Test for method get_topology_object'''
    with patch('controllers.operational_controller.OXP_TOPOLOGY_URL', 'http://mock.url/topology/'):
        result = get_topology_object("switches")
        assert result == {"switches": {}}

def test_post_topology_object(mock_requests):
    '''Test for method post_topology_object'''
    result = post_topology_object("switches", {"data": "test"})
    assert result == {"result": "success"}

def test_post_topology_object_empty_data(mock_requests):
    '''Test for post_topology_object with empty data'''
    result = post_topology_object("switches", {})
    assert result == {"result": "success"}

def test_get_connection_object(mock_requests):
    '''Test for method get_connection_object'''
    with patch('controllers.operational_controller.OXP_CONNECTION_URL', 'http://mock.url/connection/'):
        result = get_connection_object("evc")
        assert result == {"result": "success"}

def test_post_connection_object(mock_requests):
    '''Test for method post_connection_object'''
    result = post_connection_object("evc", {"data": "test"})
    assert result == {"result": "success"}

def test_post_oxp_enable_all(mock_requests):
    '''Test for method post_oxp_enable_all'''
    with patch('controllers.operational_controller.OXP_META_DATA', 'topology-conversion/ampath_metadata.json'), \
        patch('controllers.operational_controller.OXP_TOPOLOGY_URL', 'http://mock.url/topology/'):
        result = post_oxp_enable_all()
        assert result == {"links": {}}

def test_post_oxp_disable_all(mock_requests):
    '''Test for method post_oxp_disable_all'''
    with patch('controllers.operational_controller.OXP_TOPOLOGY_URL', 'http://mock.url/topology/'):
        result = post_oxp_disable_all()
        assert result == {"switches": {}}

def test_get_oxp_switches(mock_requests):
    '''Test for method get_oxp_switches'''
    with patch('controllers.operational_controller.OXP_TOPOLOGY_URL', 'http://mock.url/topology/'):
        result = get_oxp_switches()
        assert result == {"switches": {}}

def test_get_oxp_switch_by_dpid(mock_requests):
    '''Test for method get_oxp_switch_by_dpid'''
    with patch('controllers.operational_controller.OXP_TOPOLOGY_URL', 'http://mock.url/topology/'):
        result = get_oxp_switch_by_dpid("switch1")
        assert result == {"metadata": {}}

def test_json_reader_file_not_found():
    '''Test for json_reader when file does not exist'''
    with patch('controllers.operational_controller.os.getcwd', return_value='/fake/path'):
        with pytest.raises(FileNotFoundError):
            json_reader('non_existent_file.json')

def test_post_oxp_switch_enable(mock_requests):
    '''Test for method post_oxp_switch_enable'''
    result = post_oxp_switch_enable("switch1")
    assert result == "switches/switch1/enable"

def test_post_oxp_switch_enable_all(mock_json_reader, mock_requests):
    '''Test post_oxp_switch_enable with "all" parameter'''
    with patch('controllers.operational_controller.get_topology_object', \
               return_value={"switches": {"switch1": {"id": "switch1"}}}):
        result = post_oxp_switch_enable("all")
        assert result == "switches/switch1/enable"

def test_post_oxp_switch_disable(mock_requests):
    '''Test for method post_oxp_switch_disable'''
    result = post_oxp_switch_disable("switch1")
    assert result == "switches/switch1/disable"

def test_post_oxp_switch_disable_all(mock_json_reader, mock_requests):
    '''Test post_oxp_switch_disable with "all" parameter'''
    with patch('controllers.operational_controller.get_topology_object', \
               return_value={"switches": {"switch1": {"id": "switch1"}}}):
        result = post_oxp_switch_disable("all")
        assert result == "switches/switch1/disable"

def test_get_oxp_interfaces(mock_requests):
    '''Test for method get_oxp_interfaces'''
    with patch('controllers.operational_controller.OXP_TOPOLOGY_URL', 'http://mock.url/topology/'):
        result = get_oxp_interfaces()
        assert result == {"interfaces": {}}

def test_get_oxp_interface_by_id(mock_requests):
    '''Test for method get_oxp_interface_by_id'''
    with patch('controllers.operational_controller.OXP_TOPOLOGY_URL', 'http://mock.url/topology/'):
        result = get_oxp_interface_by_id("interface1")
        assert result == {"metadata": {}}

def test_post_oxp_interface_enable(mock_requests):
    '''Test for method post_oxp_interface_enable'''
    result = post_oxp_interface_enable("interface1")
    assert result == "interfaces/interface1/enable"

from unittest.mock import patch, MagicMock

def test_post_oxp_interface_enable_all(mock_requests):
    '''Test for post_oxp_interface_enable with "all" parameter to ensure all interfaces are enabled'''
    # Mock data to simulate response from get_topology_object
    mock_interfaces = {
        "interfaces": {
            "interface1": {"id": "interface1"},
            "interface2": {"id": "interface2"}
        }
    }
    
    with patch('controllers.operational_controller.get_topology_object', \
               return_value=mock_interfaces) as mock_get_topology, \
         patch('controllers.operational_controller.post_topology_object') as mock_post_topology:
        
        result = post_oxp_interface_enable("all")
        
        # Ensure get_topology_object was called with the correct parameter
        mock_get_topology.assert_called_once_with("interfaces")
        
        # Ensure post_topology_object was called for each interface with the correct URL and data
        mock_post_topology.assert_any_call("interfaces/interface1/enable", {})
        mock_post_topology.assert_any_call("interfaces/interface2/enable", {})
        
        # Check the return value
        assert result == "interfaces/interface2/enable"

def test_post_oxp_interface_disable(mock_requests):
    '''Test for method post_oxp_interface_disable'''
    result = post_oxp_interface_disable("interface1")
    assert result == "interfaces/interface1/disable"
from unittest.mock import patch, MagicMock

def test_post_oxp_interface_disable_all(mock_requests):
    '''Test for post_oxp_interface_disable with "all" parameter to ensure all interfaces are disabled'''
    # Mock data to simulate response from get_topology_object
    mock_interfaces = {
        "interfaces": {
            "interface1": {"id": "interface1"},
            "interface2": {"id": "interface2"}
        }
    }
    
    with patch('controllers.operational_controller.get_topology_object', \
               return_value=mock_interfaces) as mock_get_topology, \
         patch('controllers.operational_controller.post_topology_object') as mock_post_topology:
        
        result = post_oxp_interface_disable("all")
        
        # Ensure get_topology_object was called with the correct parameter
        mock_get_topology.assert_called_once_with("interfaces")
        
        # Ensure post_topology_object was called for each interface with the correct URL and data
        mock_post_topology.assert_any_call("interfaces/interface1/disable", {})
        mock_post_topology.assert_any_call("interfaces/interface2/disable", {})
        
        # Check the return value
        assert result == "interfaces/interface2/disable"

def test_get_oxp_links(mock_requests):
    '''Test for method get_oxp_links'''
    with patch('controllers.operational_controller.OXP_TOPOLOGY_URL', 'http://mock.url/topology/'):
        result = get_oxp_links()
        assert result == {"links": {}}

def test_get_oxp_link_by_id(mock_requests):
    '''Test for method get_oxp_link_by_id'''
    with patch('controllers.operational_controller.OXP_TOPOLOGY_URL', 'http://mock.url/topology/'):
        result = get_oxp_link_by_id("link1")
        assert result == {"metadata": {}}

def test_post_oxp_link_enable(mock_requests):
    '''Test for method post_oxp_link_enable'''
    result = post_oxp_link_enable("link1")
    assert result == "link/enable/link1"

def test_post_oxp_link_enable_all(mock_requests):
    '''Test for post_oxp_link_enable with "all" parameter to ensure all links are enabled'''
    mock_links = {
        "links": {
            "link1": {"id": "link1"},
            "link2": {"id": "link2"}
        }
    }
    
    with patch('controllers.operational_controller.get_oxp_links', \
               return_value=mock_links) as mock_get_links, \
         patch('controllers.operational_controller.post_topology_object') as mock_post_topology, \
            patch('controllers.operational_controller.OXP_META_DATA', 'topology-conversion/ampath_metadata.json'):
        result = post_oxp_link_enable("all")
        
        # Ensure get_oxp_links was called to retrieve the links
        mock_get_links.assert_called_once()
        
        # Ensure post_topology_object was called for each link with the correct URL and data
        mock_post_topology.assert_any_call("links/link1/enable", {})
        mock_post_topology.assert_any_call("links/link2/enable", {})
        
        # Check the return value
        assert result == "link/enable/all"

def test_get_oxp_evcs(mock_requests):
    '''Test for method get_oxp_evcs'''
    with patch('controllers.operational_controller.OXP_CONNECTION_URL', 'http://mock.url/connection/'):
        result = get_oxp_evcs()
        assert result == {"result": "success"}

def test_post_oxp_evc_enable(mock_json_reader, mock_requests):
    '''Test for method post_oxp_evc_enable'''
    result = post_oxp_evc_enable()
    assert result == "evc/enable"

def test_post_oxp_vlan_enable(mock_json_reader, mock_requests):
    '''Test for method post_oxp_vlan_enable'''
    result = post_oxp_vlan_enable()
    assert result == "evc/vlan/enable"

def test_post_oxp_host_enable(mock_requests):
    '''Test for method post_oxp_host_enable'''
    result = post_oxp_host_enable()
    assert result == "host/enable"

def test_post_oxp_link_disable(mock_requests):
    '''Test for method post_oxp_link_disable'''
    result = post_oxp_link_disable("link1")
    assert result == "links/link1/disable"

def test_post_oxp_link_disable_all(mock_requests):
    '''Test for post_oxp_link_disable with "all" parameter to ensure all links are disabled'''
    mock_links = {
        "links": {
            "link1": {"id": "link1"},
            "link2": {"id": "link2"}
        }
    }
    
    with patch('controllers.operational_controller.get_topology_object', \
               return_value=mock_links) as mock_get_topology, \
         patch('controllers.operational_controller.post_topology_object') as mock_post_topology:
        
        result = post_oxp_link_disable("all")
        
        # Ensure get_topology_object was called with the correct parameter
        mock_get_topology.assert_called_once_with("links")
        
        # Ensure post_topology_object was called for each link with the correct URL and data
        mock_post_topology.assert_any_call("links/link1/disable", {})
        mock_post_topology.assert_any_call("links/link2/disable", {})
        
        # Check the return value
        assert result == "links/link2/disable"
