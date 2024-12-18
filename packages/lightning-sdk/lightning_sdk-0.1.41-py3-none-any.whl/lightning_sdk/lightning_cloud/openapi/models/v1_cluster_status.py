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

class V1ClusterStatus(object):
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
        'aws_v1_region_status': 'list[V1AWSDirectV1Status]',
        'dependency_service_health': 'list[V1ServiceHealth]',
        'gcp_v1_status': 'V1GoogleCloudDirectV1Status',
        'last_healthcheck_timestamp': 'datetime',
        'phase': 'V1ClusterState',
        'prometheus_endpoint': 'str',
        'queue_endpoint': 'str',
        'reason': 'str',
        'slurm_v1_status': 'V1SlurmV1Status',
        'ssh_gateway_endpoint': 'str',
        'storage_endpoint': 'str'
    }

    attribute_map = {
        'aws_v1_region_status': 'awsV1RegionStatus',
        'dependency_service_health': 'dependencyServiceHealth',
        'gcp_v1_status': 'gcpV1Status',
        'last_healthcheck_timestamp': 'lastHealthcheckTimestamp',
        'phase': 'phase',
        'prometheus_endpoint': 'prometheusEndpoint',
        'queue_endpoint': 'queueEndpoint',
        'reason': 'reason',
        'slurm_v1_status': 'slurmV1Status',
        'ssh_gateway_endpoint': 'sshGatewayEndpoint',
        'storage_endpoint': 'storageEndpoint'
    }

    def __init__(self, aws_v1_region_status: 'list[V1AWSDirectV1Status]' =None, dependency_service_health: 'list[V1ServiceHealth]' =None, gcp_v1_status: 'V1GoogleCloudDirectV1Status' =None, last_healthcheck_timestamp: 'datetime' =None, phase: 'V1ClusterState' =None, prometheus_endpoint: 'str' =None, queue_endpoint: 'str' =None, reason: 'str' =None, slurm_v1_status: 'V1SlurmV1Status' =None, ssh_gateway_endpoint: 'str' =None, storage_endpoint: 'str' =None):  # noqa: E501
        """V1ClusterStatus - a model defined in Swagger"""  # noqa: E501
        self._aws_v1_region_status = None
        self._dependency_service_health = None
        self._gcp_v1_status = None
        self._last_healthcheck_timestamp = None
        self._phase = None
        self._prometheus_endpoint = None
        self._queue_endpoint = None
        self._reason = None
        self._slurm_v1_status = None
        self._ssh_gateway_endpoint = None
        self._storage_endpoint = None
        self.discriminator = None
        if aws_v1_region_status is not None:
            self.aws_v1_region_status = aws_v1_region_status
        if dependency_service_health is not None:
            self.dependency_service_health = dependency_service_health
        if gcp_v1_status is not None:
            self.gcp_v1_status = gcp_v1_status
        if last_healthcheck_timestamp is not None:
            self.last_healthcheck_timestamp = last_healthcheck_timestamp
        if phase is not None:
            self.phase = phase
        if prometheus_endpoint is not None:
            self.prometheus_endpoint = prometheus_endpoint
        if queue_endpoint is not None:
            self.queue_endpoint = queue_endpoint
        if reason is not None:
            self.reason = reason
        if slurm_v1_status is not None:
            self.slurm_v1_status = slurm_v1_status
        if ssh_gateway_endpoint is not None:
            self.ssh_gateway_endpoint = ssh_gateway_endpoint
        if storage_endpoint is not None:
            self.storage_endpoint = storage_endpoint

    @property
    def aws_v1_region_status(self) -> 'list[V1AWSDirectV1Status]':
        """Gets the aws_v1_region_status of this V1ClusterStatus.  # noqa: E501


        :return: The aws_v1_region_status of this V1ClusterStatus.  # noqa: E501
        :rtype: list[V1AWSDirectV1Status]
        """
        return self._aws_v1_region_status

    @aws_v1_region_status.setter
    def aws_v1_region_status(self, aws_v1_region_status: 'list[V1AWSDirectV1Status]'):
        """Sets the aws_v1_region_status of this V1ClusterStatus.


        :param aws_v1_region_status: The aws_v1_region_status of this V1ClusterStatus.  # noqa: E501
        :type: list[V1AWSDirectV1Status]
        """

        self._aws_v1_region_status = aws_v1_region_status

    @property
    def dependency_service_health(self) -> 'list[V1ServiceHealth]':
        """Gets the dependency_service_health of this V1ClusterStatus.  # noqa: E501


        :return: The dependency_service_health of this V1ClusterStatus.  # noqa: E501
        :rtype: list[V1ServiceHealth]
        """
        return self._dependency_service_health

    @dependency_service_health.setter
    def dependency_service_health(self, dependency_service_health: 'list[V1ServiceHealth]'):
        """Sets the dependency_service_health of this V1ClusterStatus.


        :param dependency_service_health: The dependency_service_health of this V1ClusterStatus.  # noqa: E501
        :type: list[V1ServiceHealth]
        """

        self._dependency_service_health = dependency_service_health

    @property
    def gcp_v1_status(self) -> 'V1GoogleCloudDirectV1Status':
        """Gets the gcp_v1_status of this V1ClusterStatus.  # noqa: E501


        :return: The gcp_v1_status of this V1ClusterStatus.  # noqa: E501
        :rtype: V1GoogleCloudDirectV1Status
        """
        return self._gcp_v1_status

    @gcp_v1_status.setter
    def gcp_v1_status(self, gcp_v1_status: 'V1GoogleCloudDirectV1Status'):
        """Sets the gcp_v1_status of this V1ClusterStatus.


        :param gcp_v1_status: The gcp_v1_status of this V1ClusterStatus.  # noqa: E501
        :type: V1GoogleCloudDirectV1Status
        """

        self._gcp_v1_status = gcp_v1_status

    @property
    def last_healthcheck_timestamp(self) -> 'datetime':
        """Gets the last_healthcheck_timestamp of this V1ClusterStatus.  # noqa: E501


        :return: The last_healthcheck_timestamp of this V1ClusterStatus.  # noqa: E501
        :rtype: datetime
        """
        return self._last_healthcheck_timestamp

    @last_healthcheck_timestamp.setter
    def last_healthcheck_timestamp(self, last_healthcheck_timestamp: 'datetime'):
        """Sets the last_healthcheck_timestamp of this V1ClusterStatus.


        :param last_healthcheck_timestamp: The last_healthcheck_timestamp of this V1ClusterStatus.  # noqa: E501
        :type: datetime
        """

        self._last_healthcheck_timestamp = last_healthcheck_timestamp

    @property
    def phase(self) -> 'V1ClusterState':
        """Gets the phase of this V1ClusterStatus.  # noqa: E501


        :return: The phase of this V1ClusterStatus.  # noqa: E501
        :rtype: V1ClusterState
        """
        return self._phase

    @phase.setter
    def phase(self, phase: 'V1ClusterState'):
        """Sets the phase of this V1ClusterStatus.


        :param phase: The phase of this V1ClusterStatus.  # noqa: E501
        :type: V1ClusterState
        """

        self._phase = phase

    @property
    def prometheus_endpoint(self) -> 'str':
        """Gets the prometheus_endpoint of this V1ClusterStatus.  # noqa: E501

        endpoint to get prometheus metrics from cluster workloads.  # noqa: E501

        :return: The prometheus_endpoint of this V1ClusterStatus.  # noqa: E501
        :rtype: str
        """
        return self._prometheus_endpoint

    @prometheus_endpoint.setter
    def prometheus_endpoint(self, prometheus_endpoint: 'str'):
        """Sets the prometheus_endpoint of this V1ClusterStatus.

        endpoint to get prometheus metrics from cluster workloads.  # noqa: E501

        :param prometheus_endpoint: The prometheus_endpoint of this V1ClusterStatus.  # noqa: E501
        :type: str
        """

        self._prometheus_endpoint = prometheus_endpoint

    @property
    def queue_endpoint(self) -> 'str':
        """Gets the queue_endpoint of this V1ClusterStatus.  # noqa: E501


        :return: The queue_endpoint of this V1ClusterStatus.  # noqa: E501
        :rtype: str
        """
        return self._queue_endpoint

    @queue_endpoint.setter
    def queue_endpoint(self, queue_endpoint: 'str'):
        """Sets the queue_endpoint of this V1ClusterStatus.


        :param queue_endpoint: The queue_endpoint of this V1ClusterStatus.  # noqa: E501
        :type: str
        """

        self._queue_endpoint = queue_endpoint

    @property
    def reason(self) -> 'str':
        """Gets the reason of this V1ClusterStatus.  # noqa: E501


        :return: The reason of this V1ClusterStatus.  # noqa: E501
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason: 'str'):
        """Sets the reason of this V1ClusterStatus.


        :param reason: The reason of this V1ClusterStatus.  # noqa: E501
        :type: str
        """

        self._reason = reason

    @property
    def slurm_v1_status(self) -> 'V1SlurmV1Status':
        """Gets the slurm_v1_status of this V1ClusterStatus.  # noqa: E501


        :return: The slurm_v1_status of this V1ClusterStatus.  # noqa: E501
        :rtype: V1SlurmV1Status
        """
        return self._slurm_v1_status

    @slurm_v1_status.setter
    def slurm_v1_status(self, slurm_v1_status: 'V1SlurmV1Status'):
        """Sets the slurm_v1_status of this V1ClusterStatus.


        :param slurm_v1_status: The slurm_v1_status of this V1ClusterStatus.  # noqa: E501
        :type: V1SlurmV1Status
        """

        self._slurm_v1_status = slurm_v1_status

    @property
    def ssh_gateway_endpoint(self) -> 'str':
        """Gets the ssh_gateway_endpoint of this V1ClusterStatus.  # noqa: E501

        ssh dns to be used to access lightning flow & work.  # noqa: E501

        :return: The ssh_gateway_endpoint of this V1ClusterStatus.  # noqa: E501
        :rtype: str
        """
        return self._ssh_gateway_endpoint

    @ssh_gateway_endpoint.setter
    def ssh_gateway_endpoint(self, ssh_gateway_endpoint: 'str'):
        """Sets the ssh_gateway_endpoint of this V1ClusterStatus.

        ssh dns to be used to access lightning flow & work.  # noqa: E501

        :param ssh_gateway_endpoint: The ssh_gateway_endpoint of this V1ClusterStatus.  # noqa: E501
        :type: str
        """

        self._ssh_gateway_endpoint = ssh_gateway_endpoint

    @property
    def storage_endpoint(self) -> 'str':
        """Gets the storage_endpoint of this V1ClusterStatus.  # noqa: E501


        :return: The storage_endpoint of this V1ClusterStatus.  # noqa: E501
        :rtype: str
        """
        return self._storage_endpoint

    @storage_endpoint.setter
    def storage_endpoint(self, storage_endpoint: 'str'):
        """Sets the storage_endpoint of this V1ClusterStatus.


        :param storage_endpoint: The storage_endpoint of this V1ClusterStatus.  # noqa: E501
        :type: str
        """

        self._storage_endpoint = storage_endpoint

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
        if issubclass(V1ClusterStatus, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1ClusterStatus') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1ClusterStatus):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1ClusterStatus') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
