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


class RepayLoanRequest(object):
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
        'intent': 'str',
        'loan_id': 'str'
    }

    attribute_map = {
        'intent': 'intent',
        'loan_id': 'loanId'
    }

    def __init__(self, intent=None, loan_id=None, local_vars_configuration=None):  # noqa: E501
        """RepayLoanRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._intent = None
        self._loan_id = None
        self.discriminator = None

        self.intent = intent
        self.loan_id = loan_id

    @property
    def intent(self):
        """Gets the intent of this RepayLoanRequest.  # noqa: E501

        Intent to repay a loan  # noqa: E501

        :return: The intent of this RepayLoanRequest.  # noqa: E501
        :rtype: str
        """
        return self._intent

    @intent.setter
    def intent(self, intent):
        """Sets the intent of this RepayLoanRequest.

        Intent to repay a loan  # noqa: E501

        :param intent: The intent of this RepayLoanRequest.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and intent is None:  # noqa: E501
            raise ValueError("Invalid value for `intent`, must not be `None`")  # noqa: E501
        allowed_values = ["Repay", "Preview"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and intent not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `intent` ({0}), must be one of {1}"  # noqa: E501
                .format(intent, allowed_values)
            )

        self._intent = intent

    @property
    def loan_id(self):
        """Gets the loan_id of this RepayLoanRequest.  # noqa: E501

        The id of a loan  # noqa: E501

        :return: The loan_id of this RepayLoanRequest.  # noqa: E501
        :rtype: str
        """
        return self._loan_id

    @loan_id.setter
    def loan_id(self, loan_id):
        """Sets the loan_id of this RepayLoanRequest.

        The id of a loan  # noqa: E501

        :param loan_id: The loan_id of this RepayLoanRequest.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and loan_id is None:  # noqa: E501
            raise ValueError("Invalid value for `loan_id`, must not be `None`")  # noqa: E501

        self._loan_id = loan_id

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
        if not isinstance(other, RepayLoanRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RepayLoanRequest):
            return True

        return self.to_dict() != other.to_dict()
