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

class DeploymenttemplatesIdBody(object):
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
        'categories': 'list[str]',
        'description': 'str',
        'featured': 'bool',
        'image_url': 'str',
        'metrics': 'V1DeploymentMetrics',
        'name': 'str',
        'org_id': 'str',
        'parameter_spec': 'V1ParameterizationSpec',
        'pricing': 'V1ApiPricingSpec',
        'spec': 'str',
        'tags': 'list[V1ResourceTag]',
        'thumbnail': 'str',
        'thumbnail_file_type': 'str',
        'visibility': 'V1DeploymentTemplateType'
    }

    attribute_map = {
        'about_page_content': 'aboutPageContent',
        'categories': 'categories',
        'description': 'description',
        'featured': 'featured',
        'image_url': 'imageUrl',
        'metrics': 'metrics',
        'name': 'name',
        'org_id': 'orgId',
        'parameter_spec': 'parameterSpec',
        'pricing': 'pricing',
        'spec': 'spec',
        'tags': 'tags',
        'thumbnail': 'thumbnail',
        'thumbnail_file_type': 'thumbnailFileType',
        'visibility': 'visibility'
    }

    def __init__(self, about_page_content: 'str' =None, categories: 'list[str]' =None, description: 'str' =None, featured: 'bool' =None, image_url: 'str' =None, metrics: 'V1DeploymentMetrics' =None, name: 'str' =None, org_id: 'str' =None, parameter_spec: 'V1ParameterizationSpec' =None, pricing: 'V1ApiPricingSpec' =None, spec: 'str' =None, tags: 'list[V1ResourceTag]' =None, thumbnail: 'str' =None, thumbnail_file_type: 'str' =None, visibility: 'V1DeploymentTemplateType' =None):  # noqa: E501
        """DeploymenttemplatesIdBody - a model defined in Swagger"""  # noqa: E501
        self._about_page_content = None
        self._categories = None
        self._description = None
        self._featured = None
        self._image_url = None
        self._metrics = None
        self._name = None
        self._org_id = None
        self._parameter_spec = None
        self._pricing = None
        self._spec = None
        self._tags = None
        self._thumbnail = None
        self._thumbnail_file_type = None
        self._visibility = None
        self.discriminator = None
        if about_page_content is not None:
            self.about_page_content = about_page_content
        if categories is not None:
            self.categories = categories
        if description is not None:
            self.description = description
        if featured is not None:
            self.featured = featured
        if image_url is not None:
            self.image_url = image_url
        if metrics is not None:
            self.metrics = metrics
        if name is not None:
            self.name = name
        if org_id is not None:
            self.org_id = org_id
        if parameter_spec is not None:
            self.parameter_spec = parameter_spec
        if pricing is not None:
            self.pricing = pricing
        if spec is not None:
            self.spec = spec
        if tags is not None:
            self.tags = tags
        if thumbnail is not None:
            self.thumbnail = thumbnail
        if thumbnail_file_type is not None:
            self.thumbnail_file_type = thumbnail_file_type
        if visibility is not None:
            self.visibility = visibility

    @property
    def about_page_content(self) -> 'str':
        """Gets the about_page_content of this DeploymenttemplatesIdBody.  # noqa: E501


        :return: The about_page_content of this DeploymenttemplatesIdBody.  # noqa: E501
        :rtype: str
        """
        return self._about_page_content

    @about_page_content.setter
    def about_page_content(self, about_page_content: 'str'):
        """Sets the about_page_content of this DeploymenttemplatesIdBody.


        :param about_page_content: The about_page_content of this DeploymenttemplatesIdBody.  # noqa: E501
        :type: str
        """

        self._about_page_content = about_page_content

    @property
    def categories(self) -> 'list[str]':
        """Gets the categories of this DeploymenttemplatesIdBody.  # noqa: E501


        :return: The categories of this DeploymenttemplatesIdBody.  # noqa: E501
        :rtype: list[str]
        """
        return self._categories

    @categories.setter
    def categories(self, categories: 'list[str]'):
        """Sets the categories of this DeploymenttemplatesIdBody.


        :param categories: The categories of this DeploymenttemplatesIdBody.  # noqa: E501
        :type: list[str]
        """

        self._categories = categories

    @property
    def description(self) -> 'str':
        """Gets the description of this DeploymenttemplatesIdBody.  # noqa: E501


        :return: The description of this DeploymenttemplatesIdBody.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: 'str'):
        """Sets the description of this DeploymenttemplatesIdBody.


        :param description: The description of this DeploymenttemplatesIdBody.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def featured(self) -> 'bool':
        """Gets the featured of this DeploymenttemplatesIdBody.  # noqa: E501


        :return: The featured of this DeploymenttemplatesIdBody.  # noqa: E501
        :rtype: bool
        """
        return self._featured

    @featured.setter
    def featured(self, featured: 'bool'):
        """Sets the featured of this DeploymenttemplatesIdBody.


        :param featured: The featured of this DeploymenttemplatesIdBody.  # noqa: E501
        :type: bool
        """

        self._featured = featured

    @property
    def image_url(self) -> 'str':
        """Gets the image_url of this DeploymenttemplatesIdBody.  # noqa: E501


        :return: The image_url of this DeploymenttemplatesIdBody.  # noqa: E501
        :rtype: str
        """
        return self._image_url

    @image_url.setter
    def image_url(self, image_url: 'str'):
        """Sets the image_url of this DeploymenttemplatesIdBody.


        :param image_url: The image_url of this DeploymenttemplatesIdBody.  # noqa: E501
        :type: str
        """

        self._image_url = image_url

    @property
    def metrics(self) -> 'V1DeploymentMetrics':
        """Gets the metrics of this DeploymenttemplatesIdBody.  # noqa: E501


        :return: The metrics of this DeploymenttemplatesIdBody.  # noqa: E501
        :rtype: V1DeploymentMetrics
        """
        return self._metrics

    @metrics.setter
    def metrics(self, metrics: 'V1DeploymentMetrics'):
        """Sets the metrics of this DeploymenttemplatesIdBody.


        :param metrics: The metrics of this DeploymenttemplatesIdBody.  # noqa: E501
        :type: V1DeploymentMetrics
        """

        self._metrics = metrics

    @property
    def name(self) -> 'str':
        """Gets the name of this DeploymenttemplatesIdBody.  # noqa: E501


        :return: The name of this DeploymenttemplatesIdBody.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: 'str'):
        """Sets the name of this DeploymenttemplatesIdBody.


        :param name: The name of this DeploymenttemplatesIdBody.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def org_id(self) -> 'str':
        """Gets the org_id of this DeploymenttemplatesIdBody.  # noqa: E501


        :return: The org_id of this DeploymenttemplatesIdBody.  # noqa: E501
        :rtype: str
        """
        return self._org_id

    @org_id.setter
    def org_id(self, org_id: 'str'):
        """Sets the org_id of this DeploymenttemplatesIdBody.


        :param org_id: The org_id of this DeploymenttemplatesIdBody.  # noqa: E501
        :type: str
        """

        self._org_id = org_id

    @property
    def parameter_spec(self) -> 'V1ParameterizationSpec':
        """Gets the parameter_spec of this DeploymenttemplatesIdBody.  # noqa: E501


        :return: The parameter_spec of this DeploymenttemplatesIdBody.  # noqa: E501
        :rtype: V1ParameterizationSpec
        """
        return self._parameter_spec

    @parameter_spec.setter
    def parameter_spec(self, parameter_spec: 'V1ParameterizationSpec'):
        """Sets the parameter_spec of this DeploymenttemplatesIdBody.


        :param parameter_spec: The parameter_spec of this DeploymenttemplatesIdBody.  # noqa: E501
        :type: V1ParameterizationSpec
        """

        self._parameter_spec = parameter_spec

    @property
    def pricing(self) -> 'V1ApiPricingSpec':
        """Gets the pricing of this DeploymenttemplatesIdBody.  # noqa: E501


        :return: The pricing of this DeploymenttemplatesIdBody.  # noqa: E501
        :rtype: V1ApiPricingSpec
        """
        return self._pricing

    @pricing.setter
    def pricing(self, pricing: 'V1ApiPricingSpec'):
        """Sets the pricing of this DeploymenttemplatesIdBody.


        :param pricing: The pricing of this DeploymenttemplatesIdBody.  # noqa: E501
        :type: V1ApiPricingSpec
        """

        self._pricing = pricing

    @property
    def spec(self) -> 'str':
        """Gets the spec of this DeploymenttemplatesIdBody.  # noqa: E501


        :return: The spec of this DeploymenttemplatesIdBody.  # noqa: E501
        :rtype: str
        """
        return self._spec

    @spec.setter
    def spec(self, spec: 'str'):
        """Sets the spec of this DeploymenttemplatesIdBody.


        :param spec: The spec of this DeploymenttemplatesIdBody.  # noqa: E501
        :type: str
        """

        self._spec = spec

    @property
    def tags(self) -> 'list[V1ResourceTag]':
        """Gets the tags of this DeploymenttemplatesIdBody.  # noqa: E501


        :return: The tags of this DeploymenttemplatesIdBody.  # noqa: E501
        :rtype: list[V1ResourceTag]
        """
        return self._tags

    @tags.setter
    def tags(self, tags: 'list[V1ResourceTag]'):
        """Sets the tags of this DeploymenttemplatesIdBody.


        :param tags: The tags of this DeploymenttemplatesIdBody.  # noqa: E501
        :type: list[V1ResourceTag]
        """

        self._tags = tags

    @property
    def thumbnail(self) -> 'str':
        """Gets the thumbnail of this DeploymenttemplatesIdBody.  # noqa: E501


        :return: The thumbnail of this DeploymenttemplatesIdBody.  # noqa: E501
        :rtype: str
        """
        return self._thumbnail

    @thumbnail.setter
    def thumbnail(self, thumbnail: 'str'):
        """Sets the thumbnail of this DeploymenttemplatesIdBody.


        :param thumbnail: The thumbnail of this DeploymenttemplatesIdBody.  # noqa: E501
        :type: str
        """

        self._thumbnail = thumbnail

    @property
    def thumbnail_file_type(self) -> 'str':
        """Gets the thumbnail_file_type of this DeploymenttemplatesIdBody.  # noqa: E501


        :return: The thumbnail_file_type of this DeploymenttemplatesIdBody.  # noqa: E501
        :rtype: str
        """
        return self._thumbnail_file_type

    @thumbnail_file_type.setter
    def thumbnail_file_type(self, thumbnail_file_type: 'str'):
        """Sets the thumbnail_file_type of this DeploymenttemplatesIdBody.


        :param thumbnail_file_type: The thumbnail_file_type of this DeploymenttemplatesIdBody.  # noqa: E501
        :type: str
        """

        self._thumbnail_file_type = thumbnail_file_type

    @property
    def visibility(self) -> 'V1DeploymentTemplateType':
        """Gets the visibility of this DeploymenttemplatesIdBody.  # noqa: E501


        :return: The visibility of this DeploymenttemplatesIdBody.  # noqa: E501
        :rtype: V1DeploymentTemplateType
        """
        return self._visibility

    @visibility.setter
    def visibility(self, visibility: 'V1DeploymentTemplateType'):
        """Sets the visibility of this DeploymenttemplatesIdBody.


        :param visibility: The visibility of this DeploymenttemplatesIdBody.  # noqa: E501
        :type: V1DeploymentTemplateType
        """

        self._visibility = visibility

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
        if issubclass(DeploymenttemplatesIdBody, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'DeploymenttemplatesIdBody') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, DeploymenttemplatesIdBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'DeploymenttemplatesIdBody') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
