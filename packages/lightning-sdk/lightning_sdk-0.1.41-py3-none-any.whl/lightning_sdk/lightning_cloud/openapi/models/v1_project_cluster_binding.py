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

class V1ProjectClusterBinding(object):
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
        'cluster_id': 'str',
        'cluster_name': 'str',
        'cluster_region': 'str',
        'created_at': 'datetime',
        'is_cluster_healthy': 'bool',
        'project_id': 'str',
        'updated_at': 'datetime'
    }

    attribute_map = {
        'cluster_id': 'clusterId',
        'cluster_name': 'clusterName',
        'cluster_region': 'clusterRegion',
        'created_at': 'createdAt',
        'is_cluster_healthy': 'isClusterHealthy',
        'project_id': 'projectId',
        'updated_at': 'updatedAt'
    }

    def __init__(self, cluster_id: 'str' =None, cluster_name: 'str' =None, cluster_region: 'str' =None, created_at: 'datetime' =None, is_cluster_healthy: 'bool' =None, project_id: 'str' =None, updated_at: 'datetime' =None):  # noqa: E501
        """V1ProjectClusterBinding - a model defined in Swagger"""  # noqa: E501
        self._cluster_id = None
        self._cluster_name = None
        self._cluster_region = None
        self._created_at = None
        self._is_cluster_healthy = None
        self._project_id = None
        self._updated_at = None
        self.discriminator = None
        if cluster_id is not None:
            self.cluster_id = cluster_id
        if cluster_name is not None:
            self.cluster_name = cluster_name
        if cluster_region is not None:
            self.cluster_region = cluster_region
        if created_at is not None:
            self.created_at = created_at
        if is_cluster_healthy is not None:
            self.is_cluster_healthy = is_cluster_healthy
        if project_id is not None:
            self.project_id = project_id
        if updated_at is not None:
            self.updated_at = updated_at

    @property
    def cluster_id(self) -> 'str':
        """Gets the cluster_id of this V1ProjectClusterBinding.  # noqa: E501


        :return: The cluster_id of this V1ProjectClusterBinding.  # noqa: E501
        :rtype: str
        """
        return self._cluster_id

    @cluster_id.setter
    def cluster_id(self, cluster_id: 'str'):
        """Sets the cluster_id of this V1ProjectClusterBinding.


        :param cluster_id: The cluster_id of this V1ProjectClusterBinding.  # noqa: E501
        :type: str
        """

        self._cluster_id = cluster_id

    @property
    def cluster_name(self) -> 'str':
        """Gets the cluster_name of this V1ProjectClusterBinding.  # noqa: E501


        :return: The cluster_name of this V1ProjectClusterBinding.  # noqa: E501
        :rtype: str
        """
        return self._cluster_name

    @cluster_name.setter
    def cluster_name(self, cluster_name: 'str'):
        """Sets the cluster_name of this V1ProjectClusterBinding.


        :param cluster_name: The cluster_name of this V1ProjectClusterBinding.  # noqa: E501
        :type: str
        """

        self._cluster_name = cluster_name

    @property
    def cluster_region(self) -> 'str':
        """Gets the cluster_region of this V1ProjectClusterBinding.  # noqa: E501


        :return: The cluster_region of this V1ProjectClusterBinding.  # noqa: E501
        :rtype: str
        """
        return self._cluster_region

    @cluster_region.setter
    def cluster_region(self, cluster_region: 'str'):
        """Sets the cluster_region of this V1ProjectClusterBinding.


        :param cluster_region: The cluster_region of this V1ProjectClusterBinding.  # noqa: E501
        :type: str
        """

        self._cluster_region = cluster_region

    @property
    def created_at(self) -> 'datetime':
        """Gets the created_at of this V1ProjectClusterBinding.  # noqa: E501


        :return: The created_at of this V1ProjectClusterBinding.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at: 'datetime'):
        """Sets the created_at of this V1ProjectClusterBinding.


        :param created_at: The created_at of this V1ProjectClusterBinding.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def is_cluster_healthy(self) -> 'bool':
        """Gets the is_cluster_healthy of this V1ProjectClusterBinding.  # noqa: E501


        :return: The is_cluster_healthy of this V1ProjectClusterBinding.  # noqa: E501
        :rtype: bool
        """
        return self._is_cluster_healthy

    @is_cluster_healthy.setter
    def is_cluster_healthy(self, is_cluster_healthy: 'bool'):
        """Sets the is_cluster_healthy of this V1ProjectClusterBinding.


        :param is_cluster_healthy: The is_cluster_healthy of this V1ProjectClusterBinding.  # noqa: E501
        :type: bool
        """

        self._is_cluster_healthy = is_cluster_healthy

    @property
    def project_id(self) -> 'str':
        """Gets the project_id of this V1ProjectClusterBinding.  # noqa: E501


        :return: The project_id of this V1ProjectClusterBinding.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id: 'str'):
        """Sets the project_id of this V1ProjectClusterBinding.


        :param project_id: The project_id of this V1ProjectClusterBinding.  # noqa: E501
        :type: str
        """

        self._project_id = project_id

    @property
    def updated_at(self) -> 'datetime':
        """Gets the updated_at of this V1ProjectClusterBinding.  # noqa: E501


        :return: The updated_at of this V1ProjectClusterBinding.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at: 'datetime'):
        """Sets the updated_at of this V1ProjectClusterBinding.


        :param updated_at: The updated_at of this V1ProjectClusterBinding.  # noqa: E501
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
        if issubclass(V1ProjectClusterBinding, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1ProjectClusterBinding') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1ProjectClusterBinding):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1ProjectClusterBinding') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
