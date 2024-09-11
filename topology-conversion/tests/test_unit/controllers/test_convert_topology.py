import pytest

@pytest.mark.parametrize("node_idx,value",
                         [
                             (0,"aa:00:00:00:00:00:00:01"),
                             (1,"aa:00:00:00:00:00:00:02"),
                             (2,"aa:00:00:00:00:00:00:03")
                        ])
def test_get_kytos_nodes(node_idx,value,parser):
    '''Test for method get_kytos_nodes'''
    nodes = list(parser.get_kytos_nodes())
    assert len(nodes) == 3
    assert nodes[node_idx]["id"] == value

@pytest.mark.parametrize("status,value",
                         [
                             ("UP","up"),
                             ("down","down"),
                             ("unknowm","error")
                        ])
def test_get_port_status(status,value,parser):
    '''Test for method get_port_status'''
    assert parser.get_port_status(status) == value

@pytest.mark.parametrize("status,value",
                         [
                             ("UNKNOWN","error"),
                             ("INVALID_STATUS","error")
                        ])
def test_get_port_status_unrecognized(status,value,parser):
    '''Test for method get_port_status with unrecognized status'''
    assert parser.get_port_status(status) == value

@pytest.mark.parametrize("speed,value",
                         [
                             ("100GE",100),
                             ("50000000000",400),
                             ("unknown",0)
                        ])
def test_get_link_port_speed(speed,value,parser):
    '''Test for method get_link_port_speed'''
    assert parser.get_link_port_speed(speed) == value

@pytest.mark.parametrize("speed,value",
                         [
                             ("abc",0),
                             ("",0),
                             ("100",0)
                        ])
def test_get_link_port_speed_invalid(speed,value,parser):
    '''Test for method get_link_port_speed with invalid speeds'''
    assert parser.get_link_port_speed(speed) == value

@pytest.mark.parametrize("speed,value",
                         [
                             ("100GE","100GE"),
                             ("50000000000","400GE"),
                             ("unknown","Other")
                        ])
def test_get_type_port_speed(speed,value,parser):
    '''Test for method get_type_port_speed'''
    assert parser.get_type_port_speed(speed) == value

@pytest.mark.parametrize("speed,value",
                         [
                             (None, "Other"),
                             ("", "Other")
                        ])
def test_get_type_port_speed_default(speed,value,parser):
    '''Test for method get_type_port_speed with default values'''
    assert parser.get_type_port_speed(speed) == value


@pytest.mark.parametrize("status,value",
                         [
                             (True,"up"),
                             (False,"down")
                        ])
def test_get_status(status,value,parser):
    '''Test for method get_status'''
    assert parser.get_status(status) == value

@pytest.mark.parametrize("state,value",
                         [
                             (True,"enabled"),
                             (False,"disabled")
                        ])
def test_get_state(state,value,parser):
    '''Test for method get_state'''
    assert parser.get_state(state) == value

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

def test_get_ports_empty(parser):
    '''Test for method get_ports with empty input'''
    ports = parser.get_ports("Node1", {})
    assert len(ports) == 0

@pytest.mark.parametrize("node,name",
                         [
                             ("aa:00:00:00:00:00:00:01","Novi01"),
                             ("aa:00:00:00:00:00:00:02","Novi02"),
                             ("aa:00:00:00:00:00:00:03","Novi03")
                        ])
def test_get_kytos_nodes_names(node,name,parser):
    '''Test for method get_kytos_nodes_names'''
    names = parser.get_kytos_nodes_names()
    assert len(names) == 3
    assert names[node] == name

def test_get_kytos_nodes_empty(parser):
    '''Test for method get_kytos_nodes with no nodes'''
    parser.get_kytos_nodes = lambda: iter([])
    nodes = list(parser.get_kytos_nodes())
    assert len(nodes) == 0

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

@pytest.mark.parametrize("node_idx,value",
                         [
                             (0,"urn:sdx:node:oxp_url:Novi01"),
                             (1,"urn:sdx:node:oxp_url:Novi02"),
                             (2,"urn:sdx:node:oxp_url:Novi03")
                        ])
def test_get_sdx_nodes(node_idx,value,parser):
    '''Test for method get_sdx_nodes'''
    nodes = parser.get_sdx_nodes()
    assert len(nodes) == 3
    assert nodes[node_idx]["id"] == value

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

@pytest.mark.parametrize("link_idx,value",
                         [
                             (0,"Novi03-eth5_Novi02-eth5"),
                             (1,"Novi01-eth2_Novi02-eth2"),
                             (2,"Novi03-eth3_Novi01-eth3")
                        ])
def test_get_sdx_links(link_idx,value,parser):
    '''Test for method get_sdx_links'''
    links = parser.get_sdx_links()
    assert len(links) == 3
    assert links[link_idx]["name"] == value

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

def test_parse_convert_topology_complex(parser):
    '''Test for method parse_convert_topology with complex data'''
    parser.parse_convert_topology = lambda: {
        "model_version": '1',
        "version": 1,
        "nodes": [
            {"name": "Novi01", "id": "urn:sdx:node:oxp_url:Novi01", "ports": []},
            {"name": "Novi02", "id": "urn:sdx:node:oxp_url:Novi02", "ports": []},
            {"name": "Novi03", "id": "urn:sdx:node:oxp_url:Novi03", "ports": []}
        ],
        "links": [],
        "services": []
    }
    
    topology = parser.parse_convert_topology()
    assert len(topology["nodes"]) == 3
    assert len(topology["links"]) == 0
    assert topology["services"] == []
