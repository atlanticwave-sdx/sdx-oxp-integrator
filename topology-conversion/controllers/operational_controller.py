""" Operational events controller """
import os
import requests
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
    print("############################################")
    print("######### get_topology_object #############")
    print("######### %s #############", url)
    print("############################################")
    response = requests.get(url, timeout=10)
    return response.json()


def post_topology_object(topology_object):
    """getting topology object"""
    url = OXP_TOPOLOGY_URL + topology_object
    response = requests.post(url, timeout=10)
    print("############################################")
    print("######### post_topology_object #############")
    print("######### %s #############", url)
    print("############################################")
    print(response.json())
    print(response.status_code)
    return response.json()


def get_switch_enable(dp_id):
    """getting switch enable"""
    if dp_id == "all":
        switches = get_topology_object("switches")
        print("############################################")
        print("######### switches #############")
        print("######### %s #############", switches)
        print("############################################")
        if "switches" in switches:
            for key in switches["switches"].keys():
                dp_id = switches["switches"][key]["id"]
                topology_object = "switches/" + dp_id + "/enable"
                switch_enable = post_topology_object(topology_object)
                print(switch_enable)
    else:
        topology_object = "switches/" + dp_id + "/enable"
        switch_enable = post_topology_object(topology_object)
        print(switch_enable)

    return f"switch/enable/{dp_id}"


def get_switch_disable(dp_id):
    """getting switch disable"""
    if dp_id == "all":
        switches = get_topology_object("switches")
        if "switches" in switches:
            for key in switches["switches"].keys():
                dp_id = switches["switches"][key]["id"]
                topology_object = "switches/" + dp_id + "/disable"
                switch_disable = post_topology_object(topology_object)
                print(switch_disable)
    else:
        topology_object = "switches/" + dp_id + "/disable"
        switch_disable = post_topology_object(topology_object)
        print(switch_disable)

    return f"switch/disable/{dp_id}"


def get_link_enable(dp_id):
    """getting link enable"""
    if dp_id == "all":
        links = get_topology_object("links")
        print("############################################")
        print("######### links #############")
        print("######### %s #############", links)
        print("############################################")
        if "links" in links:
            for key in links["links"].keys():
                dp_id = links["links"][key]["id"]
                topology_object = "links/" + dp_id + "/enable"
                link_enable = post_topology_object(topology_object)
                print(link_enable)
    else:
        topology_object = "links/" + dp_id + "/enable"
        link_enable = post_topology_object(topology_object)
        print(link_enable)

    return f"link/enable/{dp_id}"


def get_link_disable(dp_id):
    """getting link disable"""
    if dp_id == "all":
        links = get_topology_object("links")
        if "links" in links:
            for key in links["links"].keys():
                dp_id = links["links"][key]["id"]
                topology_object = "links/" + dp_id + "/disable"
                link_disable = post_topology_object(topology_object)
                print(link_disable)
    else:
        topology_object = "links/" + dp_id + "/disable"
        link_disable = post_topology_object(topology_object)
        print(link_disable)
