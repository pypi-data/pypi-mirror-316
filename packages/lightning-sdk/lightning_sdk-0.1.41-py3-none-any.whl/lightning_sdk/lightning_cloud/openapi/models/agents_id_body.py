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

class AgentsIdBody(object):
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
        'cloudspace_id': 'str',
        'cluster_id': 'str',
        'created_at': 'datetime',
        'description': 'str',
        'endpoint_id': 'str',
        'expected_cold_start_time': 'str',
        'file_uploads_enabled': 'bool',
        'internal_assistant_name': 'str',
        'knowledge': 'str',
        'knowledge_configuration': 'V1KnowledgeConfiguration',
        'model': 'str',
        'model_provider': 'str',
        'name': 'str',
        'org_id': 'str',
        'prompt_suggestions': 'list[V1PromptSuggestion]',
        'prompt_template': 'str',
        'publish_status': 'str',
        'status': 'V1AssistantModelStatus',
        'thumbnail_url': 'str',
        'updated_at': 'datetime',
        'user_id': 'str'
    }

    attribute_map = {
        'cloudspace_id': 'cloudspaceId',
        'cluster_id': 'clusterId',
        'created_at': 'createdAt',
        'description': 'description',
        'endpoint_id': 'endpointId',
        'expected_cold_start_time': 'expectedColdStartTime',
        'file_uploads_enabled': 'fileUploadsEnabled',
        'internal_assistant_name': 'internalAssistantName',
        'knowledge': 'knowledge',
        'knowledge_configuration': 'knowledgeConfiguration',
        'model': 'model',
        'model_provider': 'modelProvider',
        'name': 'name',
        'org_id': 'orgId',
        'prompt_suggestions': 'promptSuggestions',
        'prompt_template': 'promptTemplate',
        'publish_status': 'publishStatus',
        'status': 'status',
        'thumbnail_url': 'thumbnailUrl',
        'updated_at': 'updatedAt',
        'user_id': 'userId'
    }

    def __init__(self, cloudspace_id: 'str' =None, cluster_id: 'str' =None, created_at: 'datetime' =None, description: 'str' =None, endpoint_id: 'str' =None, expected_cold_start_time: 'str' =None, file_uploads_enabled: 'bool' =None, internal_assistant_name: 'str' =None, knowledge: 'str' =None, knowledge_configuration: 'V1KnowledgeConfiguration' =None, model: 'str' =None, model_provider: 'str' =None, name: 'str' =None, org_id: 'str' =None, prompt_suggestions: 'list[V1PromptSuggestion]' =None, prompt_template: 'str' =None, publish_status: 'str' =None, status: 'V1AssistantModelStatus' =None, thumbnail_url: 'str' =None, updated_at: 'datetime' =None, user_id: 'str' =None):  # noqa: E501
        """AgentsIdBody - a model defined in Swagger"""  # noqa: E501
        self._cloudspace_id = None
        self._cluster_id = None
        self._created_at = None
        self._description = None
        self._endpoint_id = None
        self._expected_cold_start_time = None
        self._file_uploads_enabled = None
        self._internal_assistant_name = None
        self._knowledge = None
        self._knowledge_configuration = None
        self._model = None
        self._model_provider = None
        self._name = None
        self._org_id = None
        self._prompt_suggestions = None
        self._prompt_template = None
        self._publish_status = None
        self._status = None
        self._thumbnail_url = None
        self._updated_at = None
        self._user_id = None
        self.discriminator = None
        if cloudspace_id is not None:
            self.cloudspace_id = cloudspace_id
        if cluster_id is not None:
            self.cluster_id = cluster_id
        if created_at is not None:
            self.created_at = created_at
        if description is not None:
            self.description = description
        if endpoint_id is not None:
            self.endpoint_id = endpoint_id
        if expected_cold_start_time is not None:
            self.expected_cold_start_time = expected_cold_start_time
        if file_uploads_enabled is not None:
            self.file_uploads_enabled = file_uploads_enabled
        if internal_assistant_name is not None:
            self.internal_assistant_name = internal_assistant_name
        if knowledge is not None:
            self.knowledge = knowledge
        if knowledge_configuration is not None:
            self.knowledge_configuration = knowledge_configuration
        if model is not None:
            self.model = model
        if model_provider is not None:
            self.model_provider = model_provider
        if name is not None:
            self.name = name
        if org_id is not None:
            self.org_id = org_id
        if prompt_suggestions is not None:
            self.prompt_suggestions = prompt_suggestions
        if prompt_template is not None:
            self.prompt_template = prompt_template
        if publish_status is not None:
            self.publish_status = publish_status
        if status is not None:
            self.status = status
        if thumbnail_url is not None:
            self.thumbnail_url = thumbnail_url
        if updated_at is not None:
            self.updated_at = updated_at
        if user_id is not None:
            self.user_id = user_id

    @property
    def cloudspace_id(self) -> 'str':
        """Gets the cloudspace_id of this AgentsIdBody.  # noqa: E501


        :return: The cloudspace_id of this AgentsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._cloudspace_id

    @cloudspace_id.setter
    def cloudspace_id(self, cloudspace_id: 'str'):
        """Sets the cloudspace_id of this AgentsIdBody.


        :param cloudspace_id: The cloudspace_id of this AgentsIdBody.  # noqa: E501
        :type: str
        """

        self._cloudspace_id = cloudspace_id

    @property
    def cluster_id(self) -> 'str':
        """Gets the cluster_id of this AgentsIdBody.  # noqa: E501


        :return: The cluster_id of this AgentsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._cluster_id

    @cluster_id.setter
    def cluster_id(self, cluster_id: 'str'):
        """Sets the cluster_id of this AgentsIdBody.


        :param cluster_id: The cluster_id of this AgentsIdBody.  # noqa: E501
        :type: str
        """

        self._cluster_id = cluster_id

    @property
    def created_at(self) -> 'datetime':
        """Gets the created_at of this AgentsIdBody.  # noqa: E501


        :return: The created_at of this AgentsIdBody.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at: 'datetime'):
        """Sets the created_at of this AgentsIdBody.


        :param created_at: The created_at of this AgentsIdBody.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def description(self) -> 'str':
        """Gets the description of this AgentsIdBody.  # noqa: E501


        :return: The description of this AgentsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: 'str'):
        """Sets the description of this AgentsIdBody.


        :param description: The description of this AgentsIdBody.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def endpoint_id(self) -> 'str':
        """Gets the endpoint_id of this AgentsIdBody.  # noqa: E501


        :return: The endpoint_id of this AgentsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._endpoint_id

    @endpoint_id.setter
    def endpoint_id(self, endpoint_id: 'str'):
        """Sets the endpoint_id of this AgentsIdBody.


        :param endpoint_id: The endpoint_id of this AgentsIdBody.  # noqa: E501
        :type: str
        """

        self._endpoint_id = endpoint_id

    @property
    def expected_cold_start_time(self) -> 'str':
        """Gets the expected_cold_start_time of this AgentsIdBody.  # noqa: E501


        :return: The expected_cold_start_time of this AgentsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._expected_cold_start_time

    @expected_cold_start_time.setter
    def expected_cold_start_time(self, expected_cold_start_time: 'str'):
        """Sets the expected_cold_start_time of this AgentsIdBody.


        :param expected_cold_start_time: The expected_cold_start_time of this AgentsIdBody.  # noqa: E501
        :type: str
        """

        self._expected_cold_start_time = expected_cold_start_time

    @property
    def file_uploads_enabled(self) -> 'bool':
        """Gets the file_uploads_enabled of this AgentsIdBody.  # noqa: E501


        :return: The file_uploads_enabled of this AgentsIdBody.  # noqa: E501
        :rtype: bool
        """
        return self._file_uploads_enabled

    @file_uploads_enabled.setter
    def file_uploads_enabled(self, file_uploads_enabled: 'bool'):
        """Sets the file_uploads_enabled of this AgentsIdBody.


        :param file_uploads_enabled: The file_uploads_enabled of this AgentsIdBody.  # noqa: E501
        :type: bool
        """

        self._file_uploads_enabled = file_uploads_enabled

    @property
    def internal_assistant_name(self) -> 'str':
        """Gets the internal_assistant_name of this AgentsIdBody.  # noqa: E501


        :return: The internal_assistant_name of this AgentsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._internal_assistant_name

    @internal_assistant_name.setter
    def internal_assistant_name(self, internal_assistant_name: 'str'):
        """Sets the internal_assistant_name of this AgentsIdBody.


        :param internal_assistant_name: The internal_assistant_name of this AgentsIdBody.  # noqa: E501
        :type: str
        """

        self._internal_assistant_name = internal_assistant_name

    @property
    def knowledge(self) -> 'str':
        """Gets the knowledge of this AgentsIdBody.  # noqa: E501


        :return: The knowledge of this AgentsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._knowledge

    @knowledge.setter
    def knowledge(self, knowledge: 'str'):
        """Sets the knowledge of this AgentsIdBody.


        :param knowledge: The knowledge of this AgentsIdBody.  # noqa: E501
        :type: str
        """

        self._knowledge = knowledge

    @property
    def knowledge_configuration(self) -> 'V1KnowledgeConfiguration':
        """Gets the knowledge_configuration of this AgentsIdBody.  # noqa: E501


        :return: The knowledge_configuration of this AgentsIdBody.  # noqa: E501
        :rtype: V1KnowledgeConfiguration
        """
        return self._knowledge_configuration

    @knowledge_configuration.setter
    def knowledge_configuration(self, knowledge_configuration: 'V1KnowledgeConfiguration'):
        """Sets the knowledge_configuration of this AgentsIdBody.


        :param knowledge_configuration: The knowledge_configuration of this AgentsIdBody.  # noqa: E501
        :type: V1KnowledgeConfiguration
        """

        self._knowledge_configuration = knowledge_configuration

    @property
    def model(self) -> 'str':
        """Gets the model of this AgentsIdBody.  # noqa: E501


        :return: The model of this AgentsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._model

    @model.setter
    def model(self, model: 'str'):
        """Sets the model of this AgentsIdBody.


        :param model: The model of this AgentsIdBody.  # noqa: E501
        :type: str
        """

        self._model = model

    @property
    def model_provider(self) -> 'str':
        """Gets the model_provider of this AgentsIdBody.  # noqa: E501


        :return: The model_provider of this AgentsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._model_provider

    @model_provider.setter
    def model_provider(self, model_provider: 'str'):
        """Sets the model_provider of this AgentsIdBody.


        :param model_provider: The model_provider of this AgentsIdBody.  # noqa: E501
        :type: str
        """

        self._model_provider = model_provider

    @property
    def name(self) -> 'str':
        """Gets the name of this AgentsIdBody.  # noqa: E501


        :return: The name of this AgentsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: 'str'):
        """Sets the name of this AgentsIdBody.


        :param name: The name of this AgentsIdBody.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def org_id(self) -> 'str':
        """Gets the org_id of this AgentsIdBody.  # noqa: E501


        :return: The org_id of this AgentsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._org_id

    @org_id.setter
    def org_id(self, org_id: 'str'):
        """Sets the org_id of this AgentsIdBody.


        :param org_id: The org_id of this AgentsIdBody.  # noqa: E501
        :type: str
        """

        self._org_id = org_id

    @property
    def prompt_suggestions(self) -> 'list[V1PromptSuggestion]':
        """Gets the prompt_suggestions of this AgentsIdBody.  # noqa: E501


        :return: The prompt_suggestions of this AgentsIdBody.  # noqa: E501
        :rtype: list[V1PromptSuggestion]
        """
        return self._prompt_suggestions

    @prompt_suggestions.setter
    def prompt_suggestions(self, prompt_suggestions: 'list[V1PromptSuggestion]'):
        """Sets the prompt_suggestions of this AgentsIdBody.


        :param prompt_suggestions: The prompt_suggestions of this AgentsIdBody.  # noqa: E501
        :type: list[V1PromptSuggestion]
        """

        self._prompt_suggestions = prompt_suggestions

    @property
    def prompt_template(self) -> 'str':
        """Gets the prompt_template of this AgentsIdBody.  # noqa: E501


        :return: The prompt_template of this AgentsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._prompt_template

    @prompt_template.setter
    def prompt_template(self, prompt_template: 'str'):
        """Sets the prompt_template of this AgentsIdBody.


        :param prompt_template: The prompt_template of this AgentsIdBody.  # noqa: E501
        :type: str
        """

        self._prompt_template = prompt_template

    @property
    def publish_status(self) -> 'str':
        """Gets the publish_status of this AgentsIdBody.  # noqa: E501


        :return: The publish_status of this AgentsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._publish_status

    @publish_status.setter
    def publish_status(self, publish_status: 'str'):
        """Sets the publish_status of this AgentsIdBody.


        :param publish_status: The publish_status of this AgentsIdBody.  # noqa: E501
        :type: str
        """

        self._publish_status = publish_status

    @property
    def status(self) -> 'V1AssistantModelStatus':
        """Gets the status of this AgentsIdBody.  # noqa: E501


        :return: The status of this AgentsIdBody.  # noqa: E501
        :rtype: V1AssistantModelStatus
        """
        return self._status

    @status.setter
    def status(self, status: 'V1AssistantModelStatus'):
        """Sets the status of this AgentsIdBody.


        :param status: The status of this AgentsIdBody.  # noqa: E501
        :type: V1AssistantModelStatus
        """

        self._status = status

    @property
    def thumbnail_url(self) -> 'str':
        """Gets the thumbnail_url of this AgentsIdBody.  # noqa: E501


        :return: The thumbnail_url of this AgentsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._thumbnail_url

    @thumbnail_url.setter
    def thumbnail_url(self, thumbnail_url: 'str'):
        """Sets the thumbnail_url of this AgentsIdBody.


        :param thumbnail_url: The thumbnail_url of this AgentsIdBody.  # noqa: E501
        :type: str
        """

        self._thumbnail_url = thumbnail_url

    @property
    def updated_at(self) -> 'datetime':
        """Gets the updated_at of this AgentsIdBody.  # noqa: E501


        :return: The updated_at of this AgentsIdBody.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at: 'datetime'):
        """Sets the updated_at of this AgentsIdBody.


        :param updated_at: The updated_at of this AgentsIdBody.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def user_id(self) -> 'str':
        """Gets the user_id of this AgentsIdBody.  # noqa: E501


        :return: The user_id of this AgentsIdBody.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: 'str'):
        """Sets the user_id of this AgentsIdBody.


        :param user_id: The user_id of this AgentsIdBody.  # noqa: E501
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
        if issubclass(AgentsIdBody, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'AgentsIdBody') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, AgentsIdBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'AgentsIdBody') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
