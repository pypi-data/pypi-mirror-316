# coding: utf-8

"""
    Zarban API

    API for Zarban services.  # noqa: E501

    The version of the OpenAPI document: 2.0.0
    Contact: info@zarban.io
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from zarban.service.openapi_client.configuration import Configuration


class UserError(object):
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
        'messages': 'dict(str, ErrorMessage)',
        'reasons': 'list[str]'
    }

    attribute_map = {
        'messages': 'messages',
        'reasons': 'reasons'
    }

    def __init__(self, messages=None, reasons=None, local_vars_configuration=None):  # noqa: E501
        """UserError - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._messages = None
        self._reasons = None
        self.discriminator = None

        self.messages = messages
        self.reasons = reasons

    @property
    def messages(self):
        """Gets the messages of this UserError.  # noqa: E501

        Localized error messages  # noqa: E501

        :return: The messages of this UserError.  # noqa: E501
        :rtype: dict(str, ErrorMessage)
        """
        return self._messages

    @messages.setter
    def messages(self, messages):
        """Sets the messages of this UserError.

        Localized error messages  # noqa: E501

        :param messages: The messages of this UserError.  # noqa: E501
        :type: dict(str, ErrorMessage)
        """
        if self.local_vars_configuration.client_side_validation and messages is None:  # noqa: E501
            raise ValueError("Invalid value for `messages`, must not be `None`")  # noqa: E501

        self._messages = messages

    @property
    def reasons(self):
        """Gets the reasons of this UserError.  # noqa: E501


        :return: The reasons of this UserError.  # noqa: E501
        :rtype: list[str]
        """
        return self._reasons

    @reasons.setter
    def reasons(self, reasons):
        """Sets the reasons of this UserError.


        :param reasons: The reasons of this UserError.  # noqa: E501
        :type: list[str]
        """
        if self.local_vars_configuration.client_side_validation and reasons is None:  # noqa: E501
            raise ValueError("Invalid value for `reasons`, must not be `None`")  # noqa: E501

        self._reasons = reasons

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
        if not isinstance(other, UserError):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UserError):
            return True

        return self.to_dict() != other.to_dict()
