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

class V1ManagedModelAbilities(object):
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
        'can_call_hub_deployment': 'bool',
        'can_receive_files': 'bool',
        'can_receive_images': 'bool'
    }

    attribute_map = {
        'can_call_hub_deployment': 'canCallHubDeployment',
        'can_receive_files': 'canReceiveFiles',
        'can_receive_images': 'canReceiveImages'
    }

    def __init__(self, can_call_hub_deployment: 'bool' =None, can_receive_files: 'bool' =None, can_receive_images: 'bool' =None):  # noqa: E501
        """V1ManagedModelAbilities - a model defined in Swagger"""  # noqa: E501
        self._can_call_hub_deployment = None
        self._can_receive_files = None
        self._can_receive_images = None
        self.discriminator = None
        if can_call_hub_deployment is not None:
            self.can_call_hub_deployment = can_call_hub_deployment
        if can_receive_files is not None:
            self.can_receive_files = can_receive_files
        if can_receive_images is not None:
            self.can_receive_images = can_receive_images

    @property
    def can_call_hub_deployment(self) -> 'bool':
        """Gets the can_call_hub_deployment of this V1ManagedModelAbilities.  # noqa: E501


        :return: The can_call_hub_deployment of this V1ManagedModelAbilities.  # noqa: E501
        :rtype: bool
        """
        return self._can_call_hub_deployment

    @can_call_hub_deployment.setter
    def can_call_hub_deployment(self, can_call_hub_deployment: 'bool'):
        """Sets the can_call_hub_deployment of this V1ManagedModelAbilities.


        :param can_call_hub_deployment: The can_call_hub_deployment of this V1ManagedModelAbilities.  # noqa: E501
        :type: bool
        """

        self._can_call_hub_deployment = can_call_hub_deployment

    @property
    def can_receive_files(self) -> 'bool':
        """Gets the can_receive_files of this V1ManagedModelAbilities.  # noqa: E501


        :return: The can_receive_files of this V1ManagedModelAbilities.  # noqa: E501
        :rtype: bool
        """
        return self._can_receive_files

    @can_receive_files.setter
    def can_receive_files(self, can_receive_files: 'bool'):
        """Sets the can_receive_files of this V1ManagedModelAbilities.


        :param can_receive_files: The can_receive_files of this V1ManagedModelAbilities.  # noqa: E501
        :type: bool
        """

        self._can_receive_files = can_receive_files

    @property
    def can_receive_images(self) -> 'bool':
        """Gets the can_receive_images of this V1ManagedModelAbilities.  # noqa: E501


        :return: The can_receive_images of this V1ManagedModelAbilities.  # noqa: E501
        :rtype: bool
        """
        return self._can_receive_images

    @can_receive_images.setter
    def can_receive_images(self, can_receive_images: 'bool'):
        """Sets the can_receive_images of this V1ManagedModelAbilities.


        :param can_receive_images: The can_receive_images of this V1ManagedModelAbilities.  # noqa: E501
        :type: bool
        """

        self._can_receive_images = can_receive_images

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
        if issubclass(V1ManagedModelAbilities, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1ManagedModelAbilities') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1ManagedModelAbilities):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1ManagedModelAbilities') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
