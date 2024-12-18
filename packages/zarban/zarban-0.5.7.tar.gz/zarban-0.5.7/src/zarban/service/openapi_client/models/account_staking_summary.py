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


class AccountStakingSummary(object):
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
        'total_stake': 'dict(str, str)',
        'unclaimed_reward': 'dict(str, str)',
        'net_apy': 'str'
    }

    attribute_map = {
        'total_stake': 'totalStake',
        'unclaimed_reward': 'unclaimedReward',
        'net_apy': 'netApy'
    }

    def __init__(self, total_stake=None, unclaimed_reward=None, net_apy=None, local_vars_configuration=None):  # noqa: E501
        """AccountStakingSummary - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._total_stake = None
        self._unclaimed_reward = None
        self._net_apy = None
        self.discriminator = None

        self.total_stake = total_stake
        self.unclaimed_reward = unclaimed_reward
        self.net_apy = net_apy

    @property
    def total_stake(self):
        """Gets the total_stake of this AccountStakingSummary.  # noqa: E501


        :return: The total_stake of this AccountStakingSummary.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._total_stake

    @total_stake.setter
    def total_stake(self, total_stake):
        """Sets the total_stake of this AccountStakingSummary.


        :param total_stake: The total_stake of this AccountStakingSummary.  # noqa: E501
        :type: dict(str, str)
        """
        if self.local_vars_configuration.client_side_validation and total_stake is None:  # noqa: E501
            raise ValueError("Invalid value for `total_stake`, must not be `None`")  # noqa: E501

        self._total_stake = total_stake

    @property
    def unclaimed_reward(self):
        """Gets the unclaimed_reward of this AccountStakingSummary.  # noqa: E501


        :return: The unclaimed_reward of this AccountStakingSummary.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._unclaimed_reward

    @unclaimed_reward.setter
    def unclaimed_reward(self, unclaimed_reward):
        """Sets the unclaimed_reward of this AccountStakingSummary.


        :param unclaimed_reward: The unclaimed_reward of this AccountStakingSummary.  # noqa: E501
        :type: dict(str, str)
        """
        if self.local_vars_configuration.client_side_validation and unclaimed_reward is None:  # noqa: E501
            raise ValueError("Invalid value for `unclaimed_reward`, must not be `None`")  # noqa: E501

        self._unclaimed_reward = unclaimed_reward

    @property
    def net_apy(self):
        """Gets the net_apy of this AccountStakingSummary.  # noqa: E501

        Net annual percentage yield in staking contract  # noqa: E501

        :return: The net_apy of this AccountStakingSummary.  # noqa: E501
        :rtype: str
        """
        return self._net_apy

    @net_apy.setter
    def net_apy(self, net_apy):
        """Sets the net_apy of this AccountStakingSummary.

        Net annual percentage yield in staking contract  # noqa: E501

        :param net_apy: The net_apy of this AccountStakingSummary.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and net_apy is None:  # noqa: E501
            raise ValueError("Invalid value for `net_apy`, must not be `None`")  # noqa: E501

        self._net_apy = net_apy

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
        if not isinstance(other, AccountStakingSummary):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AccountStakingSummary):
            return True

        return self.to_dict() != other.to_dict()
