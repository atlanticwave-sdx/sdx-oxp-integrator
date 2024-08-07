""" topology controller """
import logging
import os

import requests
from controllers.convert_topology import ParseConvertTopology
from models.error_message import ErrorMessage  # noqa: E501
from models.topology import Topology  # noqa: E501
from sdx_topology_validator import validate
from utils.util import get_timestamp

logger = logging.getLogger(__name__)
OXP_TOPOLOGY_URL = os.environ.get("OXP_TOPOLOGY_URL")


topology_class = Topology()
topology_class.model_version = os.environ.get("MODEL_VERSION")
topology_class.name = os.environ.get("OXPO_NAME")
topology_class.version = 1
topology_class.topology_id = "urn:sdx:topology:" + os.environ.get("OXPO_URL")
topology_class.oxpo_url = os.environ.get("OXPO_URL")
timestamp = get_timestamp()


def get_oxp_topology():
    """getting oxp topology"""
    response = requests.get(OXP_TOPOLOGY_URL, timeout=10)
    if response.status_code == 200:
        oxp_topology = response.json()
        result = oxp_topology["topology"]
        logger.info("get_oxp_topology result: {result}")
        return result
    return {
            "error:": "Failed to retrieve data",
            "status_code:": response.status_code}


def convert_topology():
    """converting kytos to sdx topology"""
    try:
        topology = get_oxp_topology()
        converted_topology = ParseConvertTopology(
            topology=topology,
            version=topology_class.version,
            timestamp=timestamp,
            model_version=topology_class.model_version,
            oxp_name=topology_class.name,
            oxp_url=topology_class.oxpo_url,
            topology_id=topology_class.topology_id,
        ).parse_convert_topology()
        if not converted_topology["nodes"]:
            converted_topology["validation_error"] = "No nodes to validate topology"
        elif not converted_topology["links"]:
                converted_topology["validation_error"] = "No links to validate topology"
        else:
            validated_topology = validate(converted_topology)
            if validated_topology["status_code"] != "200":
                converted_topology["validation_error"] = validated_topology
            topology_class.nodes = converted_topology["nodes"]
            topology_class.links = converted_topology["links"]
            topology_class.version += 1
            converted_topology["version"] = topology_class.version
        return converted_topology
    except Exception as err:  # pylint: disable=broad-except
        logger.info("convert_topology Error, status code 401:{err}")
        result = {"convert_topology Error": err, "status_code": 401}
        return result
