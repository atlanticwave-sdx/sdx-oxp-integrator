import os
import pytest
from unittest.mock import patch

from controllers.operational_controller import (
    get_operational_event,
    get_topology_object,
    post_topology_object,
    get_connection_object,
    post_connection_object,
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

def test_get_topology_object(mock_requests):
    '''Test for method get_topology_object'''
    with patch('controllers.operational_controller.OXP_TOPOLOGY_URL', 'http://mock.url/topology/'):
        result = get_topology_object("switches")
        assert result == {"switches": {}}

def test_post_topology_object(mock_requests):
    '''Test for method post_topology_object'''
    result = post_topology_object("switches", {"data": "test"})
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

def test_post_oxp_switch_enable(mock_requests):
    '''Test for method post_oxp_switch_enable'''
    result = post_oxp_switch_enable("switch1")
    assert result == "switches/switch1/enable"

def test_post_oxp_switch_disable(mock_requests):
    '''Test for method post_oxp_switch_disable'''
    result = post_oxp_switch_disable("switch1")
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

def test_post_oxp_interface_disable(mock_requests):
    '''Test for method post_oxp_interface_disable'''
    result = post_oxp_interface_disable("interface1")
    assert result == "interfaces/interface1/disable"

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

