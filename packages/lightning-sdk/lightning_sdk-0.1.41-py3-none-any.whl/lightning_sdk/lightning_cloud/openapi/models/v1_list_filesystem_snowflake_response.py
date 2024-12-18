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

class V1ListFilesystemSnowflakeResponse(object):
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
        'snowflake_connections': 'list[V1FilesystemSnowflakeConnection]'
    }

    attribute_map = {
        'snowflake_connections': 'snowflakeConnections'
    }

    def __init__(self, snowflake_connections: 'list[V1FilesystemSnowflakeConnection]' =None):  # noqa: E501
        """V1ListFilesystemSnowflakeResponse - a model defined in Swagger"""  # noqa: E501
        self._snowflake_connections = None
        self.discriminator = None
        if snowflake_connections is not None:
            self.snowflake_connections = snowflake_connections

    @property
    def snowflake_connections(self) -> 'list[V1FilesystemSnowflakeConnection]':
        """Gets the snowflake_connections of this V1ListFilesystemSnowflakeResponse.  # noqa: E501


        :return: The snowflake_connections of this V1ListFilesystemSnowflakeResponse.  # noqa: E501
        :rtype: list[V1FilesystemSnowflakeConnection]
        """
        return self._snowflake_connections

    @snowflake_connections.setter
    def snowflake_connections(self, snowflake_connections: 'list[V1FilesystemSnowflakeConnection]'):
        """Sets the snowflake_connections of this V1ListFilesystemSnowflakeResponse.


        :param snowflake_connections: The snowflake_connections of this V1ListFilesystemSnowflakeResponse.  # noqa: E501
        :type: list[V1FilesystemSnowflakeConnection]
        """

        self._snowflake_connections = snowflake_connections

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
        if issubclass(V1ListFilesystemSnowflakeResponse, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1ListFilesystemSnowflakeResponse') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1ListFilesystemSnowflakeResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1ListFilesystemSnowflakeResponse') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
