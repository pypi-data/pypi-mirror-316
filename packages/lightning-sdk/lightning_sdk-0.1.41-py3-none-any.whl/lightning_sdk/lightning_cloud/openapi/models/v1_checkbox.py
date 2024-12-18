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

class V1Checkbox(object):
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
        'false_value': 'str',
        'is_checked': 'bool',
        'true_value': 'str',
        'value': 'bool'
    }

    attribute_map = {
        'false_value': 'falseValue',
        'is_checked': 'isChecked',
        'true_value': 'trueValue',
        'value': 'value'
    }

    def __init__(self, false_value: 'str' =None, is_checked: 'bool' =None, true_value: 'str' =None, value: 'bool' =None):  # noqa: E501
        """V1Checkbox - a model defined in Swagger"""  # noqa: E501
        self._false_value = None
        self._is_checked = None
        self._true_value = None
        self._value = None
        self.discriminator = None
        if false_value is not None:
            self.false_value = false_value
        if is_checked is not None:
            self.is_checked = is_checked
        if true_value is not None:
            self.true_value = true_value
        if value is not None:
            self.value = value

    @property
    def false_value(self) -> 'str':
        """Gets the false_value of this V1Checkbox.  # noqa: E501


        :return: The false_value of this V1Checkbox.  # noqa: E501
        :rtype: str
        """
        return self._false_value

    @false_value.setter
    def false_value(self, false_value: 'str'):
        """Sets the false_value of this V1Checkbox.


        :param false_value: The false_value of this V1Checkbox.  # noqa: E501
        :type: str
        """

        self._false_value = false_value

    @property
    def is_checked(self) -> 'bool':
        """Gets the is_checked of this V1Checkbox.  # noqa: E501


        :return: The is_checked of this V1Checkbox.  # noqa: E501
        :rtype: bool
        """
        return self._is_checked

    @is_checked.setter
    def is_checked(self, is_checked: 'bool'):
        """Sets the is_checked of this V1Checkbox.


        :param is_checked: The is_checked of this V1Checkbox.  # noqa: E501
        :type: bool
        """

        self._is_checked = is_checked

    @property
    def true_value(self) -> 'str':
        """Gets the true_value of this V1Checkbox.  # noqa: E501


        :return: The true_value of this V1Checkbox.  # noqa: E501
        :rtype: str
        """
        return self._true_value

    @true_value.setter
    def true_value(self, true_value: 'str'):
        """Sets the true_value of this V1Checkbox.


        :param true_value: The true_value of this V1Checkbox.  # noqa: E501
        :type: str
        """

        self._true_value = true_value

    @property
    def value(self) -> 'bool':
        """Gets the value of this V1Checkbox.  # noqa: E501


        :return: The value of this V1Checkbox.  # noqa: E501
        :rtype: bool
        """
        return self._value

    @value.setter
    def value(self, value: 'bool'):
        """Sets the value of this V1Checkbox.


        :param value: The value of this V1Checkbox.  # noqa: E501
        :type: bool
        """

        self._value = value

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
        if issubclass(V1Checkbox, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1Checkbox') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1Checkbox):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1Checkbox') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
