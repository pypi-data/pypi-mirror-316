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

class V1CloudSpaceCodeVersion(object):
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
        'cloud_space_id': 'str',
        'created_at': 'datetime',
        'id': 'str',
        'name': 'str',
        'number_of_files': 'str',
        'status': 'V1CloudSpaceCodeVersionStatus',
        'sync_duration': 'str',
        'sync_percentage': 'str',
        'total_size_bytes': 'str',
        'updated_at': 'datetime',
        'user_id': 'str'
    }

    attribute_map = {
        'cloud_space_id': 'cloudSpaceId',
        'created_at': 'createdAt',
        'id': 'id',
        'name': 'name',
        'number_of_files': 'numberOfFiles',
        'status': 'status',
        'sync_duration': 'syncDuration',
        'sync_percentage': 'syncPercentage',
        'total_size_bytes': 'totalSizeBytes',
        'updated_at': 'updatedAt',
        'user_id': 'userId'
    }

    def __init__(self, cloud_space_id: 'str' =None, created_at: 'datetime' =None, id: 'str' =None, name: 'str' =None, number_of_files: 'str' =None, status: 'V1CloudSpaceCodeVersionStatus' =None, sync_duration: 'str' =None, sync_percentage: 'str' =None, total_size_bytes: 'str' =None, updated_at: 'datetime' =None, user_id: 'str' =None):  # noqa: E501
        """V1CloudSpaceCodeVersion - a model defined in Swagger"""  # noqa: E501
        self._cloud_space_id = None
        self._created_at = None
        self._id = None
        self._name = None
        self._number_of_files = None
        self._status = None
        self._sync_duration = None
        self._sync_percentage = None
        self._total_size_bytes = None
        self._updated_at = None
        self._user_id = None
        self.discriminator = None
        if cloud_space_id is not None:
            self.cloud_space_id = cloud_space_id
        if created_at is not None:
            self.created_at = created_at
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if number_of_files is not None:
            self.number_of_files = number_of_files
        if status is not None:
            self.status = status
        if sync_duration is not None:
            self.sync_duration = sync_duration
        if sync_percentage is not None:
            self.sync_percentage = sync_percentage
        if total_size_bytes is not None:
            self.total_size_bytes = total_size_bytes
        if updated_at is not None:
            self.updated_at = updated_at
        if user_id is not None:
            self.user_id = user_id

    @property
    def cloud_space_id(self) -> 'str':
        """Gets the cloud_space_id of this V1CloudSpaceCodeVersion.  # noqa: E501


        :return: The cloud_space_id of this V1CloudSpaceCodeVersion.  # noqa: E501
        :rtype: str
        """
        return self._cloud_space_id

    @cloud_space_id.setter
    def cloud_space_id(self, cloud_space_id: 'str'):
        """Sets the cloud_space_id of this V1CloudSpaceCodeVersion.


        :param cloud_space_id: The cloud_space_id of this V1CloudSpaceCodeVersion.  # noqa: E501
        :type: str
        """

        self._cloud_space_id = cloud_space_id

    @property
    def created_at(self) -> 'datetime':
        """Gets the created_at of this V1CloudSpaceCodeVersion.  # noqa: E501


        :return: The created_at of this V1CloudSpaceCodeVersion.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at: 'datetime'):
        """Sets the created_at of this V1CloudSpaceCodeVersion.


        :param created_at: The created_at of this V1CloudSpaceCodeVersion.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def id(self) -> 'str':
        """Gets the id of this V1CloudSpaceCodeVersion.  # noqa: E501


        :return: The id of this V1CloudSpaceCodeVersion.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: 'str'):
        """Sets the id of this V1CloudSpaceCodeVersion.


        :param id: The id of this V1CloudSpaceCodeVersion.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self) -> 'str':
        """Gets the name of this V1CloudSpaceCodeVersion.  # noqa: E501


        :return: The name of this V1CloudSpaceCodeVersion.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: 'str'):
        """Sets the name of this V1CloudSpaceCodeVersion.


        :param name: The name of this V1CloudSpaceCodeVersion.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def number_of_files(self) -> 'str':
        """Gets the number_of_files of this V1CloudSpaceCodeVersion.  # noqa: E501


        :return: The number_of_files of this V1CloudSpaceCodeVersion.  # noqa: E501
        :rtype: str
        """
        return self._number_of_files

    @number_of_files.setter
    def number_of_files(self, number_of_files: 'str'):
        """Sets the number_of_files of this V1CloudSpaceCodeVersion.


        :param number_of_files: The number_of_files of this V1CloudSpaceCodeVersion.  # noqa: E501
        :type: str
        """

        self._number_of_files = number_of_files

    @property
    def status(self) -> 'V1CloudSpaceCodeVersionStatus':
        """Gets the status of this V1CloudSpaceCodeVersion.  # noqa: E501


        :return: The status of this V1CloudSpaceCodeVersion.  # noqa: E501
        :rtype: V1CloudSpaceCodeVersionStatus
        """
        return self._status

    @status.setter
    def status(self, status: 'V1CloudSpaceCodeVersionStatus'):
        """Sets the status of this V1CloudSpaceCodeVersion.


        :param status: The status of this V1CloudSpaceCodeVersion.  # noqa: E501
        :type: V1CloudSpaceCodeVersionStatus
        """

        self._status = status

    @property
    def sync_duration(self) -> 'str':
        """Gets the sync_duration of this V1CloudSpaceCodeVersion.  # noqa: E501


        :return: The sync_duration of this V1CloudSpaceCodeVersion.  # noqa: E501
        :rtype: str
        """
        return self._sync_duration

    @sync_duration.setter
    def sync_duration(self, sync_duration: 'str'):
        """Sets the sync_duration of this V1CloudSpaceCodeVersion.


        :param sync_duration: The sync_duration of this V1CloudSpaceCodeVersion.  # noqa: E501
        :type: str
        """

        self._sync_duration = sync_duration

    @property
    def sync_percentage(self) -> 'str':
        """Gets the sync_percentage of this V1CloudSpaceCodeVersion.  # noqa: E501


        :return: The sync_percentage of this V1CloudSpaceCodeVersion.  # noqa: E501
        :rtype: str
        """
        return self._sync_percentage

    @sync_percentage.setter
    def sync_percentage(self, sync_percentage: 'str'):
        """Sets the sync_percentage of this V1CloudSpaceCodeVersion.


        :param sync_percentage: The sync_percentage of this V1CloudSpaceCodeVersion.  # noqa: E501
        :type: str
        """

        self._sync_percentage = sync_percentage

    @property
    def total_size_bytes(self) -> 'str':
        """Gets the total_size_bytes of this V1CloudSpaceCodeVersion.  # noqa: E501


        :return: The total_size_bytes of this V1CloudSpaceCodeVersion.  # noqa: E501
        :rtype: str
        """
        return self._total_size_bytes

    @total_size_bytes.setter
    def total_size_bytes(self, total_size_bytes: 'str'):
        """Sets the total_size_bytes of this V1CloudSpaceCodeVersion.


        :param total_size_bytes: The total_size_bytes of this V1CloudSpaceCodeVersion.  # noqa: E501
        :type: str
        """

        self._total_size_bytes = total_size_bytes

    @property
    def updated_at(self) -> 'datetime':
        """Gets the updated_at of this V1CloudSpaceCodeVersion.  # noqa: E501


        :return: The updated_at of this V1CloudSpaceCodeVersion.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at: 'datetime'):
        """Sets the updated_at of this V1CloudSpaceCodeVersion.


        :param updated_at: The updated_at of this V1CloudSpaceCodeVersion.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def user_id(self) -> 'str':
        """Gets the user_id of this V1CloudSpaceCodeVersion.  # noqa: E501


        :return: The user_id of this V1CloudSpaceCodeVersion.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: 'str'):
        """Sets the user_id of this V1CloudSpaceCodeVersion.


        :param user_id: The user_id of this V1CloudSpaceCodeVersion.  # noqa: E501
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
        if issubclass(V1CloudSpaceCodeVersion, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1CloudSpaceCodeVersion') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1CloudSpaceCodeVersion):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1CloudSpaceCodeVersion') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
