""" topology controller """
import logging
import os

import requests
from models.error_message import ErrorMessage  # noqa: E501
from models.topology import Topology  # noqa: E501
from utils.util import get_timestamp

from controllers.convert_topology import ParseConvertTopology

logger = logging.getLogger(__name__)
OXP_TOPOLOGY_URL = os.environ.get("OXP_TOPOLOGY_URL")
SDX_TOPOLOGY_VALIDATOR = os.environ.get("SDX_TOPOLOGY_VAIDATOR")

topology_class = Topology()
topology_class.model_version = os.environ.get("MODEL_VERSION")
topology_class.name = os.environ.get("OXPO_NAME")
topology_class.version = 0
OXPO_URL = os.environ.get("OXPO_URL")


def get_kytos_topology():
    """ getting kytos topology """
    response = requests.get(OXP_TOPOLOGY_URL)
    if response.status_code == 200:
        kytos_topology = response.json()
        result = kytos_topology["topology"]
        logger.info("get_kytos_topology result: {result}")
        return result
    return {"error:": "Failed to retrieve data",
            "status_code:": response.status_code}


def convert_topology():
    """ converting kytos to sdx topology """
    try:
        topology_attrs = vars(Topology())
        print("######################")
        print("## convert topology ##")
        print("######################")
        print(list(item for item in topology_attrs.items()))
        print(topology_class.topology_id)
        print(topology_class.name)
        print(topology_class.version)
        print(topology_class.model_version)
        print(topology_class.time_stamp)
        print(topology_class.nodes)
        print(topology_class.links)

        topology_converted = ParseConvertTopology(
            topology=get_kytos_topology(),
            version=topology_class.version,
            timestamp=get_timestamp(),
            model_version=topology_class.model_version,
            oxp_name=topology_class.name,
            oxp_url=OXPO_URL,
        ).parse_convert_topology()
        return topology_converted
    except Exception as err:
        logger.info("validation Error, status code 401:{err}")
        return {"result": "Validation Error {err}", "status_code": 401}
