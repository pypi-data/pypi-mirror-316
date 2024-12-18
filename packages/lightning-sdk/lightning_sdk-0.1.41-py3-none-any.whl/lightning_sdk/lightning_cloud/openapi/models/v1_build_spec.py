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

class V1BuildSpec(object):
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
        'commands': 'list[str]',
        'image': 'str',
        'python_dependencies': 'V1PythonDependencyInfo',
        'working_dir': 'str'
    }

    attribute_map = {
        'commands': 'commands',
        'image': 'image',
        'python_dependencies': 'pythonDependencies',
        'working_dir': 'workingDir'
    }

    def __init__(self, commands: 'list[str]' =None, image: 'str' =None, python_dependencies: 'V1PythonDependencyInfo' =None, working_dir: 'str' =None):  # noqa: E501
        """V1BuildSpec - a model defined in Swagger"""  # noqa: E501
        self._commands = None
        self._image = None
        self._python_dependencies = None
        self._working_dir = None
        self.discriminator = None
        if commands is not None:
            self.commands = commands
        if image is not None:
            self.image = image
        if python_dependencies is not None:
            self.python_dependencies = python_dependencies
        if working_dir is not None:
            self.working_dir = working_dir

    @property
    def commands(self) -> 'list[str]':
        """Gets the commands of this V1BuildSpec.  # noqa: E501


        :return: The commands of this V1BuildSpec.  # noqa: E501
        :rtype: list[str]
        """
        return self._commands

    @commands.setter
    def commands(self, commands: 'list[str]'):
        """Sets the commands of this V1BuildSpec.


        :param commands: The commands of this V1BuildSpec.  # noqa: E501
        :type: list[str]
        """

        self._commands = commands

    @property
    def image(self) -> 'str':
        """Gets the image of this V1BuildSpec.  # noqa: E501

        A custom Docker image to run the user's workload in. This image must be publicly accessible and not hosted by DockerHub or other registries that enforce image pull rate limits.  # noqa: E501

        :return: The image of this V1BuildSpec.  # noqa: E501
        :rtype: str
        """
        return self._image

    @image.setter
    def image(self, image: 'str'):
        """Sets the image of this V1BuildSpec.

        A custom Docker image to run the user's workload in. This image must be publicly accessible and not hosted by DockerHub or other registries that enforce image pull rate limits.  # noqa: E501

        :param image: The image of this V1BuildSpec.  # noqa: E501
        :type: str
        """

        self._image = image

    @property
    def python_dependencies(self) -> 'V1PythonDependencyInfo':
        """Gets the python_dependencies of this V1BuildSpec.  # noqa: E501


        :return: The python_dependencies of this V1BuildSpec.  # noqa: E501
        :rtype: V1PythonDependencyInfo
        """
        return self._python_dependencies

    @python_dependencies.setter
    def python_dependencies(self, python_dependencies: 'V1PythonDependencyInfo'):
        """Sets the python_dependencies of this V1BuildSpec.


        :param python_dependencies: The python_dependencies of this V1BuildSpec.  # noqa: E501
        :type: V1PythonDependencyInfo
        """

        self._python_dependencies = python_dependencies

    @property
    def working_dir(self) -> 'str':
        """Gets the working_dir of this V1BuildSpec.  # noqa: E501

        Working directory for the workload. Source will be cloned here and the app work will be started from this directory.  # noqa: E501

        :return: The working_dir of this V1BuildSpec.  # noqa: E501
        :rtype: str
        """
        return self._working_dir

    @working_dir.setter
    def working_dir(self, working_dir: 'str'):
        """Sets the working_dir of this V1BuildSpec.

        Working directory for the workload. Source will be cloned here and the app work will be started from this directory.  # noqa: E501

        :param working_dir: The working_dir of this V1BuildSpec.  # noqa: E501
        :type: str
        """

        self._working_dir = working_dir

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
        if issubclass(V1BuildSpec, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1BuildSpec') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1BuildSpec):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1BuildSpec') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
