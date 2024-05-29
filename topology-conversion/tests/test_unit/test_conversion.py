""" api test """

import os
from sdx_topology_validator import validate
from utils.util import get_timestamp
from controllers.convert_topology import ParseConvertTopology


def test_ampath_topology(ampath_topology):
    """ test kytos ampath data conversion """
    oxp_topology_urn = os.environ.get("OXP_TOPOLOGY_URN")
    model_version = os.environ.get("MODEL_VERSION")
    name = os.environ.get("OXPO_NAME")
    version = 1
    topology_id = oxp_topology_urn + os.environ.get("OXPO_URL")
    timestamp = get_timestamp()
    topology_converted = ParseConvertTopology(
            topology=ampath_topology,
            version=version,
            timestamp=timestamp,
            model_version=model_version,
            oxp_name=name,
            oxp_url=topology_id,
            ).parse_convert_topology()
    print(topology_converted)
    assert topology_converted["status_code"] == 200
