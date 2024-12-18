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


class Referral(object):
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
        'id': 'int',
        'referrer_id': 'int',
        'name': 'str',
        'usage_limit': 'int',
        'usage_count': 'int',
        'created_at': 'Timestamp',
        'link': 'str',
        'share_url': 'str'
    }

    attribute_map = {
        'id': 'id',
        'referrer_id': 'referrerId',
        'name': 'name',
        'usage_limit': 'usageLimit',
        'usage_count': 'usageCount',
        'created_at': 'createdAt',
        'link': 'link',
        'share_url': 'shareUrl'
    }

    def __init__(self, id=None, referrer_id=None, name=None, usage_limit=None, usage_count=None, created_at=None, link=None, share_url=None, local_vars_configuration=None):  # noqa: E501
        """Referral - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._referrer_id = None
        self._name = None
        self._usage_limit = None
        self._usage_count = None
        self._created_at = None
        self._link = None
        self._share_url = None
        self.discriminator = None

        self.id = id
        self.referrer_id = referrer_id
        self.name = name
        self.usage_limit = usage_limit
        self.usage_count = usage_count
        self.created_at = created_at
        self.link = link
        if share_url is not None:
            self.share_url = share_url

    @property
    def id(self):
        """Gets the id of this Referral.  # noqa: E501


        :return: The id of this Referral.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Referral.


        :param id: The id of this Referral.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def referrer_id(self):
        """Gets the referrer_id of this Referral.  # noqa: E501


        :return: The referrer_id of this Referral.  # noqa: E501
        :rtype: int
        """
        return self._referrer_id

    @referrer_id.setter
    def referrer_id(self, referrer_id):
        """Sets the referrer_id of this Referral.


        :param referrer_id: The referrer_id of this Referral.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and referrer_id is None:  # noqa: E501
            raise ValueError("Invalid value for `referrer_id`, must not be `None`")  # noqa: E501

        self._referrer_id = referrer_id

    @property
    def name(self):
        """Gets the name of this Referral.  # noqa: E501


        :return: The name of this Referral.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Referral.


        :param name: The name of this Referral.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def usage_limit(self):
        """Gets the usage_limit of this Referral.  # noqa: E501


        :return: The usage_limit of this Referral.  # noqa: E501
        :rtype: int
        """
        return self._usage_limit

    @usage_limit.setter
    def usage_limit(self, usage_limit):
        """Sets the usage_limit of this Referral.


        :param usage_limit: The usage_limit of this Referral.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and usage_limit is None:  # noqa: E501
            raise ValueError("Invalid value for `usage_limit`, must not be `None`")  # noqa: E501

        self._usage_limit = usage_limit

    @property
    def usage_count(self):
        """Gets the usage_count of this Referral.  # noqa: E501


        :return: The usage_count of this Referral.  # noqa: E501
        :rtype: int
        """
        return self._usage_count

    @usage_count.setter
    def usage_count(self, usage_count):
        """Sets the usage_count of this Referral.


        :param usage_count: The usage_count of this Referral.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and usage_count is None:  # noqa: E501
            raise ValueError("Invalid value for `usage_count`, must not be `None`")  # noqa: E501

        self._usage_count = usage_count

    @property
    def created_at(self):
        """Gets the created_at of this Referral.  # noqa: E501


        :return: The created_at of this Referral.  # noqa: E501
        :rtype: Timestamp
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Referral.


        :param created_at: The created_at of this Referral.  # noqa: E501
        :type: Timestamp
        """
        if self.local_vars_configuration.client_side_validation and created_at is None:  # noqa: E501
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def link(self):
        """Gets the link of this Referral.  # noqa: E501


        :return: The link of this Referral.  # noqa: E501
        :rtype: str
        """
        return self._link

    @link.setter
    def link(self, link):
        """Sets the link of this Referral.


        :param link: The link of this Referral.  # noqa: E501
        :type: str
        """

        self._link = link

    @property
    def share_url(self):
        """Gets the share_url of this Referral.  # noqa: E501


        :return: The share_url of this Referral.  # noqa: E501
        :rtype: str
        """
        return self._share_url

    @share_url.setter
    def share_url(self, share_url):
        """Sets the share_url of this Referral.


        :param share_url: The share_url of this Referral.  # noqa: E501
        :type: str
        """

        self._share_url = share_url

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
        if not isinstance(other, Referral):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Referral):
            return True

        return self.to_dict() != other.to_dict()
