""" Operational events controller """
import json
import os, time
import requests

OXP_META_DATA = os.environ.get("OXPO_METADATA")
OXP_TOPOLOGY_URL = os.environ.get("OXP_TOPOLOGY_URL")
OXP_CONNECTION_URL = os.environ.get("OXP_CONNECTION_URL")


def get_operational_event():
    """Get operational event from OXP topology URL"""
    response = requests.get(OXP_TOPOLOGY_URL, timeout=10)
    if response.status_code == 200:
        oxp_topology = response.json()
        result = oxp_topology["topology"]
        return result
    return {
            "error:": "Failed to retrieve data",
            "status_code:": response.status_code}


def get_topology_object(topology_object):
    """Get specific  topology object from OXP"""
    url = OXP_TOPOLOGY_URL + topology_object
    response = requests.get(url, timeout=10)
    return response.json()


def post_topology_object(url, topology_object):
    """Post topology object to OXP"""
    oxp_url = f"{OXP_TOPOLOGY_URL}{url}"
    response = requests.post(oxp_url, json=topology_object, timeout=10)
    return response.json()


def get_connection_object(connection_object):
    """Get specific connection object from OXP"""
    url = OXP_CONNECTION_URL + connection_object
    response = requests.get(url, timeout=10)
    return response.json()


def post_connection_object(url, connection_object):
    """Post connection object to OXP"""
    oxp_url = f"{OXP_CONNECTION_URL}{url}"
    response = requests.post(oxp_url, json=connection_object, timeout=10)
    return response.json()


def json_reader(json_name):
    """Read and return JSON file"""
    actual_dir = os.getcwd()
    json_data = actual_dir + "/" + json_name
    with open(json_data, encoding="utf8") as json_file:
        data = json.load(json_file)
        json_file.close()
    return data


def post_oxp_enable_all():
    """Enable all switches, interfaces, and links"""
    post_oxp_switch_enable("all")
    time.sleep(15)
    post_oxp_interface_enable("all")
    time.sleep(15)
    post_oxp_link_enable("all")
    return get_oxp_links()


def post_oxp_disable_all():
    """Disable all switches, interfaces, and links"""
    post_oxp_link_disable("all")
    post_oxp_interface_disable("all")
    post_oxp_switch_disable("all")
    return get_oxp_switches()


def get_oxp_switches():
    """Get all switches"""
    return get_topology_object("switches")


def get_oxp_switch_by_dpid(dp_id):
    """Get switch by dpid """
    topology_object = f"switches/{dp_id}/metadata"
    return get_topology_object(topology_object)


def post_oxp_switch_enable(dp_id):
    """Enable switch by DPID or all switches"""
    topology_object = {}
    if dp_id == "all":
        metadata = json_reader(OXP_META_DATA)
        for dpid, topology_object in metadata.get("switches",{}).items():
            url = f"switches/{dpid}/metadata"
            post_topology_object(url, topology_object)
        switches = get_topology_object("switches")
        for switch in switches.get("switches", {}).values():
            dp_id = switch["id"]
            url = f"switches/{dp_id}/enable"
            post_topology_object(url, topology_object)

            url = f"switches/{dp_id}/metadata"
    else:
        url = f"switches/{dp_id}/enable"
        post_topology_object(url, topology_object)
    return f"switches/{dp_id}/enable"


def post_oxp_switch_disable(dp_id):
    """Disable switch by DPID or all switches"""
    topology_object = {}
    if dp_id == "all":
        switches = get_topology_object("switches")
        for switch in switches.get("switches", {}).values():
            dp_id = switch["id"]
            url = f"switches/{dp_id}/disable"
            post_topology_object(url, topology_object)
    else:
        url = f"switches/{dp_id}/disable"
        post_topology_object(url, topology_object)
    return f"switches/{dp_id}/disable"


def get_oxp_interfaces():
    """Get all interfaces """
    return get_topology_object("interfaces")


def get_oxp_interface_by_id(dp_id):
    """Get interface by id"""
    topology_object = f"interfaces/{dp_id}/metadata"
    return get_topology_object(topology_object)


def post_oxp_interface_enable(dp_id):
    """Enable interface by ID or all Interfaces"""
    topology_object = {}
    if dp_id == "all":
        interfaces = get_topology_object("interfaces")
        for interface in interfaces.get("interfaces", {}).values():
            dp_id = interface["id"]
            url = f"interfaces/{dp_id}/enable"
            post_topology_object(url, topology_object)
    else:
        url = f"interfaces/{dp_id}/enable"
        post_topology_object(url, topology_object)
    return f"interfaces/{dp_id}/enable"


def post_oxp_interface_disable(dp_id):
    """Disable interface by ID or all interfaces"""
    topology_object = {}
    if dp_id == "all":
        interfaces = get_topology_object("interfaces")
        for interface in interfaces.get("interfaces", {}).values():
            dp_id = interface["id"]
            url = f"interfaces/{dp_id}/disable"
            post_topology_object(url, topology_object)
    else:
        url = f"interfaces/{dp_id}/disable"
        post_topology_object(url, topology_object)
    return f"interfaces/{dp_id}/disable"


def get_oxp_links():
    """Get all links"""
    return get_topology_object("links")


def get_oxp_link_by_id(dp_id):
    """Get link by ID"""
    topology_object = f"links/{dp_id}/metadata"
    return get_topology_object(topology_object)


def post_oxp_link_enable(dp_id):
    """Enable link by ID or all links"""
    if dp_id == "all":
        metadata = json_reader(OXP_META_DATA)
        for dpid, topology_object in metadata.get("interfaces",{}).items():
            url = f"interfaces/{dpid}/metadata"
            post_topology_object(url, topology_object)
        for link in get_oxp_links().get("links", {}).keys():
            url = f"links/{link}/enable"
            post_topology_object(url, {})
    else:
        url = f"links/{dp_id}/enable"
        post_topology_object(url, {})
    return f"link/enable/{dp_id}"


def get_oxp_evcs():
    """Get all EVCs"""
    return get_connection_object("evc")


def post_oxp_evc_enable():
    """Enable Ethernet Network Connection"""
    metadata = json_reader(OXP_META_DATA)
    for dpid, connection_object in metadata.get("evcs",{}).items():
        url = f"evc/"
        post_connection_object(url, connection_object)
    return f"evc/enable"


def post_oxp_vlan_enable():
    """Enable Ethernet Network Connection VLAN translation"""
    metadata = json_reader(OXP_META_DATA)
    for dpid, connection_object in metadata.get("vlans",{}).items():
        url = f"mef_eline/v2/evc/"
        post_connection_object(url, connection_object)
    return f"evc/vlan/enable"


def post_oxp_host_enable():
    """Enable Host Configuration"""
    return f"host/enable"


def post_oxp_link_disable(dp_id):
    """Disable link by ID or all links"""
    if dp_id == "all":
        links = get_topology_object("links")
        for link in links.get("links", {}).values():
            dp_id = link["id"]
            url = f"links/{dp_id}/disable"
            post_topology_object(url, {})
    else:
        url = f"links/{dp_id}/disable"
        post_topology_object(url, {})
    return f"links/{dp_id}/disable"
