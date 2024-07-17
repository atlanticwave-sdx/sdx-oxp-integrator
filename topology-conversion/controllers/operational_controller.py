""" Operational events controller """
import json
import os
import requests
OXPO_LINK = os.environ.get("OXPO_LINK")
OXP_TOPOLOGY_URL = os.environ.get("OXP_TOPOLOGY_URL")


def get_operational_event():
    """getting operational event"""
    response = requests.get(OXP_TOPOLOGY_URL, timeout=10)
    if response.status_code == 200:
        oxp_topology = response.json()
        result = oxp_topology["topology"]
        print("get_oxp_topology result: {result}")
        return result
    return {
            "error:": "Failed to retrieve data",
            "status_code:": response.status_code}


def get_topology_object(topology_object):
    """getting topology object"""
    url = OXP_TOPOLOGY_URL + topology_object
    response = requests.get(url, timeout=10)
    return response.json()


def post_topology_object(url, topology_object):
    """getting topology object"""
    oxp_url = OXP_TOPOLOGY_URL + url
    response = requests.post(oxp_url, json=topology_object, timeout=10)
    return response.json()


def json_reader(json_name):
    """Read and return json_file"""
    actual_dir = os.getcwd()
    json_data = actual_dir + "/" + json_name
    with open(json_data, encoding="utf8") as json_file:
        data = json.load(json_file)
        json_file.close()
    return data


def get_switch_enable(dp_id):
    """getting switch enable"""
    topology_object = {}
    if dp_id == "all":
        switches = get_topology_object("switches")
        if "switches" in switches:
            for key in switches["switches"].keys():
                dp_id = switches["switches"][key]["id"]
                url = "switches/" + dp_id + "/enable"
                post_topology_object(url, topology_object)
    else:
        url = "switches/" + dp_id + "/enable"
        post_topology_object(url, topology_object)
    return f"switch/enable/{dp_id}"


def get_switch_disable(dp_id):
    """getting switch disable"""
    topology_object = {}
    if dp_id == "all":
        switches = get_topology_object("switches")
        if "switches" in switches:
            for key in switches["switches"].keys():
                dp_id = switches["switches"][key]["id"]
                url = "switches/" + dp_id + "/disable"
                post_topology_object(url, topology_object)
    else:
        url = "switches/" + dp_id + "/disable"
        post_topology_object(url, topology_object)
    return f"switch/disable/{dp_id}"


def get_link_enable(dp_id):
    """getting link enable"""
    if dp_id == "all":
        links = json_reader(OXPO_LINK)
        for dpid, topology_object in links.items():
            print(dpid, topology_object)
            url = "interfaces/"+dpid+"/metadata"
            post_topology_object(url, topology_object)
    else:
        url = "links/" + dp_id + "/enable"
        topology_object = {}
        post_topology_object(url, topology_object)
    return f"link/enable/{dp_id}"


def get_link_disable(dp_id):
    """getting link disable"""
    if dp_id == "all":
        links = get_topology_object("links")
        if "links" in links:
            for key in links["links"].keys():
                dp_id = links["links"][key]["id"]
                url = "links/" + dp_id + "/disable"
                topology_object = {}
                post_topology_object(url, topology_object)
    else:
        url = "links/" + dp_id + "/disable"
        topology_object = {}
        post_topology_object(url, topology_object)