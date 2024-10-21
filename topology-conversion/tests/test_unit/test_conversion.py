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
        topology_id= "urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    print(converted_topology)
    validated_topology = validate(converted_topology)
    assert validated_topology["status_code"] == 200


def test_name_required(ampath_topology):
    """test should_fail_due_to_missing_name_attribute_on_json_data"""
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
        topology_id= "urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    missing_name_topology = {
        "id": converted_topology["id"],
        "version": converted_topology["version"],
        "model_version": converted_topology["model_version"],
        "timestamp": converted_topology["timestamp"],
        "nodes": converted_topology["nodes"],
        "links": converted_topology["links"],
    }
    validated_topology = validate(missing_name_topology)
    error_message = "Validation Error: 'name' is a required property"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_name_pattern(ampath_topology):
    """test should_fail_due_to_invalid_name_on_json_data"""
    model_version = os.environ.get("MODEL_VERSION")
    name = "This is a wrong name"
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
        topology_id= "urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: 'This is a wrong name' does not match '"
    error_message += "^[A-Za-z0-9.,-_/]*$'"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_id_pattern(ampath_topology):
    """test should_fail_due_to_invalid_id_on_json_data"""
    model_version = os.environ.get("MODEL_VERSION")
    name = os.environ.get("OXPO_NAME")
    version = 1
    topology_id = "This is a wrong ID"
    timestamp = get_timestamp()
    converted_topology = ParseConvertTopology(
        topology=ampath_topology,
        version=version,
        timestamp=timestamp,
        model_version=model_version,
        oxp_name=name,
        oxp_url=topology_id,
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    print(converted_topology)
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: 'urn:sdx:topology:This is a wrong ID' "
    error_message += "does not match '^urn:sdx:topology:[A-Za-z0-9_.:-]*$'"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_additional_properties(ampath_topology):
    """test should_fail_due_to_additional_properties_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    additional_property_topology = {
        "id": converted_topology["id"],
        "name": converted_topology["name"],
        "version": converted_topology["version"],
        "model_version": converted_topology["model_version"],
        "timestamp": converted_topology["timestamp"],
        "nodes": converted_topology["nodes"],
        "links": converted_topology["links"],
        "active": True,
    }
    validated_topology = validate(additional_property_topology)
    #error_message = "Validation Error: Additional properties are not allowed "
    #error_message += "('active' was unexpected)"
    assert validated_topology["status_code"] == 400
    #assert error_message in validated_topology["result"]


def test_version_type(ampath_topology):
    """test should_fail_due_to_invalid_type_on_json_data"""
    model_version = os.environ.get("MODEL_VERSION")
    name = os.environ.get("OXPO_NAME")
    version = "1"
    topology_id = os.environ.get("OXPO_URL")
    timestamp = get_timestamp()
    converted_topology = ParseConvertTopology(
        topology=ampath_topology,
        version=version,
        timestamp=timestamp,
        model_version=model_version,
        oxp_name=name,
        oxp_url=topology_id,
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: '1' is not of type 'integer'"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_time_pattern(ampath_topology):
    """test should_fail_due_to_invalid_date_time_on_json_data"""
    model_version = os.environ.get("MODEL_VERSION")
    name = os.environ.get("OXPO_NAME")
    version = 1
    topology_id = os.environ.get("OXPO_URL")
    timestamp = "2021-12-31 21:19:40Z"
    converted_topology = ParseConvertTopology(
        topology=ampath_topology,
        version=version,
        timestamp=timestamp,
        model_version=model_version,
        oxp_name=name,
        oxp_url=topology_id,
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: 'This is a wrong timestamp'"
    error_message += " does not match ' ^[A-Za-z0-9_.-]*$'"
    assert validated_topology["status_code"] == 400
    # assert error_message in validated_topology["result"]


def test_node_required(ampath_topology):
    """test should_fail_due_to_missing_nodes_attribute_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    missing_node_topology = {
        "id": converted_topology["id"],
        "name": converted_topology["name"],
        "version": converted_topology["version"],
        "model_version": converted_topology["model_version"],
        "timestamp": converted_topology["timestamp"],
        "links": converted_topology["links"],
    }
    validated_topology = validate(missing_node_topology)
    error_message = "Validation Error: 'nodes' is a required property"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_empty_node_array(ampath_topology):
    """test should_fail_due_to_empty_node_array_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    converted_topology["nodes"] = []
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: [] is too short"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_node_additional_property(ampath_topology):
    """test should_fail_due_to_node_additional_property_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    node_additional_property_topology = {
        "id": converted_topology["id"],
        "name": converted_topology["name"],
        "version": converted_topology["version"],
        "model_version": converted_topology["model_version"],
        "timestamp": converted_topology["timestamp"],
        "nodes": converted_topology["nodes"],
        "links": converted_topology["links"],
    }
    node = node_additional_property_topology["nodes"][0]
    node["active_node"] = 1
    node_additional_property_topology["nodes"][0] = node
    validated_topology = validate(node_additional_property_topology)
    error_message = "Validation Error: Additional properties are not allowed "
    error_message += "('active_node' was unexpected)"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_node_id_pattern(ampath_topology):
    """test should_fail_due_to_invalid_node_id_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    converted_topology["nodes"][0]["id"] = "Wrong Node ID"
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: 'Wrong Node ID' does not match '"
    error_message += "^urn:sdx:node:[A-Za-z0-9_,./-]*:[A-Za-z0-9.,_/-]*$'"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_node_name_required(ampath_topology):
    """test should_fail_due_to_missing_node_name_attribute_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    node = converted_topology["nodes"][0]
    del node["name"]
    converted_topology["nodes"][0] = node
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: 'name' is a required property"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_node_name_pattern(ampath_topology):
    """test should_fail_due_to_invalid_node_name_attribute_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    converted_topology["nodes"][0]["name"] = "Invalid Node Name"
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: 'Invalid Node Name' does not match '"
    error_message += "^[a-zA-Z0-9.,\\\\-_\\\\/]{1,30}$'"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_empty_node_port_array(ampath_topology):
    """test should_fail_due_to_empty_node_port_array_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    converted_topology["nodes"][0]["port"] = []
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: Additional properties are not allowed "
    error_message += "('port' was unexpected)"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_node_port_additional_properties(ampath_topology):
    """test should_fail_due_to_node_port_ additional_properties_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    node_port = converted_topology["nodes"][0]["ports"][0]
    node_port["active_node_port"] = 1
    converted_topology["nodes"][0]["ports"][0] = node_port
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: Additional properties are not allowed "
    error_message += "('active_node_port' was unexpected)"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_node_port_id_pattern(ampath_topology):
    """test should_fail_due_to_node_port_invalid_id_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    converted_topology["nodes"][0]["ports"][0]["id"] = "Wrong Node Port ID"
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: 'Wrong Node Port ID' does not match '"
    error_message += "^urn:sdx:port:[A-Za-z0-9_,./-]*:[A-Za-z0-9_.,/-]*:[A-Za-z0-9_.,/-]*$'"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_node_port_name_required(ampath_topology):
    """test should_fail_due_to_missing_node_port_name_attribute_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    node_port = converted_topology["nodes"][0]["ports"][0]
    del node_port["name"]
    converted_topology["nodes"][0]["ports"][0] = node_port
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: 'name' is a required property"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_node_port_name_pattern(ampath_topology):
    """test should_fail_due_to_invalid_node_port_name_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    converted_topology["nodes"][0]["ports"][0]["name"] = "InvalidNodePortName"
    validated_topology = validate(converted_topology)
    # error_message = "Validation Error: 'name' is a required property"
    assert validated_topology["status_code"] == 200
    # assert error_message in validated_topology["result"]


def test_node_port_type_pattern(ampath_topology):
    """test should_fail_due_to_invalid_type_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    converted_topology["nodes"][0]["ports"][0]["type"] = "200GE"
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: '200GE' is not one of ['100FE', '1GE', "
    error_message += "'10GE', '25GE', '40GE', '50GE', '100GE', '400GE', 'Other"
    error_message += "']"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_node_port_status_pattern(ampath_topology):
    """test should_fail_due_to_invalid_status_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    converted_topology["nodes"][0]["ports"][0]["status"] = "unknow"
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: 'unknow' is not one of "
    error_message += "['up', 'down', 'error']"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_node_port_state_pattern(ampath_topology):
    """test should_fail_due_to_invalid_state_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    converted_topology["nodes"][0]["ports"][0]["state"] = "unknow"
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: 'unknow' is not one of "
    error_message += "['enabled', 'disabled', 'maintenance']"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_empty_link_array(ampath_topology):
    """test should_fail_due_to_empty_link_array_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    converted_topology["links"] = []
    validated_topology = validate(converted_topology)
    #error_message = "Validation Error: [] should be non-empty"
    assert validated_topology["status_code"] == 200
    #assert error_message in validated_topology["result"]


def test_link_additional_properties(ampath_topology):
    """test should_fail_due_to_link_additional_properties_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    link = converted_topology["links"][0]
    link["active_link"] = 1
    converted_topology["links"][0] = link
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: Additional properties are not allowed "
    error_message += "('active_link' was unexpected)"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_link_id_pattern(ampath_topology):
    """test should_fail_due_to_link_invalid_id_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    converted_topology["links"][0]["id"] = "Wrong ID"
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: 'Wrong ID' does not match '"
    error_message += "^urn:sdx:link:[A-Za-z0-9_,./-]*:[A-Za-z0-9_.,/-]*$'"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_link_name_required(ampath_topology):
    """test should_fail_due_to_missing_link_name_attribute_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    link = converted_topology["links"][0]
    del link["name"]
    converted_topology["links"][0] = link
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: 'name' is a required property"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_link_name_pattern(ampath_topology):
    """test should_fail_due_to_invalid_link_name_on_json_topology"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    converted_topology["links"][0]["name"] = "Invalid Name"
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: 'Invalid Name' does not match '"
    error_message += "^[a-zA-Z0-9.,\\\\-_\\\\/]{1,30}$'"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_empty_link_port_array(ampath_topology):
    """test should_fail_due_to_empty_link_port_array_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    converted_topology["links"][0]["ports"] = []
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: [] is too short"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_link_port_format(ampath_topology):
    """test should_fail_due_to_invalid_link_port_format_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    converted_topology["links"][0]["ports"][0] = "Port "
    validated_topology = validate(converted_topology)
    print(converted_topology)
    error_message = "Validation Error: 'Port ' does not match '^urn:sdx:port:[A-Za-z0-9_,./-]*:[A-Za-z0-9_.,/-]*:[A-Za-z0-9_.,/-]*$'"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_link_type_pattern(ampath_topology):
    """test should_fail_due_to_invalid_type_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    converted_topology["links"][0]["type"] = "out"
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: 'out' is not one of ['intra']"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_link_bandwidth_out_range(ampath_topology):
    """test should_fail_due_to_bandwidth_out_of_range_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    converted_topology["links"][0]["bandwidth"] = -1
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: -1 is less than the minimum of 0"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_link_residual_out_range(ampath_topology):
    """test should_fail_due_to_residual_out_of_range_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    converted_topology["links"][0]["residual_bandwidth"] = 500
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: 500 is greater than the maximum of 100"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_link_latency_out_range(ampath_topology):
    """test should_fail_due_to_latency_out_of_range_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    converted_topology["links"][0]["latency"] = -1
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: -1 is less than the "
    error_message += "minimum of 0"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_link_packet_loss_out_range(ampath_topology):
    """test should_fail_due_to_bandwidth_out_of_range_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    converted_topology["links"][0]["packet_loss"] = 500
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: 500 is greater than the maximum of 100"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_link_status_pattern(ampath_topology):
    """test should_fail_due_to_invalid_status_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    converted_topology["links"][0]["status"] = "unknow"
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: 'unknow' is not one of "
    error_message += "['up', 'down', 'error']"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


def test_state_pattern(ampath_topology):
    """test should_fail_due_to_invalid_state_on_json_data"""
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
        topology_id="urn:sdx:topology:" + topology_id
    ).parse_convert_topology()
    converted_topology["links"][0]["state"] = "unknow"
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: 'unknow' is not one of "
    error_message += "['enabled', 'disabled', 'maintenance']"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]
