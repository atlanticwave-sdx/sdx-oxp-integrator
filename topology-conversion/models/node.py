# coding: utf-8

from __future__ import absolute_import

import re  # noqa: E501
from typing import List  # noqa: F401

from utils import util

from models.base_model_ import Model
from models.location import Location  # noqa: E501
from models.port import Port  # noqa: E501


class Node(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(
        self, node_id=None, name=None, location=None, ports=None
    ):  # noqa: E501
        """Node - a model defined in OpenAPI

        :param node_id: The node_id of this Node.  # noqa: E501
        :type node_id: str
        :param name: The name of this Node.  # noqa: E501
        :type name: str
        :param location: The location of this Node.  # noqa: E501
        :type location: Location
        :param ports: The ports of this Node.  # noqa: E501
        :type ports: List[Port]
        """
        self.openapi_types = {
            "node_id": str,
            "name": str,
            "location": Location,
            "ports": List[Port],
        }

        self.attribute_map = {
            "node_id": "node_id",
            "name": "name",
            "location": "location",
            "ports": "ports",
        }

        self._node_id = node_id
        self._name = name
        self._location = location
        self._ports = ports

    @classmethod
    def from_dict(cls, dikt) -> "Node":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The node of this Node.  # noqa: E501
        :rtype: Node
        """
        return util.deserialize_model(dikt, cls)

    @property
    def node_id(self):
        """Gets the node_id of this Node.


        :return: The node_id of this Node.
        :rtype: str
        """
        return self._node_id

    @node_id.setter
    def node_id(self, node_id):
        """Sets the node_id of this Node.


        :param node_id: The node_id of this Node.
        :type node_id: str
        """
        if node_id is None:
            raise ValueError(
                "Invalid value for `node_id`, must not be `None`"
            )  # noqa: E501
        if node_id is not None and not re.search(
            r"^((urn:sdx:node:)[A-Za-z_.-]*$)", node_id
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `node_id`, must be a follow pattern or equal to `/^((urn:sdx:node:)[A-Za-z_.-]*$)/`"
            )  # noqa: E501

        self._node_id = node_id

    @property
    def name(self):
        """Gets the name of this Node.


        :return: The name of this Node.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Node.


        :param name: The name of this Node.
        :type name: str
        """
        if name is None:
            raise ValueError(
                "Invalid value for `name`, must not be `None`"
            )  # noqa: E501
        if name is not None and len(name) > 30:
            raise ValueError(
                "Invalid value for `name`, length must be less than or equal to `30`"
            )  # noqa: E501
        if name is not None and len(name) < 3:
            raise ValueError(
                "Invalid value for `name`, length must be greater than or equal to `3`"
            )  # noqa: E501
        if name is not None and not re.search(r"^[A-Za-z_.-]*$", name):  # noqa: E501
            raise ValueError(
                "Invalid value for `name`, must be a follow pattern or equal to `/^[A-Za-z_.-]*$/`"
            )  # noqa: E501

        self._name = name

    @property
    def location(self):
        """Gets the location of this Node.


        :return: The location of this Node.
        :rtype: Location
        """
        return self._location

    @location.setter
    def location(self, location):
        """Sets the location of this Node.


        :param location: The location of this Node.
        :type location: Location
        """
        if location is None:
            raise ValueError(
                "Invalid value for `location`, must not be `None`"
            )  # noqa: E501

        self._location = location

    @property
    def ports(self):
        """Gets the ports of this Node.


        :return: The ports of this Node.
        :rtype: List[Port]
        """
        return self._ports

    @ports.setter
    def ports(self, ports):
        """Sets the ports of this Node.


        :param ports: The ports of this Node.
        :type ports: List[Port]
        """
        if ports is None:
            raise ValueError(
                "Invalid value for `ports`, must not be `None`"
            )  # noqa: E501

        self._ports = ports