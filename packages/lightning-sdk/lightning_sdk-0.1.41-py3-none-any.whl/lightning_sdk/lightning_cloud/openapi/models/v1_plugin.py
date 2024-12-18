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

class V1Plugin(object):
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
        'additional_info': 'str',
        'error': 'str',
        'id': 'str',
        'plugin_id': 'str',
        'project_id': 'str',
        'state': 'str'
    }

    attribute_map = {
        'additional_info': 'additionalInfo',
        'error': 'error',
        'id': 'id',
        'plugin_id': 'pluginId',
        'project_id': 'projectId',
        'state': 'state'
    }

    def __init__(self, additional_info: 'str' =None, error: 'str' =None, id: 'str' =None, plugin_id: 'str' =None, project_id: 'str' =None, state: 'str' =None):  # noqa: E501
        """V1Plugin - a model defined in Swagger"""  # noqa: E501
        self._additional_info = None
        self._error = None
        self._id = None
        self._plugin_id = None
        self._project_id = None
        self._state = None
        self.discriminator = None
        if additional_info is not None:
            self.additional_info = additional_info
        if error is not None:
            self.error = error
        if id is not None:
            self.id = id
        if plugin_id is not None:
            self.plugin_id = plugin_id
        if project_id is not None:
            self.project_id = project_id
        if state is not None:
            self.state = state

    @property
    def additional_info(self) -> 'str':
        """Gets the additional_info of this V1Plugin.  # noqa: E501


        :return: The additional_info of this V1Plugin.  # noqa: E501
        :rtype: str
        """
        return self._additional_info

    @additional_info.setter
    def additional_info(self, additional_info: 'str'):
        """Sets the additional_info of this V1Plugin.


        :param additional_info: The additional_info of this V1Plugin.  # noqa: E501
        :type: str
        """

        self._additional_info = additional_info

    @property
    def error(self) -> 'str':
        """Gets the error of this V1Plugin.  # noqa: E501


        :return: The error of this V1Plugin.  # noqa: E501
        :rtype: str
        """
        return self._error

    @error.setter
    def error(self, error: 'str'):
        """Sets the error of this V1Plugin.


        :param error: The error of this V1Plugin.  # noqa: E501
        :type: str
        """

        self._error = error

    @property
    def id(self) -> 'str':
        """Gets the id of this V1Plugin.  # noqa: E501


        :return: The id of this V1Plugin.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: 'str'):
        """Sets the id of this V1Plugin.


        :param id: The id of this V1Plugin.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def plugin_id(self) -> 'str':
        """Gets the plugin_id of this V1Plugin.  # noqa: E501


        :return: The plugin_id of this V1Plugin.  # noqa: E501
        :rtype: str
        """
        return self._plugin_id

    @plugin_id.setter
    def plugin_id(self, plugin_id: 'str'):
        """Sets the plugin_id of this V1Plugin.


        :param plugin_id: The plugin_id of this V1Plugin.  # noqa: E501
        :type: str
        """

        self._plugin_id = plugin_id

    @property
    def project_id(self) -> 'str':
        """Gets the project_id of this V1Plugin.  # noqa: E501


        :return: The project_id of this V1Plugin.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id: 'str'):
        """Sets the project_id of this V1Plugin.


        :param project_id: The project_id of this V1Plugin.  # noqa: E501
        :type: str
        """

        self._project_id = project_id

    @property
    def state(self) -> 'str':
        """Gets the state of this V1Plugin.  # noqa: E501


        :return: The state of this V1Plugin.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state: 'str'):
        """Sets the state of this V1Plugin.


        :param state: The state of this V1Plugin.  # noqa: E501
        :type: str
        """

        self._state = state

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
        if issubclass(V1Plugin, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1Plugin') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1Plugin):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1Plugin') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
