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

class V1SlurmNode(object):
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
        'address': 'str',
        'alloc_cpus': 'int',
        'alloc_memory': 'str',
        'architecture': 'str',
        'cores': 'int',
        'cpus': 'int',
        'free_memory': 'str',
        'gpu_type': 'str',
        'gpus': 'int',
        'hostname': 'str',
        'idle_cpus': 'int',
        'name': 'str',
        'operating_system': 'str',
        'slurmd_version': 'str',
        'state': 'str'
    }

    attribute_map = {
        'address': 'address',
        'alloc_cpus': 'allocCpus',
        'alloc_memory': 'allocMemory',
        'architecture': 'architecture',
        'cores': 'cores',
        'cpus': 'cpus',
        'free_memory': 'freeMemory',
        'gpu_type': 'gpuType',
        'gpus': 'gpus',
        'hostname': 'hostname',
        'idle_cpus': 'idleCpus',
        'name': 'name',
        'operating_system': 'operatingSystem',
        'slurmd_version': 'slurmdVersion',
        'state': 'state'
    }

    def __init__(self, address: 'str' =None, alloc_cpus: 'int' =None, alloc_memory: 'str' =None, architecture: 'str' =None, cores: 'int' =None, cpus: 'int' =None, free_memory: 'str' =None, gpu_type: 'str' =None, gpus: 'int' =None, hostname: 'str' =None, idle_cpus: 'int' =None, name: 'str' =None, operating_system: 'str' =None, slurmd_version: 'str' =None, state: 'str' =None):  # noqa: E501
        """V1SlurmNode - a model defined in Swagger"""  # noqa: E501
        self._address = None
        self._alloc_cpus = None
        self._alloc_memory = None
        self._architecture = None
        self._cores = None
        self._cpus = None
        self._free_memory = None
        self._gpu_type = None
        self._gpus = None
        self._hostname = None
        self._idle_cpus = None
        self._name = None
        self._operating_system = None
        self._slurmd_version = None
        self._state = None
        self.discriminator = None
        if address is not None:
            self.address = address
        if alloc_cpus is not None:
            self.alloc_cpus = alloc_cpus
        if alloc_memory is not None:
            self.alloc_memory = alloc_memory
        if architecture is not None:
            self.architecture = architecture
        if cores is not None:
            self.cores = cores
        if cpus is not None:
            self.cpus = cpus
        if free_memory is not None:
            self.free_memory = free_memory
        if gpu_type is not None:
            self.gpu_type = gpu_type
        if gpus is not None:
            self.gpus = gpus
        if hostname is not None:
            self.hostname = hostname
        if idle_cpus is not None:
            self.idle_cpus = idle_cpus
        if name is not None:
            self.name = name
        if operating_system is not None:
            self.operating_system = operating_system
        if slurmd_version is not None:
            self.slurmd_version = slurmd_version
        if state is not None:
            self.state = state

    @property
    def address(self) -> 'str':
        """Gets the address of this V1SlurmNode.  # noqa: E501


        :return: The address of this V1SlurmNode.  # noqa: E501
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address: 'str'):
        """Sets the address of this V1SlurmNode.


        :param address: The address of this V1SlurmNode.  # noqa: E501
        :type: str
        """

        self._address = address

    @property
    def alloc_cpus(self) -> 'int':
        """Gets the alloc_cpus of this V1SlurmNode.  # noqa: E501


        :return: The alloc_cpus of this V1SlurmNode.  # noqa: E501
        :rtype: int
        """
        return self._alloc_cpus

    @alloc_cpus.setter
    def alloc_cpus(self, alloc_cpus: 'int'):
        """Sets the alloc_cpus of this V1SlurmNode.


        :param alloc_cpus: The alloc_cpus of this V1SlurmNode.  # noqa: E501
        :type: int
        """

        self._alloc_cpus = alloc_cpus

    @property
    def alloc_memory(self) -> 'str':
        """Gets the alloc_memory of this V1SlurmNode.  # noqa: E501


        :return: The alloc_memory of this V1SlurmNode.  # noqa: E501
        :rtype: str
        """
        return self._alloc_memory

    @alloc_memory.setter
    def alloc_memory(self, alloc_memory: 'str'):
        """Sets the alloc_memory of this V1SlurmNode.


        :param alloc_memory: The alloc_memory of this V1SlurmNode.  # noqa: E501
        :type: str
        """

        self._alloc_memory = alloc_memory

    @property
    def architecture(self) -> 'str':
        """Gets the architecture of this V1SlurmNode.  # noqa: E501


        :return: The architecture of this V1SlurmNode.  # noqa: E501
        :rtype: str
        """
        return self._architecture

    @architecture.setter
    def architecture(self, architecture: 'str'):
        """Sets the architecture of this V1SlurmNode.


        :param architecture: The architecture of this V1SlurmNode.  # noqa: E501
        :type: str
        """

        self._architecture = architecture

    @property
    def cores(self) -> 'int':
        """Gets the cores of this V1SlurmNode.  # noqa: E501


        :return: The cores of this V1SlurmNode.  # noqa: E501
        :rtype: int
        """
        return self._cores

    @cores.setter
    def cores(self, cores: 'int'):
        """Sets the cores of this V1SlurmNode.


        :param cores: The cores of this V1SlurmNode.  # noqa: E501
        :type: int
        """

        self._cores = cores

    @property
    def cpus(self) -> 'int':
        """Gets the cpus of this V1SlurmNode.  # noqa: E501


        :return: The cpus of this V1SlurmNode.  # noqa: E501
        :rtype: int
        """
        return self._cpus

    @cpus.setter
    def cpus(self, cpus: 'int'):
        """Sets the cpus of this V1SlurmNode.


        :param cpus: The cpus of this V1SlurmNode.  # noqa: E501
        :type: int
        """

        self._cpus = cpus

    @property
    def free_memory(self) -> 'str':
        """Gets the free_memory of this V1SlurmNode.  # noqa: E501


        :return: The free_memory of this V1SlurmNode.  # noqa: E501
        :rtype: str
        """
        return self._free_memory

    @free_memory.setter
    def free_memory(self, free_memory: 'str'):
        """Sets the free_memory of this V1SlurmNode.


        :param free_memory: The free_memory of this V1SlurmNode.  # noqa: E501
        :type: str
        """

        self._free_memory = free_memory

    @property
    def gpu_type(self) -> 'str':
        """Gets the gpu_type of this V1SlurmNode.  # noqa: E501


        :return: The gpu_type of this V1SlurmNode.  # noqa: E501
        :rtype: str
        """
        return self._gpu_type

    @gpu_type.setter
    def gpu_type(self, gpu_type: 'str'):
        """Sets the gpu_type of this V1SlurmNode.


        :param gpu_type: The gpu_type of this V1SlurmNode.  # noqa: E501
        :type: str
        """

        self._gpu_type = gpu_type

    @property
    def gpus(self) -> 'int':
        """Gets the gpus of this V1SlurmNode.  # noqa: E501


        :return: The gpus of this V1SlurmNode.  # noqa: E501
        :rtype: int
        """
        return self._gpus

    @gpus.setter
    def gpus(self, gpus: 'int'):
        """Sets the gpus of this V1SlurmNode.


        :param gpus: The gpus of this V1SlurmNode.  # noqa: E501
        :type: int
        """

        self._gpus = gpus

    @property
    def hostname(self) -> 'str':
        """Gets the hostname of this V1SlurmNode.  # noqa: E501


        :return: The hostname of this V1SlurmNode.  # noqa: E501
        :rtype: str
        """
        return self._hostname

    @hostname.setter
    def hostname(self, hostname: 'str'):
        """Sets the hostname of this V1SlurmNode.


        :param hostname: The hostname of this V1SlurmNode.  # noqa: E501
        :type: str
        """

        self._hostname = hostname

    @property
    def idle_cpus(self) -> 'int':
        """Gets the idle_cpus of this V1SlurmNode.  # noqa: E501


        :return: The idle_cpus of this V1SlurmNode.  # noqa: E501
        :rtype: int
        """
        return self._idle_cpus

    @idle_cpus.setter
    def idle_cpus(self, idle_cpus: 'int'):
        """Sets the idle_cpus of this V1SlurmNode.


        :param idle_cpus: The idle_cpus of this V1SlurmNode.  # noqa: E501
        :type: int
        """

        self._idle_cpus = idle_cpus

    @property
    def name(self) -> 'str':
        """Gets the name of this V1SlurmNode.  # noqa: E501


        :return: The name of this V1SlurmNode.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: 'str'):
        """Sets the name of this V1SlurmNode.


        :param name: The name of this V1SlurmNode.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def operating_system(self) -> 'str':
        """Gets the operating_system of this V1SlurmNode.  # noqa: E501


        :return: The operating_system of this V1SlurmNode.  # noqa: E501
        :rtype: str
        """
        return self._operating_system

    @operating_system.setter
    def operating_system(self, operating_system: 'str'):
        """Sets the operating_system of this V1SlurmNode.


        :param operating_system: The operating_system of this V1SlurmNode.  # noqa: E501
        :type: str
        """

        self._operating_system = operating_system

    @property
    def slurmd_version(self) -> 'str':
        """Gets the slurmd_version of this V1SlurmNode.  # noqa: E501


        :return: The slurmd_version of this V1SlurmNode.  # noqa: E501
        :rtype: str
        """
        return self._slurmd_version

    @slurmd_version.setter
    def slurmd_version(self, slurmd_version: 'str'):
        """Sets the slurmd_version of this V1SlurmNode.


        :param slurmd_version: The slurmd_version of this V1SlurmNode.  # noqa: E501
        :type: str
        """

        self._slurmd_version = slurmd_version

    @property
    def state(self) -> 'str':
        """Gets the state of this V1SlurmNode.  # noqa: E501


        :return: The state of this V1SlurmNode.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state: 'str'):
        """Sets the state of this V1SlurmNode.


        :param state: The state of this V1SlurmNode.  # noqa: E501
        :type: str
        """

        self._state = state

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
        if issubclass(V1SlurmNode, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1SlurmNode') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1SlurmNode):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1SlurmNode') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
