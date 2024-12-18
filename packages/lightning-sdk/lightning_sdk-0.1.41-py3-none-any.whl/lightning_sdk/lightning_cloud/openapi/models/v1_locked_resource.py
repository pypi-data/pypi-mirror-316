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

class V1LockedResource(object):
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
        'created_at': 'datetime',
        'id': 'str',
        'name': 'str',
        'type': 'str',
        'updated_at': 'datetime'
    }

    attribute_map = {
        'created_at': 'createdAt',
        'id': 'id',
        'name': 'name',
        'type': 'type',
        'updated_at': 'updatedAt'
    }

    def __init__(self, created_at: 'datetime' =None, id: 'str' =None, name: 'str' =None, type: 'str' =None, updated_at: 'datetime' =None):  # noqa: E501
        """V1LockedResource - a model defined in Swagger"""  # noqa: E501
        self._created_at = None
        self._id = None
        self._name = None
        self._type = None
        self._updated_at = None
        self.discriminator = None
        if created_at is not None:
            self.created_at = created_at
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if type is not None:
            self.type = type
        if updated_at is not None:
            self.updated_at = updated_at

    @property
    def created_at(self) -> 'datetime':
        """Gets the created_at of this V1LockedResource.  # noqa: E501


        :return: The created_at of this V1LockedResource.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at: 'datetime'):
        """Sets the created_at of this V1LockedResource.


        :param created_at: The created_at of this V1LockedResource.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def id(self) -> 'str':
        """Gets the id of this V1LockedResource.  # noqa: E501


        :return: The id of this V1LockedResource.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: 'str'):
        """Sets the id of this V1LockedResource.


        :param id: The id of this V1LockedResource.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self) -> 'str':
        """Gets the name of this V1LockedResource.  # noqa: E501


        :return: The name of this V1LockedResource.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: 'str'):
        """Sets the name of this V1LockedResource.


        :param name: The name of this V1LockedResource.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def type(self) -> 'str':
        """Gets the type of this V1LockedResource.  # noqa: E501


        :return: The type of this V1LockedResource.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: 'str'):
        """Sets the type of this V1LockedResource.


        :param type: The type of this V1LockedResource.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def updated_at(self) -> 'datetime':
        """Gets the updated_at of this V1LockedResource.  # noqa: E501


        :return: The updated_at of this V1LockedResource.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at: 'datetime'):
        """Sets the updated_at of this V1LockedResource.


        :param updated_at: The updated_at of this V1LockedResource.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

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
        if issubclass(V1LockedResource, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1LockedResource') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1LockedResource):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1LockedResource') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
