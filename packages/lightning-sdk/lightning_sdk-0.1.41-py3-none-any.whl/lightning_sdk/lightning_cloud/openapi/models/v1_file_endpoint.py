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

class V1FileEndpoint(object):
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
        'arguments': 'list[V1CommandArgument]',
        'cloudspace_id': 'str',
        'cluster_id': 'str',
        'command': 'str',
        'description': 'str',
        'function_name': 'str',
        'id': 'str',
        'method': 'str',
        'path': 'str',
        'plugin_id': 'str',
        'project_id': 'str',
        'project_owner_name': 'str',
        'published': 'bool',
        'user_id': 'str'
    }

    attribute_map = {
        'arguments': 'arguments',
        'cloudspace_id': 'cloudspaceId',
        'cluster_id': 'clusterId',
        'command': 'command',
        'description': 'description',
        'function_name': 'functionName',
        'id': 'id',
        'method': 'method',
        'path': 'path',
        'plugin_id': 'pluginId',
        'project_id': 'projectId',
        'project_owner_name': 'projectOwnerName',
        'published': 'published',
        'user_id': 'userId'
    }

    def __init__(self, arguments: 'list[V1CommandArgument]' =None, cloudspace_id: 'str' =None, cluster_id: 'str' =None, command: 'str' =None, description: 'str' =None, function_name: 'str' =None, id: 'str' =None, method: 'str' =None, path: 'str' =None, plugin_id: 'str' =None, project_id: 'str' =None, project_owner_name: 'str' =None, published: 'bool' =None, user_id: 'str' =None):  # noqa: E501
        """V1FileEndpoint - a model defined in Swagger"""  # noqa: E501
        self._arguments = None
        self._cloudspace_id = None
        self._cluster_id = None
        self._command = None
        self._description = None
        self._function_name = None
        self._id = None
        self._method = None
        self._path = None
        self._plugin_id = None
        self._project_id = None
        self._project_owner_name = None
        self._published = None
        self._user_id = None
        self.discriminator = None
        if arguments is not None:
            self.arguments = arguments
        if cloudspace_id is not None:
            self.cloudspace_id = cloudspace_id
        if cluster_id is not None:
            self.cluster_id = cluster_id
        if command is not None:
            self.command = command
        if description is not None:
            self.description = description
        if function_name is not None:
            self.function_name = function_name
        if id is not None:
            self.id = id
        if method is not None:
            self.method = method
        if path is not None:
            self.path = path
        if plugin_id is not None:
            self.plugin_id = plugin_id
        if project_id is not None:
            self.project_id = project_id
        if project_owner_name is not None:
            self.project_owner_name = project_owner_name
        if published is not None:
            self.published = published
        if user_id is not None:
            self.user_id = user_id

    @property
    def arguments(self) -> 'list[V1CommandArgument]':
        """Gets the arguments of this V1FileEndpoint.  # noqa: E501


        :return: The arguments of this V1FileEndpoint.  # noqa: E501
        :rtype: list[V1CommandArgument]
        """
        return self._arguments

    @arguments.setter
    def arguments(self, arguments: 'list[V1CommandArgument]'):
        """Sets the arguments of this V1FileEndpoint.


        :param arguments: The arguments of this V1FileEndpoint.  # noqa: E501
        :type: list[V1CommandArgument]
        """

        self._arguments = arguments

    @property
    def cloudspace_id(self) -> 'str':
        """Gets the cloudspace_id of this V1FileEndpoint.  # noqa: E501


        :return: The cloudspace_id of this V1FileEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._cloudspace_id

    @cloudspace_id.setter
    def cloudspace_id(self, cloudspace_id: 'str'):
        """Sets the cloudspace_id of this V1FileEndpoint.


        :param cloudspace_id: The cloudspace_id of this V1FileEndpoint.  # noqa: E501
        :type: str
        """

        self._cloudspace_id = cloudspace_id

    @property
    def cluster_id(self) -> 'str':
        """Gets the cluster_id of this V1FileEndpoint.  # noqa: E501


        :return: The cluster_id of this V1FileEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._cluster_id

    @cluster_id.setter
    def cluster_id(self, cluster_id: 'str'):
        """Sets the cluster_id of this V1FileEndpoint.


        :param cluster_id: The cluster_id of this V1FileEndpoint.  # noqa: E501
        :type: str
        """

        self._cluster_id = cluster_id

    @property
    def command(self) -> 'str':
        """Gets the command of this V1FileEndpoint.  # noqa: E501


        :return: The command of this V1FileEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._command

    @command.setter
    def command(self, command: 'str'):
        """Sets the command of this V1FileEndpoint.


        :param command: The command of this V1FileEndpoint.  # noqa: E501
        :type: str
        """

        self._command = command

    @property
    def description(self) -> 'str':
        """Gets the description of this V1FileEndpoint.  # noqa: E501


        :return: The description of this V1FileEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: 'str'):
        """Sets the description of this V1FileEndpoint.


        :param description: The description of this V1FileEndpoint.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def function_name(self) -> 'str':
        """Gets the function_name of this V1FileEndpoint.  # noqa: E501


        :return: The function_name of this V1FileEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._function_name

    @function_name.setter
    def function_name(self, function_name: 'str'):
        """Sets the function_name of this V1FileEndpoint.


        :param function_name: The function_name of this V1FileEndpoint.  # noqa: E501
        :type: str
        """

        self._function_name = function_name

    @property
    def id(self) -> 'str':
        """Gets the id of this V1FileEndpoint.  # noqa: E501


        :return: The id of this V1FileEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: 'str'):
        """Sets the id of this V1FileEndpoint.


        :param id: The id of this V1FileEndpoint.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def method(self) -> 'str':
        """Gets the method of this V1FileEndpoint.  # noqa: E501


        :return: The method of this V1FileEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._method

    @method.setter
    def method(self, method: 'str'):
        """Sets the method of this V1FileEndpoint.


        :param method: The method of this V1FileEndpoint.  # noqa: E501
        :type: str
        """

        self._method = method

    @property
    def path(self) -> 'str':
        """Gets the path of this V1FileEndpoint.  # noqa: E501


        :return: The path of this V1FileEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path: 'str'):
        """Sets the path of this V1FileEndpoint.


        :param path: The path of this V1FileEndpoint.  # noqa: E501
        :type: str
        """

        self._path = path

    @property
    def plugin_id(self) -> 'str':
        """Gets the plugin_id of this V1FileEndpoint.  # noqa: E501


        :return: The plugin_id of this V1FileEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._plugin_id

    @plugin_id.setter
    def plugin_id(self, plugin_id: 'str'):
        """Sets the plugin_id of this V1FileEndpoint.


        :param plugin_id: The plugin_id of this V1FileEndpoint.  # noqa: E501
        :type: str
        """

        self._plugin_id = plugin_id

    @property
    def project_id(self) -> 'str':
        """Gets the project_id of this V1FileEndpoint.  # noqa: E501


        :return: The project_id of this V1FileEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id: 'str'):
        """Sets the project_id of this V1FileEndpoint.


        :param project_id: The project_id of this V1FileEndpoint.  # noqa: E501
        :type: str
        """

        self._project_id = project_id

    @property
    def project_owner_name(self) -> 'str':
        """Gets the project_owner_name of this V1FileEndpoint.  # noqa: E501


        :return: The project_owner_name of this V1FileEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._project_owner_name

    @project_owner_name.setter
    def project_owner_name(self, project_owner_name: 'str'):
        """Sets the project_owner_name of this V1FileEndpoint.


        :param project_owner_name: The project_owner_name of this V1FileEndpoint.  # noqa: E501
        :type: str
        """

        self._project_owner_name = project_owner_name

    @property
    def published(self) -> 'bool':
        """Gets the published of this V1FileEndpoint.  # noqa: E501


        :return: The published of this V1FileEndpoint.  # noqa: E501
        :rtype: bool
        """
        return self._published

    @published.setter
    def published(self, published: 'bool'):
        """Sets the published of this V1FileEndpoint.


        :param published: The published of this V1FileEndpoint.  # noqa: E501
        :type: bool
        """

        self._published = published

    @property
    def user_id(self) -> 'str':
        """Gets the user_id of this V1FileEndpoint.  # noqa: E501


        :return: The user_id of this V1FileEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: 'str'):
        """Sets the user_id of this V1FileEndpoint.


        :param user_id: The user_id of this V1FileEndpoint.  # noqa: E501
        :type: str
        """

        self._user_id = user_id

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
        if issubclass(V1FileEndpoint, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1FileEndpoint') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1FileEndpoint):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1FileEndpoint') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
