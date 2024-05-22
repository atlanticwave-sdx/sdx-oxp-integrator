""" location model """
# coding: utf-8

from __future__ import absolute_import

from utils import util
from models.base_model_ import Model


class Location(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, address=None, latitude=None, longitude=None):  # noqa: E501
        """Location - a model defined in OpenAPI

        :param address: The address of this Location.  # noqa: E501
        :type address: str
        :param latitude: The latitude of this Location.  # noqa: E501
        :type latitude: float
        :param longitude: The longitude of this Location.  # noqa: E501
        :type longitude: float
        """
        self.openapi_types = {"address": str, "latitude": float, "longitude": float}

        self.attribute_map = {
            "address": "address",
            "latitude": "latitude",
            "longitude": "longitude",
        }

        self._address = address
        self._latitude = latitude
        self._longitude = longitude

    @classmethod
    def from_dict(cls, dikt) -> "Location":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The location of this Location.  # noqa: E501
        :rtype: Location
        """
        return util.deserialize_model(dikt, cls)

    @property
    def address(self):
        """Gets the address of this Location.


        :return: The address of this Location.
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this Location.


        :param address: The address of this Location.
        :type address: str
        """
        if address is None:
            raise ValueError(
                "Invalid value for `address`, must not be `None`"
            )  # noqa: E501

        self._address = address

    @property
    def latitude(self):
        """Gets the latitude of this Location.


        :return: The latitude of this Location.
        :rtype: float
        """
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        """Sets the latitude of this Location.


        :param latitude: The latitude of this Location.
        :type latitude: float
        """
        if latitude is None:
            raise ValueError(
                "Invalid value for `latitude`, must not be `None`"
            )  # noqa: E501
        if latitude is not None and latitude > 90.0:  # noqa: E501
            raise ValueError(
                "Invalid value for `latitude`, must be a value less than or equal to `90.0`"
            )  # noqa: E501
        if latitude is not None and latitude < -90.0:  # noqa: E501
            raise ValueError(
                "Invalid value for `latitude`, must be a value greater than or equal to `-90.0`"
            )  # noqa: E501

        self._latitude = latitude

    @property
    def longitude(self):
        """Gets the longitude of this Location.


        :return: The longitude of this Location.
        :rtype: float
        """
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        """Sets the longitude of this Location.


        :param longitude: The longitude of this Location.
        :type longitude: float
        """
        if longitude is None:
            raise ValueError(
                "Invalid value for `longitude`, must not be `None`"
            )  # noqa: E501
        if longitude is not None and longitude > 90.0:  # noqa: E501
            raise ValueError(
                "Invalid value for `longitude`, must be a value less than or equal to `90.0`"
            )  # noqa: E501
        if longitude is not None and longitude < -90.0:  # noqa: E501
            raise ValueError(
                "Invalid value for `longitude`, must be a value greater than or equal to `-90.0`"
            )  # noqa: E501

        self._longitude = longitude