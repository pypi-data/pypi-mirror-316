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

class SlurmJobsBody(object):
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
        'cache_id': 'str',
        'cloudspace_id': 'str',
        'cluster_id': 'str',
        'command': 'str',
        'name': 'str',
        'num_gpus': 'str',
        'service_id': 'str',
        'sync_env': 'bool',
        'work_dir': 'str'
    }

    attribute_map = {
        'cache_id': 'cacheId',
        'cloudspace_id': 'cloudspaceId',
        'cluster_id': 'clusterId',
        'command': 'command',
        'name': 'name',
        'num_gpus': 'numGpus',
        'service_id': 'serviceId',
        'sync_env': 'syncEnv',
        'work_dir': 'workDir'
    }

    def __init__(self, cache_id: 'str' =None, cloudspace_id: 'str' =None, cluster_id: 'str' =None, command: 'str' =None, name: 'str' =None, num_gpus: 'str' =None, service_id: 'str' =None, sync_env: 'bool' =None, work_dir: 'str' =None):  # noqa: E501
        """SlurmJobsBody - a model defined in Swagger"""  # noqa: E501
        self._cache_id = None
        self._cloudspace_id = None
        self._cluster_id = None
        self._command = None
        self._name = None
        self._num_gpus = None
        self._service_id = None
        self._sync_env = None
        self._work_dir = None
        self.discriminator = None
        if cache_id is not None:
            self.cache_id = cache_id
        if cloudspace_id is not None:
            self.cloudspace_id = cloudspace_id
        if cluster_id is not None:
            self.cluster_id = cluster_id
        if command is not None:
            self.command = command
        if name is not None:
            self.name = name
        if num_gpus is not None:
            self.num_gpus = num_gpus
        if service_id is not None:
            self.service_id = service_id
        if sync_env is not None:
            self.sync_env = sync_env
        if work_dir is not None:
            self.work_dir = work_dir

    @property
    def cache_id(self) -> 'str':
        """Gets the cache_id of this SlurmJobsBody.  # noqa: E501


        :return: The cache_id of this SlurmJobsBody.  # noqa: E501
        :rtype: str
        """
        return self._cache_id

    @cache_id.setter
    def cache_id(self, cache_id: 'str'):
        """Sets the cache_id of this SlurmJobsBody.


        :param cache_id: The cache_id of this SlurmJobsBody.  # noqa: E501
        :type: str
        """

        self._cache_id = cache_id

    @property
    def cloudspace_id(self) -> 'str':
        """Gets the cloudspace_id of this SlurmJobsBody.  # noqa: E501


        :return: The cloudspace_id of this SlurmJobsBody.  # noqa: E501
        :rtype: str
        """
        return self._cloudspace_id

    @cloudspace_id.setter
    def cloudspace_id(self, cloudspace_id: 'str'):
        """Sets the cloudspace_id of this SlurmJobsBody.


        :param cloudspace_id: The cloudspace_id of this SlurmJobsBody.  # noqa: E501
        :type: str
        """

        self._cloudspace_id = cloudspace_id

    @property
    def cluster_id(self) -> 'str':
        """Gets the cluster_id of this SlurmJobsBody.  # noqa: E501


        :return: The cluster_id of this SlurmJobsBody.  # noqa: E501
        :rtype: str
        """
        return self._cluster_id

    @cluster_id.setter
    def cluster_id(self, cluster_id: 'str'):
        """Sets the cluster_id of this SlurmJobsBody.


        :param cluster_id: The cluster_id of this SlurmJobsBody.  # noqa: E501
        :type: str
        """

        self._cluster_id = cluster_id

    @property
    def command(self) -> 'str':
        """Gets the command of this SlurmJobsBody.  # noqa: E501


        :return: The command of this SlurmJobsBody.  # noqa: E501
        :rtype: str
        """
        return self._command

    @command.setter
    def command(self, command: 'str'):
        """Sets the command of this SlurmJobsBody.


        :param command: The command of this SlurmJobsBody.  # noqa: E501
        :type: str
        """

        self._command = command

    @property
    def name(self) -> 'str':
        """Gets the name of this SlurmJobsBody.  # noqa: E501

        required parameter when creating a job.  # noqa: E501

        :return: The name of this SlurmJobsBody.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: 'str'):
        """Sets the name of this SlurmJobsBody.

        required parameter when creating a job.  # noqa: E501

        :param name: The name of this SlurmJobsBody.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def num_gpus(self) -> 'str':
        """Gets the num_gpus of this SlurmJobsBody.  # noqa: E501


        :return: The num_gpus of this SlurmJobsBody.  # noqa: E501
        :rtype: str
        """
        return self._num_gpus

    @num_gpus.setter
    def num_gpus(self, num_gpus: 'str'):
        """Sets the num_gpus of this SlurmJobsBody.


        :param num_gpus: The num_gpus of this SlurmJobsBody.  # noqa: E501
        :type: str
        """

        self._num_gpus = num_gpus

    @property
    def service_id(self) -> 'str':
        """Gets the service_id of this SlurmJobsBody.  # noqa: E501


        :return: The service_id of this SlurmJobsBody.  # noqa: E501
        :rtype: str
        """
        return self._service_id

    @service_id.setter
    def service_id(self, service_id: 'str'):
        """Sets the service_id of this SlurmJobsBody.


        :param service_id: The service_id of this SlurmJobsBody.  # noqa: E501
        :type: str
        """

        self._service_id = service_id

    @property
    def sync_env(self) -> 'bool':
        """Gets the sync_env of this SlurmJobsBody.  # noqa: E501


        :return: The sync_env of this SlurmJobsBody.  # noqa: E501
        :rtype: bool
        """
        return self._sync_env

    @sync_env.setter
    def sync_env(self, sync_env: 'bool'):
        """Sets the sync_env of this SlurmJobsBody.


        :param sync_env: The sync_env of this SlurmJobsBody.  # noqa: E501
        :type: bool
        """

        self._sync_env = sync_env

    @property
    def work_dir(self) -> 'str':
        """Gets the work_dir of this SlurmJobsBody.  # noqa: E501


        :return: The work_dir of this SlurmJobsBody.  # noqa: E501
        :rtype: str
        """
        return self._work_dir

    @work_dir.setter
    def work_dir(self, work_dir: 'str'):
        """Sets the work_dir of this SlurmJobsBody.


        :param work_dir: The work_dir of this SlurmJobsBody.  # noqa: E501
        :type: str
        """

        self._work_dir = work_dir

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
        if issubclass(SlurmJobsBody, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'SlurmJobsBody') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, SlurmJobsBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'SlurmJobsBody') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
