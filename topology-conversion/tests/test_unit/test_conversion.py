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
    ).parse_convert_topology()
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: 'This is a wrong name' does not match '"
    error_message += "^[A-Za-z0-9_.-]*$'"
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
    ).parse_convert_topology()
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: 'urn:sdx:topology:This is a wrong ID' "
    error_message += "does not match '^((urn:sdx:topology:)[A-Za-z0-9_.:-]*$)'"
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
    error_message = "Validation Error: Additional properties are not allowed "
    error_message += "('active' was unexpected)"
    assert validated_topology["status_code"] == 400
    assert error_message in validated_topology["result"]


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
    ).parse_convert_topology()
    validated_topology = validate(converted_topology)
    error_message = "Validation Error: 'This is a wrong timestamp'"
    error_message += " does not match ' ^[A-Za-z0-9_.-]*$'"
    assert validated_topology["status_code"] == 200
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
    ).parse_convert_topology()
    empty_node_topology = {
        "id": converted_topology["id"],
        "name": converted_topology["name"],
        "version": converted_topology["version"],
        "model_version": converted_topology["model_version"],
        "timestamp": converted_topology["timestamp"],
        "nodes": [],
        "links": converted_topology["links"],
    }
    validated_topology = validate(empty_node_topology)
    error_message = "Validation Error: [] should be non-empty"
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
