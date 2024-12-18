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

class VersionsIdBody(object):
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
        'about_page_content': 'str',
        'code_url': 'str',
        'description': 'str',
        'hide_files': 'bool',
        'license': 'str',
        'operating_cost': 'str',
        'paper_authors': 'str',
        'paper_org': 'str',
        'paper_org_avatar_url': 'str',
        'paper_url': 'str'
    }

    attribute_map = {
        'about_page_content': 'aboutPageContent',
        'code_url': 'codeUrl',
        'description': 'description',
        'hide_files': 'hideFiles',
        'license': 'license',
        'operating_cost': 'operatingCost',
        'paper_authors': 'paperAuthors',
        'paper_org': 'paperOrg',
        'paper_org_avatar_url': 'paperOrgAvatarUrl',
        'paper_url': 'paperUrl'
    }

    def __init__(self, about_page_content: 'str' =None, code_url: 'str' =None, description: 'str' =None, hide_files: 'bool' =None, license: 'str' =None, operating_cost: 'str' =None, paper_authors: 'str' =None, paper_org: 'str' =None, paper_org_avatar_url: 'str' =None, paper_url: 'str' =None):  # noqa: E501
        """VersionsIdBody - a model defined in Swagger"""  # noqa: E501
        self._about_page_content = None
        self._code_url = None
        self._description = None
        self._hide_files = None
        self._license = None
        self._operating_cost = None
        self._paper_authors = None
        self._paper_org = None
        self._paper_org_avatar_url = None
        self._paper_url = None
        self.discriminator = None
        if about_page_content is not None:
            self.about_page_content = about_page_content
        if code_url is not None:
            self.code_url = code_url
        if description is not None:
            self.description = description
        if hide_files is not None:
            self.hide_files = hide_files
        if license is not None:
            self.license = license
        if operating_cost is not None:
            self.operating_cost = operating_cost
        if paper_authors is not None:
            self.paper_authors = paper_authors
        if paper_org is not None:
            self.paper_org = paper_org
        if paper_org_avatar_url is not None:
            self.paper_org_avatar_url = paper_org_avatar_url
        if paper_url is not None:
            self.paper_url = paper_url

    @property
    def about_page_content(self) -> 'str':
        """Gets the about_page_content of this VersionsIdBody.  # noqa: E501


        :return: The about_page_content of this VersionsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._about_page_content

    @about_page_content.setter
    def about_page_content(self, about_page_content: 'str'):
        """Sets the about_page_content of this VersionsIdBody.


        :param about_page_content: The about_page_content of this VersionsIdBody.  # noqa: E501
        :type: str
        """

        self._about_page_content = about_page_content

    @property
    def code_url(self) -> 'str':
        """Gets the code_url of this VersionsIdBody.  # noqa: E501


        :return: The code_url of this VersionsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._code_url

    @code_url.setter
    def code_url(self, code_url: 'str'):
        """Sets the code_url of this VersionsIdBody.


        :param code_url: The code_url of this VersionsIdBody.  # noqa: E501
        :type: str
        """

        self._code_url = code_url

    @property
    def description(self) -> 'str':
        """Gets the description of this VersionsIdBody.  # noqa: E501


        :return: The description of this VersionsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: 'str'):
        """Sets the description of this VersionsIdBody.


        :param description: The description of this VersionsIdBody.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def hide_files(self) -> 'bool':
        """Gets the hide_files of this VersionsIdBody.  # noqa: E501


        :return: The hide_files of this VersionsIdBody.  # noqa: E501
        :rtype: bool
        """
        return self._hide_files

    @hide_files.setter
    def hide_files(self, hide_files: 'bool'):
        """Sets the hide_files of this VersionsIdBody.


        :param hide_files: The hide_files of this VersionsIdBody.  # noqa: E501
        :type: bool
        """

        self._hide_files = hide_files

    @property
    def license(self) -> 'str':
        """Gets the license of this VersionsIdBody.  # noqa: E501


        :return: The license of this VersionsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._license

    @license.setter
    def license(self, license: 'str'):
        """Sets the license of this VersionsIdBody.


        :param license: The license of this VersionsIdBody.  # noqa: E501
        :type: str
        """

        self._license = license

    @property
    def operating_cost(self) -> 'str':
        """Gets the operating_cost of this VersionsIdBody.  # noqa: E501


        :return: The operating_cost of this VersionsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._operating_cost

    @operating_cost.setter
    def operating_cost(self, operating_cost: 'str'):
        """Sets the operating_cost of this VersionsIdBody.


        :param operating_cost: The operating_cost of this VersionsIdBody.  # noqa: E501
        :type: str
        """

        self._operating_cost = operating_cost

    @property
    def paper_authors(self) -> 'str':
        """Gets the paper_authors of this VersionsIdBody.  # noqa: E501


        :return: The paper_authors of this VersionsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._paper_authors

    @paper_authors.setter
    def paper_authors(self, paper_authors: 'str'):
        """Sets the paper_authors of this VersionsIdBody.


        :param paper_authors: The paper_authors of this VersionsIdBody.  # noqa: E501
        :type: str
        """

        self._paper_authors = paper_authors

    @property
    def paper_org(self) -> 'str':
        """Gets the paper_org of this VersionsIdBody.  # noqa: E501


        :return: The paper_org of this VersionsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._paper_org

    @paper_org.setter
    def paper_org(self, paper_org: 'str'):
        """Sets the paper_org of this VersionsIdBody.


        :param paper_org: The paper_org of this VersionsIdBody.  # noqa: E501
        :type: str
        """

        self._paper_org = paper_org

    @property
    def paper_org_avatar_url(self) -> 'str':
        """Gets the paper_org_avatar_url of this VersionsIdBody.  # noqa: E501


        :return: The paper_org_avatar_url of this VersionsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._paper_org_avatar_url

    @paper_org_avatar_url.setter
    def paper_org_avatar_url(self, paper_org_avatar_url: 'str'):
        """Sets the paper_org_avatar_url of this VersionsIdBody.


        :param paper_org_avatar_url: The paper_org_avatar_url of this VersionsIdBody.  # noqa: E501
        :type: str
        """

        self._paper_org_avatar_url = paper_org_avatar_url

    @property
    def paper_url(self) -> 'str':
        """Gets the paper_url of this VersionsIdBody.  # noqa: E501


        :return: The paper_url of this VersionsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._paper_url

    @paper_url.setter
    def paper_url(self, paper_url: 'str'):
        """Sets the paper_url of this VersionsIdBody.


        :param paper_url: The paper_url of this VersionsIdBody.  # noqa: E501
        :type: str
        """

        self._paper_url = paper_url

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
        if issubclass(VersionsIdBody, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'VersionsIdBody') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, VersionsIdBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'VersionsIdBody') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
