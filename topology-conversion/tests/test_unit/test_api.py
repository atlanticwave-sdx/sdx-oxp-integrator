""" api test """
from controllers.topology_controller import convert_topology


def test_ampath_data(mocker, ampath_data):
    """ test kytos ampath data conversion """
    get_kytos_topology_mock = mocker.path("get_kytos_topology")
    get_kytos_topology_mock.result = ampath_data
    topology_converted = convert_topology()
    assert topology_converted.status_code == "200"
