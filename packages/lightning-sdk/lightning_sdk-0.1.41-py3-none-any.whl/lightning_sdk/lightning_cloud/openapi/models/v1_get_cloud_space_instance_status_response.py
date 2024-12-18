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

class V1GetCloudSpaceInstanceStatusResponse(object):
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
        'collab_session': 'V1CollabSession',
        'collab_status': 'V1CloudSpaceInstanceCollabStatus',
        'in_use': 'Externalv1CloudSpaceInstanceStatus',
        'requested': 'Externalv1CloudSpaceInstanceStatus'
    }

    attribute_map = {
        'collab_session': 'collabSession',
        'collab_status': 'collabStatus',
        'in_use': 'inUse',
        'requested': 'requested'
    }

    def __init__(self, collab_session: 'V1CollabSession' =None, collab_status: 'V1CloudSpaceInstanceCollabStatus' =None, in_use: 'Externalv1CloudSpaceInstanceStatus' =None, requested: 'Externalv1CloudSpaceInstanceStatus' =None):  # noqa: E501
        """V1GetCloudSpaceInstanceStatusResponse - a model defined in Swagger"""  # noqa: E501
        self._collab_session = None
        self._collab_status = None
        self._in_use = None
        self._requested = None
        self.discriminator = None
        if collab_session is not None:
            self.collab_session = collab_session
        if collab_status is not None:
            self.collab_status = collab_status
        if in_use is not None:
            self.in_use = in_use
        if requested is not None:
            self.requested = requested

    @property
    def collab_session(self) -> 'V1CollabSession':
        """Gets the collab_session of this V1GetCloudSpaceInstanceStatusResponse.  # noqa: E501


        :return: The collab_session of this V1GetCloudSpaceInstanceStatusResponse.  # noqa: E501
        :rtype: V1CollabSession
        """
        return self._collab_session

    @collab_session.setter
    def collab_session(self, collab_session: 'V1CollabSession'):
        """Sets the collab_session of this V1GetCloudSpaceInstanceStatusResponse.


        :param collab_session: The collab_session of this V1GetCloudSpaceInstanceStatusResponse.  # noqa: E501
        :type: V1CollabSession
        """

        self._collab_session = collab_session

    @property
    def collab_status(self) -> 'V1CloudSpaceInstanceCollabStatus':
        """Gets the collab_status of this V1GetCloudSpaceInstanceStatusResponse.  # noqa: E501


        :return: The collab_status of this V1GetCloudSpaceInstanceStatusResponse.  # noqa: E501
        :rtype: V1CloudSpaceInstanceCollabStatus
        """
        return self._collab_status

    @collab_status.setter
    def collab_status(self, collab_status: 'V1CloudSpaceInstanceCollabStatus'):
        """Sets the collab_status of this V1GetCloudSpaceInstanceStatusResponse.


        :param collab_status: The collab_status of this V1GetCloudSpaceInstanceStatusResponse.  # noqa: E501
        :type: V1CloudSpaceInstanceCollabStatus
        """

        self._collab_status = collab_status

    @property
    def in_use(self) -> 'Externalv1CloudSpaceInstanceStatus':
        """Gets the in_use of this V1GetCloudSpaceInstanceStatusResponse.  # noqa: E501


        :return: The in_use of this V1GetCloudSpaceInstanceStatusResponse.  # noqa: E501
        :rtype: Externalv1CloudSpaceInstanceStatus
        """
        return self._in_use

    @in_use.setter
    def in_use(self, in_use: 'Externalv1CloudSpaceInstanceStatus'):
        """Sets the in_use of this V1GetCloudSpaceInstanceStatusResponse.


        :param in_use: The in_use of this V1GetCloudSpaceInstanceStatusResponse.  # noqa: E501
        :type: Externalv1CloudSpaceInstanceStatus
        """

        self._in_use = in_use

    @property
    def requested(self) -> 'Externalv1CloudSpaceInstanceStatus':
        """Gets the requested of this V1GetCloudSpaceInstanceStatusResponse.  # noqa: E501


        :return: The requested of this V1GetCloudSpaceInstanceStatusResponse.  # noqa: E501
        :rtype: Externalv1CloudSpaceInstanceStatus
        """
        return self._requested

    @requested.setter
    def requested(self, requested: 'Externalv1CloudSpaceInstanceStatus'):
        """Sets the requested of this V1GetCloudSpaceInstanceStatusResponse.


        :param requested: The requested of this V1GetCloudSpaceInstanceStatusResponse.  # noqa: E501
        :type: Externalv1CloudSpaceInstanceStatus
        """

        self._requested = requested

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
        if issubclass(V1GetCloudSpaceInstanceStatusResponse, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1GetCloudSpaceInstanceStatusResponse') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1GetCloudSpaceInstanceStatusResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1GetCloudSpaceInstanceStatusResponse') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
