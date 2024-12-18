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

class V1ProjectComputeDailyUsage(object):
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
        '_date': 'datetime',
        'total_cost_experiments': 'float',
        'total_cost_sessions': 'float',
        'usage': 'list[V1ProjectComputeUsage]'
    }

    attribute_map = {
        '_date': 'date',
        'total_cost_experiments': 'totalCostExperiments',
        'total_cost_sessions': 'totalCostSessions',
        'usage': 'usage'
    }

    def __init__(self, _date: 'datetime' =None, total_cost_experiments: 'float' =None, total_cost_sessions: 'float' =None, usage: 'list[V1ProjectComputeUsage]' =None):  # noqa: E501
        """V1ProjectComputeDailyUsage - a model defined in Swagger"""  # noqa: E501
        self.__date = None
        self._total_cost_experiments = None
        self._total_cost_sessions = None
        self._usage = None
        self.discriminator = None
        if _date is not None:
            self._date = _date
        if total_cost_experiments is not None:
            self.total_cost_experiments = total_cost_experiments
        if total_cost_sessions is not None:
            self.total_cost_sessions = total_cost_sessions
        if usage is not None:
            self.usage = usage

    @property
    def _date(self) -> 'datetime':
        """Gets the _date of this V1ProjectComputeDailyUsage.  # noqa: E501


        :return: The _date of this V1ProjectComputeDailyUsage.  # noqa: E501
        :rtype: datetime
        """
        return self.__date

    @_date.setter
    def _date(self, _date: 'datetime'):
        """Sets the _date of this V1ProjectComputeDailyUsage.


        :param _date: The _date of this V1ProjectComputeDailyUsage.  # noqa: E501
        :type: datetime
        """

        self.__date = _date

    @property
    def total_cost_experiments(self) -> 'float':
        """Gets the total_cost_experiments of this V1ProjectComputeDailyUsage.  # noqa: E501


        :return: The total_cost_experiments of this V1ProjectComputeDailyUsage.  # noqa: E501
        :rtype: float
        """
        return self._total_cost_experiments

    @total_cost_experiments.setter
    def total_cost_experiments(self, total_cost_experiments: 'float'):
        """Sets the total_cost_experiments of this V1ProjectComputeDailyUsage.


        :param total_cost_experiments: The total_cost_experiments of this V1ProjectComputeDailyUsage.  # noqa: E501
        :type: float
        """

        self._total_cost_experiments = total_cost_experiments

    @property
    def total_cost_sessions(self) -> 'float':
        """Gets the total_cost_sessions of this V1ProjectComputeDailyUsage.  # noqa: E501


        :return: The total_cost_sessions of this V1ProjectComputeDailyUsage.  # noqa: E501
        :rtype: float
        """
        return self._total_cost_sessions

    @total_cost_sessions.setter
    def total_cost_sessions(self, total_cost_sessions: 'float'):
        """Sets the total_cost_sessions of this V1ProjectComputeDailyUsage.


        :param total_cost_sessions: The total_cost_sessions of this V1ProjectComputeDailyUsage.  # noqa: E501
        :type: float
        """

        self._total_cost_sessions = total_cost_sessions

    @property
    def usage(self) -> 'list[V1ProjectComputeUsage]':
        """Gets the usage of this V1ProjectComputeDailyUsage.  # noqa: E501


        :return: The usage of this V1ProjectComputeDailyUsage.  # noqa: E501
        :rtype: list[V1ProjectComputeUsage]
        """
        return self._usage

    @usage.setter
    def usage(self, usage: 'list[V1ProjectComputeUsage]'):
        """Sets the usage of this V1ProjectComputeDailyUsage.


        :param usage: The usage of this V1ProjectComputeDailyUsage.  # noqa: E501
        :type: list[V1ProjectComputeUsage]
        """

        self._usage = usage

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
        if issubclass(V1ProjectComputeDailyUsage, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1ProjectComputeDailyUsage') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1ProjectComputeDailyUsage):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1ProjectComputeDailyUsage') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
