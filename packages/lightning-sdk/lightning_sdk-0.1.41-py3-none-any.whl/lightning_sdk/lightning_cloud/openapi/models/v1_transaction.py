# coding: utf-8

"""
    external/v1/auth_service.proto

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: version not set
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git

    NOTE
    ----
    standard swagger-codegen-cli for this python client has been modified
    by custom templates. The purpose of these templates is to include
    typing information in the API and Model code. Please refer to the
    main grid repository for more info
"""

import pprint
import re  # noqa: F401

from typing import TYPE_CHECKING

import six

if TYPE_CHECKING:
    from datetime import datetime
    from lightning_sdk.lightning_cloud.openapi.models import *

class V1Transaction(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'amount': 'float',
        'created_at': 'datetime',
        'display_name': 'str',
        'type': 'str'
    }

    attribute_map = {
        'amount': 'amount',
        'created_at': 'createdAt',
        'display_name': 'displayName',
        'type': 'type'
    }

    def __init__(self, amount: 'float' =None, created_at: 'datetime' =None, display_name: 'str' =None, type: 'str' =None):  # noqa: E501
        """V1Transaction - a model defined in Swagger"""  # noqa: E501
        self._amount = None
        self._created_at = None
        self._display_name = None
        self._type = None
        self.discriminator = None
        if amount is not None:
            self.amount = amount
        if created_at is not None:
            self.created_at = created_at
        if display_name is not None:
            self.display_name = display_name
        if type is not None:
            self.type = type

    @property
    def amount(self) -> 'float':
        """Gets the amount of this V1Transaction.  # noqa: E501


        :return: The amount of this V1Transaction.  # noqa: E501
        :rtype: float
        """
        return self._amount

    @amount.setter
    def amount(self, amount: 'float'):
        """Sets the amount of this V1Transaction.


        :param amount: The amount of this V1Transaction.  # noqa: E501
        :type: float
        """

        self._amount = amount

    @property
    def created_at(self) -> 'datetime':
        """Gets the created_at of this V1Transaction.  # noqa: E501


        :return: The created_at of this V1Transaction.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at: 'datetime'):
        """Sets the created_at of this V1Transaction.


        :param created_at: The created_at of this V1Transaction.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def display_name(self) -> 'str':
        """Gets the display_name of this V1Transaction.  # noqa: E501


        :return: The display_name of this V1Transaction.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name: 'str'):
        """Sets the display_name of this V1Transaction.


        :param display_name: The display_name of this V1Transaction.  # noqa: E501
        :type: str
        """

        self._display_name = display_name

    @property
    def type(self) -> 'str':
        """Gets the type of this V1Transaction.  # noqa: E501


        :return: The type of this V1Transaction.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: 'str'):
        """Sets the type of this V1Transaction.


        :param type: The type of this V1Transaction.  # noqa: E501
        :type: str
        """

        self._type = type

    def to_dict(self) -> dict:
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(V1Transaction, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1Transaction') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1Transaction):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1Transaction') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
