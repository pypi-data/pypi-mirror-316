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


class Vault(object):
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
        'owner': 'str',
        'urn': 'str',
        'liquidation_price': 'dict(str, str)',
        'collateral_locked': 'dict(str, str)',
        'collateralization_ratio': 'str',
        'loan_to_value': 'str',
        'debt': 'dict(str, str)',
        'available_to_withdraw': 'dict(str, str)',
        'available_to_mint': 'dict(str, str)',
        'ilk': 'Ilk'
    }

    attribute_map = {
        'id': 'id',
        'owner': 'owner',
        'urn': 'urn',
        'liquidation_price': 'liquidationPrice',
        'collateral_locked': 'collateralLocked',
        'collateralization_ratio': 'collateralizationRatio',
        'loan_to_value': 'loanToValue',
        'debt': 'debt',
        'available_to_withdraw': 'availableToWithdraw',
        'available_to_mint': 'availableToMint',
        'ilk': 'ilk'
    }

    def __init__(self, id=None, owner=None, urn=None, liquidation_price=None, collateral_locked=None, collateralization_ratio=None, loan_to_value=None, debt=None, available_to_withdraw=None, available_to_mint=None, ilk=None, local_vars_configuration=None):  # noqa: E501
        """Vault - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._owner = None
        self._urn = None
        self._liquidation_price = None
        self._collateral_locked = None
        self._collateralization_ratio = None
        self._loan_to_value = None
        self._debt = None
        self._available_to_withdraw = None
        self._available_to_mint = None
        self._ilk = None
        self.discriminator = None

        self.id = id
        self.owner = owner
        self.urn = urn
        self.liquidation_price = liquidation_price
        self.collateral_locked = collateral_locked
        self.collateralization_ratio = collateralization_ratio
        self.loan_to_value = loan_to_value
        self.debt = debt
        self.available_to_withdraw = available_to_withdraw
        self.available_to_mint = available_to_mint
        self.ilk = ilk

    @property
    def id(self):
        """Gets the id of this Vault.  # noqa: E501

        Identifier for the vault.  # noqa: E501

        :return: The id of this Vault.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Vault.

        Identifier for the vault.  # noqa: E501

        :param id: The id of this Vault.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def owner(self):
        """Gets the owner of this Vault.  # noqa: E501

        Ethereum address of the vault owner.  # noqa: E501

        :return: The owner of this Vault.  # noqa: E501
        :rtype: str
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Sets the owner of this Vault.

        Ethereum address of the vault owner.  # noqa: E501

        :param owner: The owner of this Vault.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and owner is None:  # noqa: E501
            raise ValueError("Invalid value for `owner`, must not be `None`")  # noqa: E501

        self._owner = owner

    @property
    def urn(self):
        """Gets the urn of this Vault.  # noqa: E501

        Ethereum address of the vault urn.  # noqa: E501

        :return: The urn of this Vault.  # noqa: E501
        :rtype: str
        """
        return self._urn

    @urn.setter
    def urn(self, urn):
        """Sets the urn of this Vault.

        Ethereum address of the vault urn.  # noqa: E501

        :param urn: The urn of this Vault.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and urn is None:  # noqa: E501
            raise ValueError("Invalid value for `urn`, must not be `None`")  # noqa: E501

        self._urn = urn

    @property
    def liquidation_price(self):
        """Gets the liquidation_price of this Vault.  # noqa: E501


        :return: The liquidation_price of this Vault.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._liquidation_price

    @liquidation_price.setter
    def liquidation_price(self, liquidation_price):
        """Sets the liquidation_price of this Vault.


        :param liquidation_price: The liquidation_price of this Vault.  # noqa: E501
        :type: dict(str, str)
        """
        if self.local_vars_configuration.client_side_validation and liquidation_price is None:  # noqa: E501
            raise ValueError("Invalid value for `liquidation_price`, must not be `None`")  # noqa: E501

        self._liquidation_price = liquidation_price

    @property
    def collateral_locked(self):
        """Gets the collateral_locked of this Vault.  # noqa: E501


        :return: The collateral_locked of this Vault.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._collateral_locked

    @collateral_locked.setter
    def collateral_locked(self, collateral_locked):
        """Sets the collateral_locked of this Vault.


        :param collateral_locked: The collateral_locked of this Vault.  # noqa: E501
        :type: dict(str, str)
        """
        if self.local_vars_configuration.client_side_validation and collateral_locked is None:  # noqa: E501
            raise ValueError("Invalid value for `collateral_locked`, must not be `None`")  # noqa: E501

        self._collateral_locked = collateral_locked

    @property
    def collateralization_ratio(self):
        """Gets the collateralization_ratio of this Vault.  # noqa: E501

        The collateralization ratio of the vault.  # noqa: E501

        :return: The collateralization_ratio of this Vault.  # noqa: E501
        :rtype: str
        """
        return self._collateralization_ratio

    @collateralization_ratio.setter
    def collateralization_ratio(self, collateralization_ratio):
        """Sets the collateralization_ratio of this Vault.

        The collateralization ratio of the vault.  # noqa: E501

        :param collateralization_ratio: The collateralization_ratio of this Vault.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and collateralization_ratio is None:  # noqa: E501
            raise ValueError("Invalid value for `collateralization_ratio`, must not be `None`")  # noqa: E501

        self._collateralization_ratio = collateralization_ratio

    @property
    def loan_to_value(self):
        """Gets the loan_to_value of this Vault.  # noqa: E501

        The loan to value of the vault.  # noqa: E501

        :return: The loan_to_value of this Vault.  # noqa: E501
        :rtype: str
        """
        return self._loan_to_value

    @loan_to_value.setter
    def loan_to_value(self, loan_to_value):
        """Sets the loan_to_value of this Vault.

        The loan to value of the vault.  # noqa: E501

        :param loan_to_value: The loan_to_value of this Vault.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and loan_to_value is None:  # noqa: E501
            raise ValueError("Invalid value for `loan_to_value`, must not be `None`")  # noqa: E501

        self._loan_to_value = loan_to_value

    @property
    def debt(self):
        """Gets the debt of this Vault.  # noqa: E501


        :return: The debt of this Vault.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._debt

    @debt.setter
    def debt(self, debt):
        """Sets the debt of this Vault.


        :param debt: The debt of this Vault.  # noqa: E501
        :type: dict(str, str)
        """
        if self.local_vars_configuration.client_side_validation and debt is None:  # noqa: E501
            raise ValueError("Invalid value for `debt`, must not be `None`")  # noqa: E501

        self._debt = debt

    @property
    def available_to_withdraw(self):
        """Gets the available_to_withdraw of this Vault.  # noqa: E501


        :return: The available_to_withdraw of this Vault.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._available_to_withdraw

    @available_to_withdraw.setter
    def available_to_withdraw(self, available_to_withdraw):
        """Sets the available_to_withdraw of this Vault.


        :param available_to_withdraw: The available_to_withdraw of this Vault.  # noqa: E501
        :type: dict(str, str)
        """
        if self.local_vars_configuration.client_side_validation and available_to_withdraw is None:  # noqa: E501
            raise ValueError("Invalid value for `available_to_withdraw`, must not be `None`")  # noqa: E501

        self._available_to_withdraw = available_to_withdraw

    @property
    def available_to_mint(self):
        """Gets the available_to_mint of this Vault.  # noqa: E501


        :return: The available_to_mint of this Vault.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._available_to_mint

    @available_to_mint.setter
    def available_to_mint(self, available_to_mint):
        """Sets the available_to_mint of this Vault.


        :param available_to_mint: The available_to_mint of this Vault.  # noqa: E501
        :type: dict(str, str)
        """
        if self.local_vars_configuration.client_side_validation and available_to_mint is None:  # noqa: E501
            raise ValueError("Invalid value for `available_to_mint`, must not be `None`")  # noqa: E501

        self._available_to_mint = available_to_mint

    @property
    def ilk(self):
        """Gets the ilk of this Vault.  # noqa: E501


        :return: The ilk of this Vault.  # noqa: E501
        :rtype: Ilk
        """
        return self._ilk

    @ilk.setter
    def ilk(self, ilk):
        """Sets the ilk of this Vault.


        :param ilk: The ilk of this Vault.  # noqa: E501
        :type: Ilk
        """
        if self.local_vars_configuration.client_side_validation and ilk is None:  # noqa: E501
            raise ValueError("Invalid value for `ilk`, must not be `None`")  # noqa: E501

        self._ilk = ilk

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
        if not isinstance(other, Vault):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Vault):
            return True

        return self.to_dict() != other.to_dict()
