import connexion
import requests
import logging
import os
from typing import Dict
from controllers.convert_topology import ParseConvertTopology
from util import get_timestamp
from models.error_message import ErrorMessage  # noqa: E501
from models.topology import Topology  # noqa: E501

logger = logging.getLogger(__name__)
OXP_TOPOLOGY_URL = os.environ.get("OXP_TOPOLOGY_URL")
SDX_TOPOLOGY_VALIDATOR = os.environ.get("SDX_TOPOLOGY_VAIDATOR")
MODEL_VERSION = os.environ.get("MODEL_VERSION")
OXPO_NAME = os.environ.get("OXPO_NAME")
OXPO_URL = os.environ.get("OXPO_URL")


def get_kytos_topology():
    response = requests.get(OXP_TOPOLOGY_URL)
    if response.status_code == 200:
        kytos_topology = response.json()
        result = kytos_topology["topology"]
        logger.info("get_kytos_topology result:", result)
        return result
    else:
        print("Failed to retrieve data. Status code:", response.status_code)

def convert_topology():
    try:

        topology_converted = ParseConvertTopology(
            topology=get_kytos_topology(),
            version= 1,
            timestamp=get_timestamp(),
            model_version=MODEL_VERSION,
            oxp_name=OXPO_NAME,
            oxp_url=OXPO_URL,
            ).parse_convert_topology()
        return topology_converted
        # return {"result": topology_converted, "status_code": 200}
    except Exception as err:
        logger.info("validation Error, status code 401:", err)
        return {"result": "Validation Error", "status_code": 401}

