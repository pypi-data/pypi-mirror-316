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

class V1DeploymentSpec(object):
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
        'apis': 'list[V1DeploymentAPI]',
        'autoscaling': 'V1AutoscalingSpec',
        'endpoint': 'V1Endpoint',
        'job': 'V1JobSpec'
    }

    attribute_map = {
        'apis': 'apis',
        'autoscaling': 'autoscaling',
        'endpoint': 'endpoint',
        'job': 'job'
    }

    def __init__(self, apis: 'list[V1DeploymentAPI]' =None, autoscaling: 'V1AutoscalingSpec' =None, endpoint: 'V1Endpoint' =None, job: 'V1JobSpec' =None):  # noqa: E501
        """V1DeploymentSpec - a model defined in Swagger"""  # noqa: E501
        self._apis = None
        self._autoscaling = None
        self._endpoint = None
        self._job = None
        self.discriminator = None
        if apis is not None:
            self.apis = apis
        if autoscaling is not None:
            self.autoscaling = autoscaling
        if endpoint is not None:
            self.endpoint = endpoint
        if job is not None:
            self.job = job

    @property
    def apis(self) -> 'list[V1DeploymentAPI]':
        """Gets the apis of this V1DeploymentSpec.  # noqa: E501


        :return: The apis of this V1DeploymentSpec.  # noqa: E501
        :rtype: list[V1DeploymentAPI]
        """
        return self._apis

    @apis.setter
    def apis(self, apis: 'list[V1DeploymentAPI]'):
        """Sets the apis of this V1DeploymentSpec.


        :param apis: The apis of this V1DeploymentSpec.  # noqa: E501
        :type: list[V1DeploymentAPI]
        """

        self._apis = apis

    @property
    def autoscaling(self) -> 'V1AutoscalingSpec':
        """Gets the autoscaling of this V1DeploymentSpec.  # noqa: E501


        :return: The autoscaling of this V1DeploymentSpec.  # noqa: E501
        :rtype: V1AutoscalingSpec
        """
        return self._autoscaling

    @autoscaling.setter
    def autoscaling(self, autoscaling: 'V1AutoscalingSpec'):
        """Sets the autoscaling of this V1DeploymentSpec.


        :param autoscaling: The autoscaling of this V1DeploymentSpec.  # noqa: E501
        :type: V1AutoscalingSpec
        """

        self._autoscaling = autoscaling

    @property
    def endpoint(self) -> 'V1Endpoint':
        """Gets the endpoint of this V1DeploymentSpec.  # noqa: E501


        :return: The endpoint of this V1DeploymentSpec.  # noqa: E501
        :rtype: V1Endpoint
        """
        return self._endpoint

    @endpoint.setter
    def endpoint(self, endpoint: 'V1Endpoint'):
        """Sets the endpoint of this V1DeploymentSpec.


        :param endpoint: The endpoint of this V1DeploymentSpec.  # noqa: E501
        :type: V1Endpoint
        """

        self._endpoint = endpoint

    @property
    def job(self) -> 'V1JobSpec':
        """Gets the job of this V1DeploymentSpec.  # noqa: E501


        :return: The job of this V1DeploymentSpec.  # noqa: E501
        :rtype: V1JobSpec
        """
        return self._job

    @job.setter
    def job(self, job: 'V1JobSpec'):
        """Sets the job of this V1DeploymentSpec.


        :param job: The job of this V1DeploymentSpec.  # noqa: E501
        :type: V1JobSpec
        """

        self._job = job

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
        if issubclass(V1DeploymentSpec, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1DeploymentSpec') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1DeploymentSpec):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1DeploymentSpec') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
