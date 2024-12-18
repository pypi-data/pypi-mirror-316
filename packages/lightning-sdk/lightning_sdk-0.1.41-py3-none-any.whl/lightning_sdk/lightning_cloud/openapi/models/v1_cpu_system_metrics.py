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

class V1CPUSystemMetrics(object):
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
        'block_read': 'int',
        'block_write': 'int',
        'memory_percentage': 'int',
        'memory_total': 'int',
        'memory_used': 'int',
        'network_rx': 'int',
        'network_tx': 'int',
        'percentage': 'int',
        'percentage_per_cpu': 'list[float]'
    }

    attribute_map = {
        'block_read': 'blockRead',
        'block_write': 'blockWrite',
        'memory_percentage': 'memoryPercentage',
        'memory_total': 'memoryTotal',
        'memory_used': 'memoryUsed',
        'network_rx': 'networkRx',
        'network_tx': 'networkTx',
        'percentage': 'percentage',
        'percentage_per_cpu': 'percentagePerCpu'
    }

    def __init__(self, block_read: 'int' =None, block_write: 'int' =None, memory_percentage: 'int' =None, memory_total: 'int' =None, memory_used: 'int' =None, network_rx: 'int' =None, network_tx: 'int' =None, percentage: 'int' =None, percentage_per_cpu: 'list[float]' =None):  # noqa: E501
        """V1CPUSystemMetrics - a model defined in Swagger"""  # noqa: E501
        self._block_read = None
        self._block_write = None
        self._memory_percentage = None
        self._memory_total = None
        self._memory_used = None
        self._network_rx = None
        self._network_tx = None
        self._percentage = None
        self._percentage_per_cpu = None
        self.discriminator = None
        if block_read is not None:
            self.block_read = block_read
        if block_write is not None:
            self.block_write = block_write
        if memory_percentage is not None:
            self.memory_percentage = memory_percentage
        if memory_total is not None:
            self.memory_total = memory_total
        if memory_used is not None:
            self.memory_used = memory_used
        if network_rx is not None:
            self.network_rx = network_rx
        if network_tx is not None:
            self.network_tx = network_tx
        if percentage is not None:
            self.percentage = percentage
        if percentage_per_cpu is not None:
            self.percentage_per_cpu = percentage_per_cpu

    @property
    def block_read(self) -> 'int':
        """Gets the block_read of this V1CPUSystemMetrics.  # noqa: E501


        :return: The block_read of this V1CPUSystemMetrics.  # noqa: E501
        :rtype: int
        """
        return self._block_read

    @block_read.setter
    def block_read(self, block_read: 'int'):
        """Sets the block_read of this V1CPUSystemMetrics.


        :param block_read: The block_read of this V1CPUSystemMetrics.  # noqa: E501
        :type: int
        """

        self._block_read = block_read

    @property
    def block_write(self) -> 'int':
        """Gets the block_write of this V1CPUSystemMetrics.  # noqa: E501


        :return: The block_write of this V1CPUSystemMetrics.  # noqa: E501
        :rtype: int
        """
        return self._block_write

    @block_write.setter
    def block_write(self, block_write: 'int'):
        """Sets the block_write of this V1CPUSystemMetrics.


        :param block_write: The block_write of this V1CPUSystemMetrics.  # noqa: E501
        :type: int
        """

        self._block_write = block_write

    @property
    def memory_percentage(self) -> 'int':
        """Gets the memory_percentage of this V1CPUSystemMetrics.  # noqa: E501


        :return: The memory_percentage of this V1CPUSystemMetrics.  # noqa: E501
        :rtype: int
        """
        return self._memory_percentage

    @memory_percentage.setter
    def memory_percentage(self, memory_percentage: 'int'):
        """Sets the memory_percentage of this V1CPUSystemMetrics.


        :param memory_percentage: The memory_percentage of this V1CPUSystemMetrics.  # noqa: E501
        :type: int
        """

        self._memory_percentage = memory_percentage

    @property
    def memory_total(self) -> 'int':
        """Gets the memory_total of this V1CPUSystemMetrics.  # noqa: E501


        :return: The memory_total of this V1CPUSystemMetrics.  # noqa: E501
        :rtype: int
        """
        return self._memory_total

    @memory_total.setter
    def memory_total(self, memory_total: 'int'):
        """Sets the memory_total of this V1CPUSystemMetrics.


        :param memory_total: The memory_total of this V1CPUSystemMetrics.  # noqa: E501
        :type: int
        """

        self._memory_total = memory_total

    @property
    def memory_used(self) -> 'int':
        """Gets the memory_used of this V1CPUSystemMetrics.  # noqa: E501


        :return: The memory_used of this V1CPUSystemMetrics.  # noqa: E501
        :rtype: int
        """
        return self._memory_used

    @memory_used.setter
    def memory_used(self, memory_used: 'int'):
        """Sets the memory_used of this V1CPUSystemMetrics.


        :param memory_used: The memory_used of this V1CPUSystemMetrics.  # noqa: E501
        :type: int
        """

        self._memory_used = memory_used

    @property
    def network_rx(self) -> 'int':
        """Gets the network_rx of this V1CPUSystemMetrics.  # noqa: E501


        :return: The network_rx of this V1CPUSystemMetrics.  # noqa: E501
        :rtype: int
        """
        return self._network_rx

    @network_rx.setter
    def network_rx(self, network_rx: 'int'):
        """Sets the network_rx of this V1CPUSystemMetrics.


        :param network_rx: The network_rx of this V1CPUSystemMetrics.  # noqa: E501
        :type: int
        """

        self._network_rx = network_rx

    @property
    def network_tx(self) -> 'int':
        """Gets the network_tx of this V1CPUSystemMetrics.  # noqa: E501


        :return: The network_tx of this V1CPUSystemMetrics.  # noqa: E501
        :rtype: int
        """
        return self._network_tx

    @network_tx.setter
    def network_tx(self, network_tx: 'int'):
        """Sets the network_tx of this V1CPUSystemMetrics.


        :param network_tx: The network_tx of this V1CPUSystemMetrics.  # noqa: E501
        :type: int
        """

        self._network_tx = network_tx

    @property
    def percentage(self) -> 'int':
        """Gets the percentage of this V1CPUSystemMetrics.  # noqa: E501


        :return: The percentage of this V1CPUSystemMetrics.  # noqa: E501
        :rtype: int
        """
        return self._percentage

    @percentage.setter
    def percentage(self, percentage: 'int'):
        """Sets the percentage of this V1CPUSystemMetrics.


        :param percentage: The percentage of this V1CPUSystemMetrics.  # noqa: E501
        :type: int
        """

        self._percentage = percentage

    @property
    def percentage_per_cpu(self) -> 'list[float]':
        """Gets the percentage_per_cpu of this V1CPUSystemMetrics.  # noqa: E501


        :return: The percentage_per_cpu of this V1CPUSystemMetrics.  # noqa: E501
        :rtype: list[float]
        """
        return self._percentage_per_cpu

    @percentage_per_cpu.setter
    def percentage_per_cpu(self, percentage_per_cpu: 'list[float]'):
        """Sets the percentage_per_cpu of this V1CPUSystemMetrics.


        :param percentage_per_cpu: The percentage_per_cpu of this V1CPUSystemMetrics.  # noqa: E501
        :type: list[float]
        """

        self._percentage_per_cpu = percentage_per_cpu

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
        if issubclass(V1CPUSystemMetrics, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1CPUSystemMetrics') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1CPUSystemMetrics):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1CPUSystemMetrics') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
