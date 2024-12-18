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

class V1InstanceOverprovisioningSpec(object):
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
        'count': 'int',
        'instance_type': 'str',
        'is_spot': 'bool',
        'resource_type': 'str',
        'volume_size': 'int'
    }

    attribute_map = {
        'count': 'count',
        'instance_type': 'instanceType',
        'is_spot': 'isSpot',
        'resource_type': 'resourceType',
        'volume_size': 'volumeSize'
    }

    def __init__(self, count: 'int' =None, instance_type: 'str' =None, is_spot: 'bool' =None, resource_type: 'str' =None, volume_size: 'int' =None):  # noqa: E501
        """V1InstanceOverprovisioningSpec - a model defined in Swagger"""  # noqa: E501
        self._count = None
        self._instance_type = None
        self._is_spot = None
        self._resource_type = None
        self._volume_size = None
        self.discriminator = None
        if count is not None:
            self.count = count
        if instance_type is not None:
            self.instance_type = instance_type
        if is_spot is not None:
            self.is_spot = is_spot
        if resource_type is not None:
            self.resource_type = resource_type
        if volume_size is not None:
            self.volume_size = volume_size

    @property
    def count(self) -> 'int':
        """Gets the count of this V1InstanceOverprovisioningSpec.  # noqa: E501


        :return: The count of this V1InstanceOverprovisioningSpec.  # noqa: E501
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count: 'int'):
        """Sets the count of this V1InstanceOverprovisioningSpec.


        :param count: The count of this V1InstanceOverprovisioningSpec.  # noqa: E501
        :type: int
        """

        self._count = count

    @property
    def instance_type(self) -> 'str':
        """Gets the instance_type of this V1InstanceOverprovisioningSpec.  # noqa: E501


        :return: The instance_type of this V1InstanceOverprovisioningSpec.  # noqa: E501
        :rtype: str
        """
        return self._instance_type

    @instance_type.setter
    def instance_type(self, instance_type: 'str'):
        """Sets the instance_type of this V1InstanceOverprovisioningSpec.


        :param instance_type: The instance_type of this V1InstanceOverprovisioningSpec.  # noqa: E501
        :type: str
        """

        self._instance_type = instance_type

    @property
    def is_spot(self) -> 'bool':
        """Gets the is_spot of this V1InstanceOverprovisioningSpec.  # noqa: E501


        :return: The is_spot of this V1InstanceOverprovisioningSpec.  # noqa: E501
        :rtype: bool
        """
        return self._is_spot

    @is_spot.setter
    def is_spot(self, is_spot: 'bool'):
        """Sets the is_spot of this V1InstanceOverprovisioningSpec.


        :param is_spot: The is_spot of this V1InstanceOverprovisioningSpec.  # noqa: E501
        :type: bool
        """

        self._is_spot = is_spot

    @property
    def resource_type(self) -> 'str':
        """Gets the resource_type of this V1InstanceOverprovisioningSpec.  # noqa: E501


        :return: The resource_type of this V1InstanceOverprovisioningSpec.  # noqa: E501
        :rtype: str
        """
        return self._resource_type

    @resource_type.setter
    def resource_type(self, resource_type: 'str'):
        """Sets the resource_type of this V1InstanceOverprovisioningSpec.


        :param resource_type: The resource_type of this V1InstanceOverprovisioningSpec.  # noqa: E501
        :type: str
        """

        self._resource_type = resource_type

    @property
    def volume_size(self) -> 'int':
        """Gets the volume_size of this V1InstanceOverprovisioningSpec.  # noqa: E501


        :return: The volume_size of this V1InstanceOverprovisioningSpec.  # noqa: E501
        :rtype: int
        """
        return self._volume_size

    @volume_size.setter
    def volume_size(self, volume_size: 'int'):
        """Sets the volume_size of this V1InstanceOverprovisioningSpec.


        :param volume_size: The volume_size of this V1InstanceOverprovisioningSpec.  # noqa: E501
        :type: int
        """

        self._volume_size = volume_size

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
        if issubclass(V1InstanceOverprovisioningSpec, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1InstanceOverprovisioningSpec') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1InstanceOverprovisioningSpec):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1InstanceOverprovisioningSpec') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
