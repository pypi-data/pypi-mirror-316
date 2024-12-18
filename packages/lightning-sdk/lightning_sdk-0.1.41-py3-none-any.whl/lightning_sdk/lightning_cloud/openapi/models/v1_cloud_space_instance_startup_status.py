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

class V1CloudSpaceInstanceStartupStatus(object):
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
        'initial_restore_at': 'datetime',
        'initial_restore_finished': 'bool',
        'started_at': 'datetime',
        'top_up_restore_at': 'datetime',
        'top_up_restore_finished': 'bool'
    }

    attribute_map = {
        'initial_restore_at': 'initialRestoreAt',
        'initial_restore_finished': 'initialRestoreFinished',
        'started_at': 'startedAt',
        'top_up_restore_at': 'topUpRestoreAt',
        'top_up_restore_finished': 'topUpRestoreFinished'
    }

    def __init__(self, initial_restore_at: 'datetime' =None, initial_restore_finished: 'bool' =None, started_at: 'datetime' =None, top_up_restore_at: 'datetime' =None, top_up_restore_finished: 'bool' =None):  # noqa: E501
        """V1CloudSpaceInstanceStartupStatus - a model defined in Swagger"""  # noqa: E501
        self._initial_restore_at = None
        self._initial_restore_finished = None
        self._started_at = None
        self._top_up_restore_at = None
        self._top_up_restore_finished = None
        self.discriminator = None
        if initial_restore_at is not None:
            self.initial_restore_at = initial_restore_at
        if initial_restore_finished is not None:
            self.initial_restore_finished = initial_restore_finished
        if started_at is not None:
            self.started_at = started_at
        if top_up_restore_at is not None:
            self.top_up_restore_at = top_up_restore_at
        if top_up_restore_finished is not None:
            self.top_up_restore_finished = top_up_restore_finished

    @property
    def initial_restore_at(self) -> 'datetime':
        """Gets the initial_restore_at of this V1CloudSpaceInstanceStartupStatus.  # noqa: E501


        :return: The initial_restore_at of this V1CloudSpaceInstanceStartupStatus.  # noqa: E501
        :rtype: datetime
        """
        return self._initial_restore_at

    @initial_restore_at.setter
    def initial_restore_at(self, initial_restore_at: 'datetime'):
        """Sets the initial_restore_at of this V1CloudSpaceInstanceStartupStatus.


        :param initial_restore_at: The initial_restore_at of this V1CloudSpaceInstanceStartupStatus.  # noqa: E501
        :type: datetime
        """

        self._initial_restore_at = initial_restore_at

    @property
    def initial_restore_finished(self) -> 'bool':
        """Gets the initial_restore_finished of this V1CloudSpaceInstanceStartupStatus.  # noqa: E501


        :return: The initial_restore_finished of this V1CloudSpaceInstanceStartupStatus.  # noqa: E501
        :rtype: bool
        """
        return self._initial_restore_finished

    @initial_restore_finished.setter
    def initial_restore_finished(self, initial_restore_finished: 'bool'):
        """Sets the initial_restore_finished of this V1CloudSpaceInstanceStartupStatus.


        :param initial_restore_finished: The initial_restore_finished of this V1CloudSpaceInstanceStartupStatus.  # noqa: E501
        :type: bool
        """

        self._initial_restore_finished = initial_restore_finished

    @property
    def started_at(self) -> 'datetime':
        """Gets the started_at of this V1CloudSpaceInstanceStartupStatus.  # noqa: E501


        :return: The started_at of this V1CloudSpaceInstanceStartupStatus.  # noqa: E501
        :rtype: datetime
        """
        return self._started_at

    @started_at.setter
    def started_at(self, started_at: 'datetime'):
        """Sets the started_at of this V1CloudSpaceInstanceStartupStatus.


        :param started_at: The started_at of this V1CloudSpaceInstanceStartupStatus.  # noqa: E501
        :type: datetime
        """

        self._started_at = started_at

    @property
    def top_up_restore_at(self) -> 'datetime':
        """Gets the top_up_restore_at of this V1CloudSpaceInstanceStartupStatus.  # noqa: E501


        :return: The top_up_restore_at of this V1CloudSpaceInstanceStartupStatus.  # noqa: E501
        :rtype: datetime
        """
        return self._top_up_restore_at

    @top_up_restore_at.setter
    def top_up_restore_at(self, top_up_restore_at: 'datetime'):
        """Sets the top_up_restore_at of this V1CloudSpaceInstanceStartupStatus.


        :param top_up_restore_at: The top_up_restore_at of this V1CloudSpaceInstanceStartupStatus.  # noqa: E501
        :type: datetime
        """

        self._top_up_restore_at = top_up_restore_at

    @property
    def top_up_restore_finished(self) -> 'bool':
        """Gets the top_up_restore_finished of this V1CloudSpaceInstanceStartupStatus.  # noqa: E501


        :return: The top_up_restore_finished of this V1CloudSpaceInstanceStartupStatus.  # noqa: E501
        :rtype: bool
        """
        return self._top_up_restore_finished

    @top_up_restore_finished.setter
    def top_up_restore_finished(self, top_up_restore_finished: 'bool'):
        """Sets the top_up_restore_finished of this V1CloudSpaceInstanceStartupStatus.


        :param top_up_restore_finished: The top_up_restore_finished of this V1CloudSpaceInstanceStartupStatus.  # noqa: E501
        :type: bool
        """

        self._top_up_restore_finished = top_up_restore_finished

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
        if issubclass(V1CloudSpaceInstanceStartupStatus, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1CloudSpaceInstanceStartupStatus') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1CloudSpaceInstanceStartupStatus):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1CloudSpaceInstanceStartupStatus') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
