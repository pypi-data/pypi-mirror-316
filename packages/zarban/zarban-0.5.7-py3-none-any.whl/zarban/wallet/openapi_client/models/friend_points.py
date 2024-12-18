# coding: utf-8

"""
    Zarban Wallet API

    API for Zarban wallet services.  # noqa: E501

    The version of the OpenAPI document: 2.0.0
    Contact: info@zarban.io
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from zarban.wallet.openapi_client.configuration import Configuration


class FriendPoints(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'first_name': 'str',
        'points': 'int'
    }

    attribute_map = {
        'first_name': 'firstName',
        'points': 'points'
    }

    def __init__(self, first_name=None, points=None, local_vars_configuration=None):  # noqa: E501
        """FriendPoints - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._first_name = None
        self._points = None
        self.discriminator = None

        self.first_name = first_name
        self.points = points

    @property
    def first_name(self):
        """Gets the first_name of this FriendPoints.  # noqa: E501

        the first name of the friend  # noqa: E501

        :return: The first_name of this FriendPoints.  # noqa: E501
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """Sets the first_name of this FriendPoints.

        the first name of the friend  # noqa: E501

        :param first_name: The first_name of this FriendPoints.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and first_name is None:  # noqa: E501
            raise ValueError("Invalid value for `first_name`, must not be `None`")  # noqa: E501

        self._first_name = first_name

    @property
    def points(self):
        """Gets the points of this FriendPoints.  # noqa: E501

        the points of the friend  # noqa: E501

        :return: The points of this FriendPoints.  # noqa: E501
        :rtype: int
        """
        return self._points

    @points.setter
    def points(self, points):
        """Sets the points of this FriendPoints.

        the points of the friend  # noqa: E501

        :param points: The points of this FriendPoints.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and points is None:  # noqa: E501
            raise ValueError("Invalid value for `points`, must not be `None`")  # noqa: E501

        self._points = points

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, FriendPoints):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, FriendPoints):
            return True

        return self.to_dict() != other.to_dict()
