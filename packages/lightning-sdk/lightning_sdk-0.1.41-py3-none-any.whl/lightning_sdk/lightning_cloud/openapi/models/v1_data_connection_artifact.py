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

class V1DataConnectionArtifact(object):
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
        'filename': 'str',
        'last_modified': 'datetime',
        'md5_checksum': 'str',
        'size_bytes': 'str',
        'url': 'str'
    }

    attribute_map = {
        'filename': 'filename',
        'last_modified': 'lastModified',
        'md5_checksum': 'md5Checksum',
        'size_bytes': 'sizeBytes',
        'url': 'url'
    }

    def __init__(self, filename: 'str' =None, last_modified: 'datetime' =None, md5_checksum: 'str' =None, size_bytes: 'str' =None, url: 'str' =None):  # noqa: E501
        """V1DataConnectionArtifact - a model defined in Swagger"""  # noqa: E501
        self._filename = None
        self._last_modified = None
        self._md5_checksum = None
        self._size_bytes = None
        self._url = None
        self.discriminator = None
        if filename is not None:
            self.filename = filename
        if last_modified is not None:
            self.last_modified = last_modified
        if md5_checksum is not None:
            self.md5_checksum = md5_checksum
        if size_bytes is not None:
            self.size_bytes = size_bytes
        if url is not None:
            self.url = url

    @property
    def filename(self) -> 'str':
        """Gets the filename of this V1DataConnectionArtifact.  # noqa: E501


        :return: The filename of this V1DataConnectionArtifact.  # noqa: E501
        :rtype: str
        """
        return self._filename

    @filename.setter
    def filename(self, filename: 'str'):
        """Sets the filename of this V1DataConnectionArtifact.


        :param filename: The filename of this V1DataConnectionArtifact.  # noqa: E501
        :type: str
        """

        self._filename = filename

    @property
    def last_modified(self) -> 'datetime':
        """Gets the last_modified of this V1DataConnectionArtifact.  # noqa: E501


        :return: The last_modified of this V1DataConnectionArtifact.  # noqa: E501
        :rtype: datetime
        """
        return self._last_modified

    @last_modified.setter
    def last_modified(self, last_modified: 'datetime'):
        """Sets the last_modified of this V1DataConnectionArtifact.


        :param last_modified: The last_modified of this V1DataConnectionArtifact.  # noqa: E501
        :type: datetime
        """

        self._last_modified = last_modified

    @property
    def md5_checksum(self) -> 'str':
        """Gets the md5_checksum of this V1DataConnectionArtifact.  # noqa: E501


        :return: The md5_checksum of this V1DataConnectionArtifact.  # noqa: E501
        :rtype: str
        """
        return self._md5_checksum

    @md5_checksum.setter
    def md5_checksum(self, md5_checksum: 'str'):
        """Sets the md5_checksum of this V1DataConnectionArtifact.


        :param md5_checksum: The md5_checksum of this V1DataConnectionArtifact.  # noqa: E501
        :type: str
        """

        self._md5_checksum = md5_checksum

    @property
    def size_bytes(self) -> 'str':
        """Gets the size_bytes of this V1DataConnectionArtifact.  # noqa: E501


        :return: The size_bytes of this V1DataConnectionArtifact.  # noqa: E501
        :rtype: str
        """
        return self._size_bytes

    @size_bytes.setter
    def size_bytes(self, size_bytes: 'str'):
        """Sets the size_bytes of this V1DataConnectionArtifact.


        :param size_bytes: The size_bytes of this V1DataConnectionArtifact.  # noqa: E501
        :type: str
        """

        self._size_bytes = size_bytes

    @property
    def url(self) -> 'str':
        """Gets the url of this V1DataConnectionArtifact.  # noqa: E501


        :return: The url of this V1DataConnectionArtifact.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url: 'str'):
        """Sets the url of this V1DataConnectionArtifact.


        :param url: The url of this V1DataConnectionArtifact.  # noqa: E501
        :type: str
        """

        self._url = url

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
        if issubclass(V1DataConnectionArtifact, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1DataConnectionArtifact') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1DataConnectionArtifact):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1DataConnectionArtifact') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
