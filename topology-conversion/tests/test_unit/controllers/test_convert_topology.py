import pytest

def test_get_kytos_nodes(parser):
    '''Test for method get_kytos_nodes'''
    nodes = list(parser.get_kytos_nodes())
    assert len(nodes) == 3
    assert nodes[0]["id"] == "aa:00:00:00:00:00:00:01"
    assert nodes[1]["id"] == "aa:00:00:00:00:00:00:02"
    assert nodes[2]["id"] == "aa:00:00:00:00:00:00:03"

def test_get_port_status(parser):
    '''Test for method get_port_status'''
    assert parser.get_port_status("UP") == "up"
    assert parser.get_port_status("down") == "down"
    assert parser.get_port_status("unknown") == "error"


def test_get_link_port_speed(parser):
    '''Test for method get_link_port_speed'''
    assert parser.get_link_port_speed("100GE") == 100
    assert parser.get_link_port_speed("50000000000") == 400
    assert parser.get_link_port_speed("unknown") == 0

def test_get_type_port_speed(parser):
    '''Test for method get_type_port_speed'''
    assert parser.get_type_port_speed("100GE") == "100GE"
    assert parser.get_type_port_speed("50000000000") == "400GE"
    assert parser.get_type_port_speed("unknown") == "Other"

def test_get_status(parser):
    '''Test for method get_status'''
    assert parser.get_status(True) == "up"
    assert parser.get_status(False) == "down"

def test_get_state(parser):
    '''Test for method get_state'''
    assert parser.get_state(True) == "enabled"
    assert parser.get_state(False) == "disabled"

def test_get_port_urn(parser):
    '''
    Tests for method get_port_urn
    Includes Error Handling to ensures that invalid inputs 
    are handled correctly by raising appropriate exceptions.
    '''
    urn = parser.get_port_urn("aa:00:00:00:00:00:00:01", "1")
    assert urn == "urn:sdx:port:oxp_url:Novi01:1"

    with pytest.raises(ValueError):
        parser.get_port_urn("", "1")

    with pytest.raises(ValueError):
        parser.get_port_urn("aa:00:00:00:00:00:00:01", -1)

def test_get_ports(parser):
    '''Test for method get_ports'''
    ports = parser.get_ports("Node1", {
        "interface1": {
            "port_number": 1,
            "metadata": {"port_name": "Port1"},
            "speed": "100GE",
            "active": True,
            "enabled": True,
            "id": "port1"
        }
    })
    assert len(ports) == 1
    assert ports[0]["id"] == "urn:sdx:port:oxp_url:Node1:1"
    assert ports[0]["name"] == "Port1"
    assert ports[0]["node"] == "urn:sdx:node:oxp_url:Node1"
    assert ports[0]["type"] == "100GE"
    assert ports[0]["status"] == "up"
    assert ports[0]["state"] == "enabled"
    assert ports[0]["mtu"] == 1500
    assert ports[0]["nni"] == ""

def test_get_kytos_nodes_names(parser):
    '''Test for method get_kytos_nodes_names'''
    names = parser.get_kytos_nodes_names()
    assert len(names) == 3
    assert names["aa:00:00:00:00:00:00:01"] == "Novi01"
    assert names["aa:00:00:00:00:00:00:02"] == "Novi02"
    assert names["aa:00:00:00:00:00:00:03"] == "Novi03"

def test_get_sdx_node(parser):
    '''Test for method get_sdx_node'''
    kytos_node = {
        "id": "switch1",
        "metadata": {"node_name": "Node1", "address": "192.168.0.1", "lat": "40.7128", "lng": "-74.0060"},
        "data_path": "switch1_data_path",
        "interfaces": {
            "interface1": {
                "id": "port1",
                "port_number": 1,
                "metadata": {"port_name": "Port1", "mtu": 1500},
                "speed": "100GE",
                "active": True,
                "enabled": True
            }
        },
        "enabled": True,
        "active": True
    }
    node = parser.get_sdx_node(kytos_node)
    assert node["name"] == "Node1"
    assert node["id"] == "urn:sdx:node:oxp_url:Node1"
    assert node["location"]["address"] == "192.168.0.1"
    assert node["location"]["latitude"] == 40.7128
    assert node["location"]["longitude"] == -74.0060
    assert node["status"] == "up"
    assert node["state"] == "enabled"

def test_get_sdx_nodes(parser):
    '''Test for method get_sdx_nodes'''
    nodes = parser.get_sdx_nodes()
    assert len(nodes) == 3
    assert nodes[0]["id"] == "urn:sdx:node:oxp_url:Novi01"
    assert nodes[1]["id"] == "urn:sdx:node:oxp_url:Novi02"
    assert nodes[2]["id"] == "urn:sdx:node:oxp_url:Novi03"

def test_get_sdx_link(parser):
    '''Test for method get_sdx_link'''
    kytos_link = {
        "endpoint_a": {
            "name": "Node1",
            "speed": "50GE",
            "port_number": 1
        },
        "endpoint_b": {
            "name": "Node2",
            "speed": "100GE",
            "port_number": 2
        },
        "status": "UP",
        "enabled": True
    }
    link = parser.get_sdx_link(kytos_link)
    assert link["name"] == "Node1_Node2"
    assert link["id"] == "urn:sdx:link:oxp_url:Node1_Node2"
    assert link["type"] == "intra"
    assert link["bandwidth"] == 100
    assert link["ports"] == ['urn:sdx:port:oxp_url:Node1:1', 'urn:sdx:port:oxp_url:Node2:2']

def test_get_sdx_links(parser):
    '''Test for method get_sdx_links'''
    links = parser.get_sdx_links()
    assert len(links) == 3
    assert links[0]["name"] == "Novi03-eth5_Novi02-eth5"
    assert links[1]["name"] == "Novi01-eth2_Novi02-eth2"
    assert links[2]["name"] == "Novi03-eth3_Novi01-eth3"

def test_parse_convert_topology(parser):
    '''Test for method parse_convert_topology'''
    topology = parser.parse_convert_topology()
    assert topology["model_version"] == '1'
    assert topology["version"] == 1
    assert len(topology["nodes"]) == 3

    assert topology['nodes'][0]['name'] == 'Novi01'
    assert topology['nodes'][1]['name'] == 'Novi02'
    assert topology['nodes'][2]['name'] == 'Novi03'

    assert topology['nodes'][0]['id'] == 'urn:sdx:node:oxp_url:Novi01'
    assert topology['nodes'][1]['id'] == 'urn:sdx:node:oxp_url:Novi02'
    assert topology['nodes'][2]['id'] == 'urn:sdx:node:oxp_url:Novi03'

    assert len(topology['nodes'][0]['ports']) == 3
    assert topology['nodes'][0]['ports'][0]['id'] == 'urn:sdx:port:oxp_url:Novi01:1'
    assert topology['nodes'][0]['ports'][0]['name'] == 'Novi01-eth1'
    assert topology['nodes'][0]['ports'][0]['node'] == 'urn:sdx:node:oxp_url:Novi01'
    assert topology['nodes'][0]['ports'][0]['nni'] == 'urn:sdx:port:tenet.ac.za:Novi06:1'

    assert topology['nodes'][0]['ports'][1]['id'] == 'urn:sdx:port:oxp_url:Novi01:2'
    assert topology['nodes'][0]['ports'][1]['name'] == 'Novi01-eth2'
    assert topology['nodes'][0]['ports'][1]['node'] == 'urn:sdx:node:oxp_url:Novi01'
    assert topology['nodes'][0]['ports'][1]['nni'] == ''
    
    assert topology['nodes'][0]['ports'][2]['id'] == 'urn:sdx:port:oxp_url:Novi01:3'
    assert topology['nodes'][0]['ports'][2]['name'] == 'Novi01-eth3'
    assert topology['nodes'][0]['ports'][2]['node'] == 'urn:sdx:node:oxp_url:Novi01'
    assert topology['nodes'][0]['ports'][2]['nni'] == ''
    
    assert len(topology['nodes'][1]['ports']) == 4
    assert topology['nodes'][1]['ports'][0]['id'] == 'urn:sdx:port:oxp_url:Novi02:4'
    assert topology['nodes'][1]['ports'][0]['name'] == 'Novi02-eth4'
    assert topology['nodes'][1]['ports'][0]['node'] == 'urn:sdx:node:oxp_url:Novi02'
    assert topology['nodes'][1]['ports'][0]['nni'] == 'urn:sdx:port:sax.net:Novi04:4'

    assert topology['nodes'][1]['ports'][1]['id'] == 'urn:sdx:port:oxp_url:Novi02:5'
    assert topology['nodes'][1]['ports'][1]['name'] == 'Novi02-eth5'
    assert topology['nodes'][1]['ports'][1]['node'] == 'urn:sdx:node:oxp_url:Novi02'
    assert topology['nodes'][1]['ports'][1]['nni'] == ''
    
    assert topology['nodes'][1]['ports'][2]['id'] == 'urn:sdx:port:oxp_url:Novi02:2'
    assert topology['nodes'][1]['ports'][2]['name'] == 'Novi02-eth2'
    assert topology['nodes'][1]['ports'][2]['node'] == 'urn:sdx:node:oxp_url:Novi02'
    assert topology['nodes'][1]['ports'][2]['nni'] == ''

    assert topology['nodes'][1]['ports'][3]['id'] == 'urn:sdx:port:oxp_url:Novi02:3'
    assert topology['nodes'][1]['ports'][3]['name'] == 'Novi02-eth3'
    assert topology['nodes'][1]['ports'][3]['node'] == 'urn:sdx:node:oxp_url:Novi02'
    assert topology['nodes'][1]['ports'][3]['nni'] == 'urn:sdx:port:tenet.ac.za:Novi06:3'

    assert len(topology['nodes'][2]['ports']) == 3
    assert topology['nodes'][2]['ports'][0]['id'] == 'urn:sdx:port:oxp_url:Novi03:1'
    assert topology['nodes'][2]['ports'][0]['name'] == 'Novi03-eth1'
    assert topology['nodes'][2]['ports'][0]['node'] == 'urn:sdx:node:oxp_url:Novi03'
    assert topology['nodes'][2]['ports'][0]['nni'] == 'urn:sdx:port:tenet.ac.za:Novi07:1'

    assert topology['nodes'][2]['ports'][1]['id'] == 'urn:sdx:port:oxp_url:Novi03:5'
    assert topology['nodes'][2]['ports'][1]['name'] == 'Novi03-eth5'
    assert topology['nodes'][2]['ports'][1]['node'] == 'urn:sdx:node:oxp_url:Novi03'
    assert topology['nodes'][2]['ports'][1]['nni'] == ''
    
    assert topology['nodes'][2]['ports'][2]['id'] == 'urn:sdx:port:oxp_url:Novi03:3'
    assert topology['nodes'][2]['ports'][2]['name'] == 'Novi03-eth3'
    assert topology['nodes'][2]['ports'][2]['node'] == 'urn:sdx:node:oxp_url:Novi03'
    assert topology['nodes'][2]['ports'][2]['nni'] == ''

    assert len(topology["links"]) == 3
    assert topology['links'][0]['name'] == 'Novi03-eth5_Novi02-eth5'
    assert topology['links'][0]['id'] == 'urn:sdx:link:oxp_url:Novi03-eth5_Novi02-eth5'
    assert topology['links'][0]['type'] == 'intra'
    assert topology['links'][0]['ports'] == ['urn:sdx:port:oxp_url:Novi03:5', 'urn:sdx:port:oxp_url:Novi02:5']

    assert topology['links'][1]['name'] == 'Novi01-eth2_Novi02-eth2'
    assert topology['links'][1]['id'] == 'urn:sdx:link:oxp_url:Novi01-eth2_Novi02-eth2'
    assert topology['links'][1]['type'] == 'intra'
    assert topology['links'][1]['ports'] == ['urn:sdx:port:oxp_url:Novi01:2', 'urn:sdx:port:oxp_url:Novi02:2']

    assert topology['links'][2]['name'] == 'Novi03-eth3_Novi01-eth3'
    assert topology['links'][2]['id'] == 'urn:sdx:link:oxp_url:Novi03-eth3_Novi01-eth3'
    assert topology['links'][2]['type'] == 'intra'
    assert topology['links'][2]['ports'] == ['urn:sdx:port:oxp_url:Novi03:3', 'urn:sdx:port:oxp_url:Novi01:3']

    assert topology["services"] == ["l2vpn-ptp"]

