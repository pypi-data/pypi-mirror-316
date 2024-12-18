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

class V1MultiMachineJobStatus(object):
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
        'deleting_machines': 'str',
        'failing_machines': 'str',
        'message': 'str',
        'pending_machines': 'str',
        'ready_machines': 'str',
        'started_at': 'datetime',
        'stopped_at': 'datetime'
    }

    attribute_map = {
        'deleting_machines': 'deletingMachines',
        'failing_machines': 'failingMachines',
        'message': 'message',
        'pending_machines': 'pendingMachines',
        'ready_machines': 'readyMachines',
        'started_at': 'startedAt',
        'stopped_at': 'stoppedAt'
    }

    def __init__(self, deleting_machines: 'str' =None, failing_machines: 'str' =None, message: 'str' =None, pending_machines: 'str' =None, ready_machines: 'str' =None, started_at: 'datetime' =None, stopped_at: 'datetime' =None):  # noqa: E501
        """V1MultiMachineJobStatus - a model defined in Swagger"""  # noqa: E501
        self._deleting_machines = None
        self._failing_machines = None
        self._message = None
        self._pending_machines = None
        self._ready_machines = None
        self._started_at = None
        self._stopped_at = None
        self.discriminator = None
        if deleting_machines is not None:
            self.deleting_machines = deleting_machines
        if failing_machines is not None:
            self.failing_machines = failing_machines
        if message is not None:
            self.message = message
        if pending_machines is not None:
            self.pending_machines = pending_machines
        if ready_machines is not None:
            self.ready_machines = ready_machines
        if started_at is not None:
            self.started_at = started_at
        if stopped_at is not None:
            self.stopped_at = stopped_at

    @property
    def deleting_machines(self) -> 'str':
        """Gets the deleting_machines of this V1MultiMachineJobStatus.  # noqa: E501


        :return: The deleting_machines of this V1MultiMachineJobStatus.  # noqa: E501
        :rtype: str
        """
        return self._deleting_machines

    @deleting_machines.setter
    def deleting_machines(self, deleting_machines: 'str'):
        """Sets the deleting_machines of this V1MultiMachineJobStatus.


        :param deleting_machines: The deleting_machines of this V1MultiMachineJobStatus.  # noqa: E501
        :type: str
        """

        self._deleting_machines = deleting_machines

    @property
    def failing_machines(self) -> 'str':
        """Gets the failing_machines of this V1MultiMachineJobStatus.  # noqa: E501


        :return: The failing_machines of this V1MultiMachineJobStatus.  # noqa: E501
        :rtype: str
        """
        return self._failing_machines

    @failing_machines.setter
    def failing_machines(self, failing_machines: 'str'):
        """Sets the failing_machines of this V1MultiMachineJobStatus.


        :param failing_machines: The failing_machines of this V1MultiMachineJobStatus.  # noqa: E501
        :type: str
        """

        self._failing_machines = failing_machines

    @property
    def message(self) -> 'str':
        """Gets the message of this V1MultiMachineJobStatus.  # noqa: E501


        :return: The message of this V1MultiMachineJobStatus.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message: 'str'):
        """Sets the message of this V1MultiMachineJobStatus.


        :param message: The message of this V1MultiMachineJobStatus.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def pending_machines(self) -> 'str':
        """Gets the pending_machines of this V1MultiMachineJobStatus.  # noqa: E501


        :return: The pending_machines of this V1MultiMachineJobStatus.  # noqa: E501
        :rtype: str
        """
        return self._pending_machines

    @pending_machines.setter
    def pending_machines(self, pending_machines: 'str'):
        """Sets the pending_machines of this V1MultiMachineJobStatus.


        :param pending_machines: The pending_machines of this V1MultiMachineJobStatus.  # noqa: E501
        :type: str
        """

        self._pending_machines = pending_machines

    @property
    def ready_machines(self) -> 'str':
        """Gets the ready_machines of this V1MultiMachineJobStatus.  # noqa: E501


        :return: The ready_machines of this V1MultiMachineJobStatus.  # noqa: E501
        :rtype: str
        """
        return self._ready_machines

    @ready_machines.setter
    def ready_machines(self, ready_machines: 'str'):
        """Sets the ready_machines of this V1MultiMachineJobStatus.


        :param ready_machines: The ready_machines of this V1MultiMachineJobStatus.  # noqa: E501
        :type: str
        """

        self._ready_machines = ready_machines

    @property
    def started_at(self) -> 'datetime':
        """Gets the started_at of this V1MultiMachineJobStatus.  # noqa: E501


        :return: The started_at of this V1MultiMachineJobStatus.  # noqa: E501
        :rtype: datetime
        """
        return self._started_at

    @started_at.setter
    def started_at(self, started_at: 'datetime'):
        """Sets the started_at of this V1MultiMachineJobStatus.


        :param started_at: The started_at of this V1MultiMachineJobStatus.  # noqa: E501
        :type: datetime
        """

        self._started_at = started_at

    @property
    def stopped_at(self) -> 'datetime':
        """Gets the stopped_at of this V1MultiMachineJobStatus.  # noqa: E501


        :return: The stopped_at of this V1MultiMachineJobStatus.  # noqa: E501
        :rtype: datetime
        """
        return self._stopped_at

    @stopped_at.setter
    def stopped_at(self, stopped_at: 'datetime'):
        """Sets the stopped_at of this V1MultiMachineJobStatus.


        :param stopped_at: The stopped_at of this V1MultiMachineJobStatus.  # noqa: E501
        :type: datetime
        """

        self._stopped_at = stopped_at

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
        if issubclass(V1MultiMachineJobStatus, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1MultiMachineJobStatus') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1MultiMachineJobStatus):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1MultiMachineJobStatus') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
