""" conftest """
import json
import os

import pytest


@pytest.fixture
def ampath_topology():
    """Build ampath topology json_data"""
    actual_dir = os.getcwd()
    ampath_data = actual_dir + "/tests/ampath.json"
    with open(ampath_data, encoding="utf8") as json_file:
        data = json.load(json_file)
        json_file.close()
    return data


@pytest.fixture
def oxp_topology():
    """Build oxp topology json_data"""
    actual_dir = os.getcwd()
    ampath_data = actual_dir + "/tests/oxp_topology.json"
    with open(ampath_data, encoding="utf8") as json_file:
        data = json.load(json_file)
        json_file.close()
    return data
