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

class V1DeploymentStatus(object):
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
        'deleting_replicas': 'str',
        'failing_replicas': 'str',
        'first_job_state_current_release': 'str',
        'message': 'str',
        'pending_replicas': 'str',
        'ready_replicas': 'str',
        'urls': 'list[str]'
    }

    attribute_map = {
        'deleting_replicas': 'deletingReplicas',
        'failing_replicas': 'failingReplicas',
        'first_job_state_current_release': 'firstJobStateCurrentRelease',
        'message': 'message',
        'pending_replicas': 'pendingReplicas',
        'ready_replicas': 'readyReplicas',
        'urls': 'urls'
    }

    def __init__(self, deleting_replicas: 'str' =None, failing_replicas: 'str' =None, first_job_state_current_release: 'str' =None, message: 'str' =None, pending_replicas: 'str' =None, ready_replicas: 'str' =None, urls: 'list[str]' =None):  # noqa: E501
        """V1DeploymentStatus - a model defined in Swagger"""  # noqa: E501
        self._deleting_replicas = None
        self._failing_replicas = None
        self._first_job_state_current_release = None
        self._message = None
        self._pending_replicas = None
        self._ready_replicas = None
        self._urls = None
        self.discriminator = None
        if deleting_replicas is not None:
            self.deleting_replicas = deleting_replicas
        if failing_replicas is not None:
            self.failing_replicas = failing_replicas
        if first_job_state_current_release is not None:
            self.first_job_state_current_release = first_job_state_current_release
        if message is not None:
            self.message = message
        if pending_replicas is not None:
            self.pending_replicas = pending_replicas
        if ready_replicas is not None:
            self.ready_replicas = ready_replicas
        if urls is not None:
            self.urls = urls

    @property
    def deleting_replicas(self) -> 'str':
        """Gets the deleting_replicas of this V1DeploymentStatus.  # noqa: E501


        :return: The deleting_replicas of this V1DeploymentStatus.  # noqa: E501
        :rtype: str
        """
        return self._deleting_replicas

    @deleting_replicas.setter
    def deleting_replicas(self, deleting_replicas: 'str'):
        """Sets the deleting_replicas of this V1DeploymentStatus.


        :param deleting_replicas: The deleting_replicas of this V1DeploymentStatus.  # noqa: E501
        :type: str
        """

        self._deleting_replicas = deleting_replicas

    @property
    def failing_replicas(self) -> 'str':
        """Gets the failing_replicas of this V1DeploymentStatus.  # noqa: E501


        :return: The failing_replicas of this V1DeploymentStatus.  # noqa: E501
        :rtype: str
        """
        return self._failing_replicas

    @failing_replicas.setter
    def failing_replicas(self, failing_replicas: 'str'):
        """Sets the failing_replicas of this V1DeploymentStatus.


        :param failing_replicas: The failing_replicas of this V1DeploymentStatus.  # noqa: E501
        :type: str
        """

        self._failing_replicas = failing_replicas

    @property
    def first_job_state_current_release(self) -> 'str':
        """Gets the first_job_state_current_release of this V1DeploymentStatus.  # noqa: E501


        :return: The first_job_state_current_release of this V1DeploymentStatus.  # noqa: E501
        :rtype: str
        """
        return self._first_job_state_current_release

    @first_job_state_current_release.setter
    def first_job_state_current_release(self, first_job_state_current_release: 'str'):
        """Sets the first_job_state_current_release of this V1DeploymentStatus.


        :param first_job_state_current_release: The first_job_state_current_release of this V1DeploymentStatus.  # noqa: E501
        :type: str
        """

        self._first_job_state_current_release = first_job_state_current_release

    @property
    def message(self) -> 'str':
        """Gets the message of this V1DeploymentStatus.  # noqa: E501


        :return: The message of this V1DeploymentStatus.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message: 'str'):
        """Sets the message of this V1DeploymentStatus.


        :param message: The message of this V1DeploymentStatus.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def pending_replicas(self) -> 'str':
        """Gets the pending_replicas of this V1DeploymentStatus.  # noqa: E501


        :return: The pending_replicas of this V1DeploymentStatus.  # noqa: E501
        :rtype: str
        """
        return self._pending_replicas

    @pending_replicas.setter
    def pending_replicas(self, pending_replicas: 'str'):
        """Sets the pending_replicas of this V1DeploymentStatus.


        :param pending_replicas: The pending_replicas of this V1DeploymentStatus.  # noqa: E501
        :type: str
        """

        self._pending_replicas = pending_replicas

    @property
    def ready_replicas(self) -> 'str':
        """Gets the ready_replicas of this V1DeploymentStatus.  # noqa: E501


        :return: The ready_replicas of this V1DeploymentStatus.  # noqa: E501
        :rtype: str
        """
        return self._ready_replicas

    @ready_replicas.setter
    def ready_replicas(self, ready_replicas: 'str'):
        """Sets the ready_replicas of this V1DeploymentStatus.


        :param ready_replicas: The ready_replicas of this V1DeploymentStatus.  # noqa: E501
        :type: str
        """

        self._ready_replicas = ready_replicas

    @property
    def urls(self) -> 'list[str]':
        """Gets the urls of this V1DeploymentStatus.  # noqa: E501


        :return: The urls of this V1DeploymentStatus.  # noqa: E501
        :rtype: list[str]
        """
        return self._urls

    @urls.setter
    def urls(self, urls: 'list[str]'):
        """Sets the urls of this V1DeploymentStatus.


        :param urls: The urls of this V1DeploymentStatus.  # noqa: E501
        :type: list[str]
        """

        self._urls = urls

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
        if issubclass(V1DeploymentStatus, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1DeploymentStatus') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1DeploymentStatus):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1DeploymentStatus') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
