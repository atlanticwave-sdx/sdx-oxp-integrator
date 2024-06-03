""" api test """

import os

from controllers.convert_topology import ParseConvertTopology
from sdx_topology_validator import validate
from utils.util import get_timestamp


def test_ampath_topology(ampath_topology):
    """test kytos ampath data conversion"""
    model_version = os.environ.get("MODEL_VERSION")
    name = os.environ.get("OXPO_NAME")
    version = 1
    topology_id = os.environ.get("OXPO_URL")
    timestamp = get_timestamp()
    converted_topology = ParseConvertTopology(
        topology=ampath_topology,
        version=version,
        timestamp=timestamp,
        model_version=model_version,
        oxp_name=name,
        oxp_url=topology_id,
    ).parse_convert_topology()
    validated_topology = validate(converted_topology)
    assert validated_topology["status_code"] == 200
