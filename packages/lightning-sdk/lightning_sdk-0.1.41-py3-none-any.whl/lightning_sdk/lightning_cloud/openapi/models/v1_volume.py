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

class V1Volume(object):
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
        'ebs': 'V1Ebs',
        'id': 'str',
        'spec_id': 'str'
    }

    attribute_map = {
        'ebs': 'ebs',
        'id': 'id',
        'spec_id': 'specId'
    }

    def __init__(self, ebs: 'V1Ebs' =None, id: 'str' =None, spec_id: 'str' =None):  # noqa: E501
        """V1Volume - a model defined in Swagger"""  # noqa: E501
        self._ebs = None
        self._id = None
        self._spec_id = None
        self.discriminator = None
        if ebs is not None:
            self.ebs = ebs
        if id is not None:
            self.id = id
        if spec_id is not None:
            self.spec_id = spec_id

    @property
    def ebs(self) -> 'V1Ebs':
        """Gets the ebs of this V1Volume.  # noqa: E501


        :return: The ebs of this V1Volume.  # noqa: E501
        :rtype: V1Ebs
        """
        return self._ebs

    @ebs.setter
    def ebs(self, ebs: 'V1Ebs'):
        """Sets the ebs of this V1Volume.


        :param ebs: The ebs of this V1Volume.  # noqa: E501
        :type: V1Ebs
        """

        self._ebs = ebs

    @property
    def id(self) -> 'str':
        """Gets the id of this V1Volume.  # noqa: E501


        :return: The id of this V1Volume.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: 'str'):
        """Sets the id of this V1Volume.


        :param id: The id of this V1Volume.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def spec_id(self) -> 'str':
        """Gets the spec_id of this V1Volume.  # noqa: E501


        :return: The spec_id of this V1Volume.  # noqa: E501
        :rtype: str
        """
        return self._spec_id

    @spec_id.setter
    def spec_id(self, spec_id: 'str'):
        """Sets the spec_id of this V1Volume.


        :param spec_id: The spec_id of this V1Volume.  # noqa: E501
        :type: str
        """

        self._spec_id = spec_id

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
        if issubclass(V1Volume, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1Volume') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1Volume):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1Volume') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
