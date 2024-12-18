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

class V1ProjectMembershipInvite(object):
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
        'invite_reason': 'str',
        'invite_status': 'str',
        'invite_token': 'str',
        'invite_url': 'str',
        'project_id': 'str',
        'role_ids': 'list[str]',
        'user_email': 'str',
        'user_id': 'str'
    }

    attribute_map = {
        'invite_reason': 'inviteReason',
        'invite_status': 'inviteStatus',
        'invite_token': 'inviteToken',
        'invite_url': 'inviteUrl',
        'project_id': 'projectId',
        'role_ids': 'roleIds',
        'user_email': 'userEmail',
        'user_id': 'userId'
    }

    def __init__(self, invite_reason: 'str' =None, invite_status: 'str' =None, invite_token: 'str' =None, invite_url: 'str' =None, project_id: 'str' =None, role_ids: 'list[str]' =None, user_email: 'str' =None, user_id: 'str' =None):  # noqa: E501
        """V1ProjectMembershipInvite - a model defined in Swagger"""  # noqa: E501
        self._invite_reason = None
        self._invite_status = None
        self._invite_token = None
        self._invite_url = None
        self._project_id = None
        self._role_ids = None
        self._user_email = None
        self._user_id = None
        self.discriminator = None
        if invite_reason is not None:
            self.invite_reason = invite_reason
        if invite_status is not None:
            self.invite_status = invite_status
        if invite_token is not None:
            self.invite_token = invite_token
        if invite_url is not None:
            self.invite_url = invite_url
        if project_id is not None:
            self.project_id = project_id
        if role_ids is not None:
            self.role_ids = role_ids
        if user_email is not None:
            self.user_email = user_email
        if user_id is not None:
            self.user_id = user_id

    @property
    def invite_reason(self) -> 'str':
        """Gets the invite_reason of this V1ProjectMembershipInvite.  # noqa: E501


        :return: The invite_reason of this V1ProjectMembershipInvite.  # noqa: E501
        :rtype: str
        """
        return self._invite_reason

    @invite_reason.setter
    def invite_reason(self, invite_reason: 'str'):
        """Sets the invite_reason of this V1ProjectMembershipInvite.


        :param invite_reason: The invite_reason of this V1ProjectMembershipInvite.  # noqa: E501
        :type: str
        """

        self._invite_reason = invite_reason

    @property
    def invite_status(self) -> 'str':
        """Gets the invite_status of this V1ProjectMembershipInvite.  # noqa: E501


        :return: The invite_status of this V1ProjectMembershipInvite.  # noqa: E501
        :rtype: str
        """
        return self._invite_status

    @invite_status.setter
    def invite_status(self, invite_status: 'str'):
        """Sets the invite_status of this V1ProjectMembershipInvite.


        :param invite_status: The invite_status of this V1ProjectMembershipInvite.  # noqa: E501
        :type: str
        """

        self._invite_status = invite_status

    @property
    def invite_token(self) -> 'str':
        """Gets the invite_token of this V1ProjectMembershipInvite.  # noqa: E501


        :return: The invite_token of this V1ProjectMembershipInvite.  # noqa: E501
        :rtype: str
        """
        return self._invite_token

    @invite_token.setter
    def invite_token(self, invite_token: 'str'):
        """Sets the invite_token of this V1ProjectMembershipInvite.


        :param invite_token: The invite_token of this V1ProjectMembershipInvite.  # noqa: E501
        :type: str
        """

        self._invite_token = invite_token

    @property
    def invite_url(self) -> 'str':
        """Gets the invite_url of this V1ProjectMembershipInvite.  # noqa: E501


        :return: The invite_url of this V1ProjectMembershipInvite.  # noqa: E501
        :rtype: str
        """
        return self._invite_url

    @invite_url.setter
    def invite_url(self, invite_url: 'str'):
        """Sets the invite_url of this V1ProjectMembershipInvite.


        :param invite_url: The invite_url of this V1ProjectMembershipInvite.  # noqa: E501
        :type: str
        """

        self._invite_url = invite_url

    @property
    def project_id(self) -> 'str':
        """Gets the project_id of this V1ProjectMembershipInvite.  # noqa: E501


        :return: The project_id of this V1ProjectMembershipInvite.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id: 'str'):
        """Sets the project_id of this V1ProjectMembershipInvite.


        :param project_id: The project_id of this V1ProjectMembershipInvite.  # noqa: E501
        :type: str
        """

        self._project_id = project_id

    @property
    def role_ids(self) -> 'list[str]':
        """Gets the role_ids of this V1ProjectMembershipInvite.  # noqa: E501


        :return: The role_ids of this V1ProjectMembershipInvite.  # noqa: E501
        :rtype: list[str]
        """
        return self._role_ids

    @role_ids.setter
    def role_ids(self, role_ids: 'list[str]'):
        """Sets the role_ids of this V1ProjectMembershipInvite.


        :param role_ids: The role_ids of this V1ProjectMembershipInvite.  # noqa: E501
        :type: list[str]
        """

        self._role_ids = role_ids

    @property
    def user_email(self) -> 'str':
        """Gets the user_email of this V1ProjectMembershipInvite.  # noqa: E501


        :return: The user_email of this V1ProjectMembershipInvite.  # noqa: E501
        :rtype: str
        """
        return self._user_email

    @user_email.setter
    def user_email(self, user_email: 'str'):
        """Sets the user_email of this V1ProjectMembershipInvite.


        :param user_email: The user_email of this V1ProjectMembershipInvite.  # noqa: E501
        :type: str
        """

        self._user_email = user_email

    @property
    def user_id(self) -> 'str':
        """Gets the user_id of this V1ProjectMembershipInvite.  # noqa: E501


        :return: The user_id of this V1ProjectMembershipInvite.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: 'str'):
        """Sets the user_id of this V1ProjectMembershipInvite.


        :param user_id: The user_id of this V1ProjectMembershipInvite.  # noqa: E501
        :type: str
        """

        self._user_id = user_id

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
        if issubclass(V1ProjectMembershipInvite, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1ProjectMembershipInvite') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1ProjectMembershipInvite):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1ProjectMembershipInvite') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
