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

class V1ImageSpec(object):
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
        'actions_on_image_build_end': 'list[str]',
        'actions_on_image_build_start': 'list[str]',
        'dependency_file_info': 'V1DependencyFileInfo',
        'dockerfile': 'str',
        'image': 'str',
        'on_image_build_commands': 'list[str]',
        'relative_working_dir': 'str'
    }

    attribute_map = {
        'actions_on_image_build_end': 'actionsOnImageBuildEnd',
        'actions_on_image_build_start': 'actionsOnImageBuildStart',
        'dependency_file_info': 'dependencyFileInfo',
        'dockerfile': 'dockerfile',
        'image': 'image',
        'on_image_build_commands': 'onImageBuildCommands',
        'relative_working_dir': 'relativeWorkingDir'
    }

    def __init__(self, actions_on_image_build_end: 'list[str]' =None, actions_on_image_build_start: 'list[str]' =None, dependency_file_info: 'V1DependencyFileInfo' =None, dockerfile: 'str' =None, image: 'str' =None, on_image_build_commands: 'list[str]' =None, relative_working_dir: 'str' =None):  # noqa: E501
        """V1ImageSpec - a model defined in Swagger"""  # noqa: E501
        self._actions_on_image_build_end = None
        self._actions_on_image_build_start = None
        self._dependency_file_info = None
        self._dockerfile = None
        self._image = None
        self._on_image_build_commands = None
        self._relative_working_dir = None
        self.discriminator = None
        if actions_on_image_build_end is not None:
            self.actions_on_image_build_end = actions_on_image_build_end
        if actions_on_image_build_start is not None:
            self.actions_on_image_build_start = actions_on_image_build_start
        if dependency_file_info is not None:
            self.dependency_file_info = dependency_file_info
        if dockerfile is not None:
            self.dockerfile = dockerfile
        if image is not None:
            self.image = image
        if on_image_build_commands is not None:
            self.on_image_build_commands = on_image_build_commands
        if relative_working_dir is not None:
            self.relative_working_dir = relative_working_dir

    @property
    def actions_on_image_build_end(self) -> 'list[str]':
        """Gets the actions_on_image_build_end of this V1ImageSpec.  # noqa: E501

        commands passed to the image builder which are interpreted as RUN commands in a Dockerfile. Executes after installing dependencies from package manager.  # noqa: E501

        :return: The actions_on_image_build_end of this V1ImageSpec.  # noqa: E501
        :rtype: list[str]
        """
        return self._actions_on_image_build_end

    @actions_on_image_build_end.setter
    def actions_on_image_build_end(self, actions_on_image_build_end: 'list[str]'):
        """Sets the actions_on_image_build_end of this V1ImageSpec.

        commands passed to the image builder which are interpreted as RUN commands in a Dockerfile. Executes after installing dependencies from package manager.  # noqa: E501

        :param actions_on_image_build_end: The actions_on_image_build_end of this V1ImageSpec.  # noqa: E501
        :type: list[str]
        """

        self._actions_on_image_build_end = actions_on_image_build_end

    @property
    def actions_on_image_build_start(self) -> 'list[str]':
        """Gets the actions_on_image_build_start of this V1ImageSpec.  # noqa: E501

        commands passed to the image builder which are interpreted as RUN commands in a Dockerfile. Executes before installing dependencies from package manager.  # noqa: E501

        :return: The actions_on_image_build_start of this V1ImageSpec.  # noqa: E501
        :rtype: list[str]
        """
        return self._actions_on_image_build_start

    @actions_on_image_build_start.setter
    def actions_on_image_build_start(self, actions_on_image_build_start: 'list[str]'):
        """Sets the actions_on_image_build_start of this V1ImageSpec.

        commands passed to the image builder which are interpreted as RUN commands in a Dockerfile. Executes before installing dependencies from package manager.  # noqa: E501

        :param actions_on_image_build_start: The actions_on_image_build_start of this V1ImageSpec.  # noqa: E501
        :type: list[str]
        """

        self._actions_on_image_build_start = actions_on_image_build_start

    @property
    def dependency_file_info(self) -> 'V1DependencyFileInfo':
        """Gets the dependency_file_info of this V1ImageSpec.  # noqa: E501


        :return: The dependency_file_info of this V1ImageSpec.  # noqa: E501
        :rtype: V1DependencyFileInfo
        """
        return self._dependency_file_info

    @dependency_file_info.setter
    def dependency_file_info(self, dependency_file_info: 'V1DependencyFileInfo'):
        """Sets the dependency_file_info of this V1ImageSpec.


        :param dependency_file_info: The dependency_file_info of this V1ImageSpec.  # noqa: E501
        :type: V1DependencyFileInfo
        """

        self._dependency_file_info = dependency_file_info

    @property
    def dockerfile(self) -> 'str':
        """Gets the dockerfile of this V1ImageSpec.  # noqa: E501

        this is a relative path to a dockerfile within the build context.  # noqa: E501

        :return: The dockerfile of this V1ImageSpec.  # noqa: E501
        :rtype: str
        """
        return self._dockerfile

    @dockerfile.setter
    def dockerfile(self, dockerfile: 'str'):
        """Sets the dockerfile of this V1ImageSpec.

        this is a relative path to a dockerfile within the build context.  # noqa: E501

        :param dockerfile: The dockerfile of this V1ImageSpec.  # noqa: E501
        :type: str
        """

        self._dockerfile = dockerfile

    @property
    def image(self) -> 'str':
        """Gets the image of this V1ImageSpec.  # noqa: E501

        name of the base image to use when rendering dockerfile templates.  # noqa: E501

        :return: The image of this V1ImageSpec.  # noqa: E501
        :rtype: str
        """
        return self._image

    @image.setter
    def image(self, image: 'str'):
        """Sets the image of this V1ImageSpec.

        name of the base image to use when rendering dockerfile templates.  # noqa: E501

        :param image: The image of this V1ImageSpec.  # noqa: E501
        :type: str
        """

        self._image = image

    @property
    def on_image_build_commands(self) -> 'list[str]':
        """Gets the on_image_build_commands of this V1ImageSpec.  # noqa: E501

        DEPRECATED: DO NOT USE! Build commands to add as RUN instructions. These instructions are executed before any dependencies are installed.  # noqa: E501

        :return: The on_image_build_commands of this V1ImageSpec.  # noqa: E501
        :rtype: list[str]
        """
        return self._on_image_build_commands

    @on_image_build_commands.setter
    def on_image_build_commands(self, on_image_build_commands: 'list[str]'):
        """Sets the on_image_build_commands of this V1ImageSpec.

        DEPRECATED: DO NOT USE! Build commands to add as RUN instructions. These instructions are executed before any dependencies are installed.  # noqa: E501

        :param on_image_build_commands: The on_image_build_commands of this V1ImageSpec.  # noqa: E501
        :type: list[str]
        """

        self._on_image_build_commands = on_image_build_commands

    @property
    def relative_working_dir(self) -> 'str':
        """Gets the relative_working_dir of this V1ImageSpec.  # noqa: E501


        :return: The relative_working_dir of this V1ImageSpec.  # noqa: E501
        :rtype: str
        """
        return self._relative_working_dir

    @relative_working_dir.setter
    def relative_working_dir(self, relative_working_dir: 'str'):
        """Sets the relative_working_dir of this V1ImageSpec.


        :param relative_working_dir: The relative_working_dir of this V1ImageSpec.  # noqa: E501
        :type: str
        """

        self._relative_working_dir = relative_working_dir

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
        if issubclass(V1ImageSpec, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1ImageSpec') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1ImageSpec):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1ImageSpec') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
