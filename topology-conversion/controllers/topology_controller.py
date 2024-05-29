""" topology controller """
import logging
import os
from sdx_topology_validator import validate

import requests
from models.error_message import ErrorMessage  # noqa: E501
from models.topology import Topology  # noqa: E501
from utils.util import get_timestamp

from controllers.convert_topology import ParseConvertTopology

logger = logging.getLogger(__name__)
OXP_TOPOLOGY_URL = os.environ.get("OXP_TOPOLOGY_URL")

topology_class = Topology()
topology_class.model_version = os.environ.get("MODEL_VERSION")
topology_class.name = os.environ.get("OXPO_NAME")
topology_class.version = 1
topology_class.topology_id = os.environ.get("OXPO_URL")
timestamp = get_timestamp()


def get_kytos_topology():
    """ getting kytos topology """
    response = requests.get(OXP_TOPOLOGY_URL, timeout=10)
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
        print("######################")
        print("## convert topology ##")
        print("######################")

        topology_converted = ParseConvertTopology(
            topology=get_kytos_topology(),
            version=topology_class.version,
            timestamp=timestamp,
            model_version=topology_class.model_version,
            oxp_name=topology_class.name,
            oxp_url=topology_class.topology_id,
        ).parse_convert_topology()
        validation_result = validate(topology_converted)
        print(validation_result)
        if validation_result.status_code == "200":
            return topology_converted
        return validation_result
    except Exception as err:  # pylint: disable=broad-except
        logger.info("validation Error, status code 401:{err}")
        result = {"Validation Error": err, "status_code": 401}
        return result
