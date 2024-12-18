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

class V1ClusterAccelerator(object):
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
        'accelerator_type': 'str',
        'allowed_resources': 'list[str]',
        'available_in_seconds': 'str',
        'available_in_seconds_spot': 'str',
        'available_zones': 'list[str]',
        'byoc_only': 'bool',
        'capacity_block_only': 'bool',
        'capacity_block_price': 'float',
        'capacity_blocks_available': 'list[V1ClusterCapacityReservation]',
        'cluster_id': 'str',
        'cost': 'float',
        'detailed_quotas_info': 'list[V1AcceleratorQuotaInfo]',
        'device_card': 'str',
        'device_info': 'str',
        'display_name': 'str',
        'dws_only': 'bool',
        'enabled': 'bool',
        'family': 'str',
        'instance_id': 'str',
        'is_custom': 'bool',
        'is_tier_restricted': 'bool',
        'local_disk_size': 'str',
        'local_disk_supported': 'bool',
        'max_available_quota': 'str',
        'non_spot': 'bool',
        'quota_checked_at': 'datetime',
        'quota_code': 'str',
        'quota_name': 'str',
        'quota_page_url': 'str',
        'quota_service_code': 'str',
        'quota_utilization': 'str',
        'quota_value': 'str',
        'reservable': 'bool',
        'reservation_available_zones': 'list[str]',
        'resources': 'V1Resources',
        'slug': 'str',
        'spot_price': 'float'
    }

    attribute_map = {
        'accelerator_type': 'acceleratorType',
        'allowed_resources': 'allowedResources',
        'available_in_seconds': 'availableInSeconds',
        'available_in_seconds_spot': 'availableInSecondsSpot',
        'available_zones': 'availableZones',
        'byoc_only': 'byocOnly',
        'capacity_block_only': 'capacityBlockOnly',
        'capacity_block_price': 'capacityBlockPrice',
        'capacity_blocks_available': 'capacityBlocksAvailable',
        'cluster_id': 'clusterId',
        'cost': 'cost',
        'detailed_quotas_info': 'detailedQuotasInfo',
        'device_card': 'deviceCard',
        'device_info': 'deviceInfo',
        'display_name': 'displayName',
        'dws_only': 'dwsOnly',
        'enabled': 'enabled',
        'family': 'family',
        'instance_id': 'instanceId',
        'is_custom': 'isCustom',
        'is_tier_restricted': 'isTierRestricted',
        'local_disk_size': 'localDiskSize',
        'local_disk_supported': 'localDiskSupported',
        'max_available_quota': 'maxAvailableQuota',
        'non_spot': 'nonSpot',
        'quota_checked_at': 'quotaCheckedAt',
        'quota_code': 'quotaCode',
        'quota_name': 'quotaName',
        'quota_page_url': 'quotaPageUrl',
        'quota_service_code': 'quotaServiceCode',
        'quota_utilization': 'quotaUtilization',
        'quota_value': 'quotaValue',
        'reservable': 'reservable',
        'reservation_available_zones': 'reservationAvailableZones',
        'resources': 'resources',
        'slug': 'slug',
        'spot_price': 'spotPrice'
    }

    def __init__(self, accelerator_type: 'str' =None, allowed_resources: 'list[str]' =None, available_in_seconds: 'str' =None, available_in_seconds_spot: 'str' =None, available_zones: 'list[str]' =None, byoc_only: 'bool' =None, capacity_block_only: 'bool' =None, capacity_block_price: 'float' =None, capacity_blocks_available: 'list[V1ClusterCapacityReservation]' =None, cluster_id: 'str' =None, cost: 'float' =None, detailed_quotas_info: 'list[V1AcceleratorQuotaInfo]' =None, device_card: 'str' =None, device_info: 'str' =None, display_name: 'str' =None, dws_only: 'bool' =None, enabled: 'bool' =None, family: 'str' =None, instance_id: 'str' =None, is_custom: 'bool' =None, is_tier_restricted: 'bool' =None, local_disk_size: 'str' =None, local_disk_supported: 'bool' =None, max_available_quota: 'str' =None, non_spot: 'bool' =None, quota_checked_at: 'datetime' =None, quota_code: 'str' =None, quota_name: 'str' =None, quota_page_url: 'str' =None, quota_service_code: 'str' =None, quota_utilization: 'str' =None, quota_value: 'str' =None, reservable: 'bool' =None, reservation_available_zones: 'list[str]' =None, resources: 'V1Resources' =None, slug: 'str' =None, spot_price: 'float' =None):  # noqa: E501
        """V1ClusterAccelerator - a model defined in Swagger"""  # noqa: E501
        self._accelerator_type = None
        self._allowed_resources = None
        self._available_in_seconds = None
        self._available_in_seconds_spot = None
        self._available_zones = None
        self._byoc_only = None
        self._capacity_block_only = None
        self._capacity_block_price = None
        self._capacity_blocks_available = None
        self._cluster_id = None
        self._cost = None
        self._detailed_quotas_info = None
        self._device_card = None
        self._device_info = None
        self._display_name = None
        self._dws_only = None
        self._enabled = None
        self._family = None
        self._instance_id = None
        self._is_custom = None
        self._is_tier_restricted = None
        self._local_disk_size = None
        self._local_disk_supported = None
        self._max_available_quota = None
        self._non_spot = None
        self._quota_checked_at = None
        self._quota_code = None
        self._quota_name = None
        self._quota_page_url = None
        self._quota_service_code = None
        self._quota_utilization = None
        self._quota_value = None
        self._reservable = None
        self._reservation_available_zones = None
        self._resources = None
        self._slug = None
        self._spot_price = None
        self.discriminator = None
        if accelerator_type is not None:
            self.accelerator_type = accelerator_type
        if allowed_resources is not None:
            self.allowed_resources = allowed_resources
        if available_in_seconds is not None:
            self.available_in_seconds = available_in_seconds
        if available_in_seconds_spot is not None:
            self.available_in_seconds_spot = available_in_seconds_spot
        if available_zones is not None:
            self.available_zones = available_zones
        if byoc_only is not None:
            self.byoc_only = byoc_only
        if capacity_block_only is not None:
            self.capacity_block_only = capacity_block_only
        if capacity_block_price is not None:
            self.capacity_block_price = capacity_block_price
        if capacity_blocks_available is not None:
            self.capacity_blocks_available = capacity_blocks_available
        if cluster_id is not None:
            self.cluster_id = cluster_id
        if cost is not None:
            self.cost = cost
        if detailed_quotas_info is not None:
            self.detailed_quotas_info = detailed_quotas_info
        if device_card is not None:
            self.device_card = device_card
        if device_info is not None:
            self.device_info = device_info
        if display_name is not None:
            self.display_name = display_name
        if dws_only is not None:
            self.dws_only = dws_only
        if enabled is not None:
            self.enabled = enabled
        if family is not None:
            self.family = family
        if instance_id is not None:
            self.instance_id = instance_id
        if is_custom is not None:
            self.is_custom = is_custom
        if is_tier_restricted is not None:
            self.is_tier_restricted = is_tier_restricted
        if local_disk_size is not None:
            self.local_disk_size = local_disk_size
        if local_disk_supported is not None:
            self.local_disk_supported = local_disk_supported
        if max_available_quota is not None:
            self.max_available_quota = max_available_quota
        if non_spot is not None:
            self.non_spot = non_spot
        if quota_checked_at is not None:
            self.quota_checked_at = quota_checked_at
        if quota_code is not None:
            self.quota_code = quota_code
        if quota_name is not None:
            self.quota_name = quota_name
        if quota_page_url is not None:
            self.quota_page_url = quota_page_url
        if quota_service_code is not None:
            self.quota_service_code = quota_service_code
        if quota_utilization is not None:
            self.quota_utilization = quota_utilization
        if quota_value is not None:
            self.quota_value = quota_value
        if reservable is not None:
            self.reservable = reservable
        if reservation_available_zones is not None:
            self.reservation_available_zones = reservation_available_zones
        if resources is not None:
            self.resources = resources
        if slug is not None:
            self.slug = slug
        if spot_price is not None:
            self.spot_price = spot_price

    @property
    def accelerator_type(self) -> 'str':
        """Gets the accelerator_type of this V1ClusterAccelerator.  # noqa: E501


        :return: The accelerator_type of this V1ClusterAccelerator.  # noqa: E501
        :rtype: str
        """
        return self._accelerator_type

    @accelerator_type.setter
    def accelerator_type(self, accelerator_type: 'str'):
        """Sets the accelerator_type of this V1ClusterAccelerator.


        :param accelerator_type: The accelerator_type of this V1ClusterAccelerator.  # noqa: E501
        :type: str
        """

        self._accelerator_type = accelerator_type

    @property
    def allowed_resources(self) -> 'list[str]':
        """Gets the allowed_resources of this V1ClusterAccelerator.  # noqa: E501


        :return: The allowed_resources of this V1ClusterAccelerator.  # noqa: E501
        :rtype: list[str]
        """
        return self._allowed_resources

    @allowed_resources.setter
    def allowed_resources(self, allowed_resources: 'list[str]'):
        """Sets the allowed_resources of this V1ClusterAccelerator.


        :param allowed_resources: The allowed_resources of this V1ClusterAccelerator.  # noqa: E501
        :type: list[str]
        """

        self._allowed_resources = allowed_resources

    @property
    def available_in_seconds(self) -> 'str':
        """Gets the available_in_seconds of this V1ClusterAccelerator.  # noqa: E501


        :return: The available_in_seconds of this V1ClusterAccelerator.  # noqa: E501
        :rtype: str
        """
        return self._available_in_seconds

    @available_in_seconds.setter
    def available_in_seconds(self, available_in_seconds: 'str'):
        """Sets the available_in_seconds of this V1ClusterAccelerator.


        :param available_in_seconds: The available_in_seconds of this V1ClusterAccelerator.  # noqa: E501
        :type: str
        """

        self._available_in_seconds = available_in_seconds

    @property
    def available_in_seconds_spot(self) -> 'str':
        """Gets the available_in_seconds_spot of this V1ClusterAccelerator.  # noqa: E501


        :return: The available_in_seconds_spot of this V1ClusterAccelerator.  # noqa: E501
        :rtype: str
        """
        return self._available_in_seconds_spot

    @available_in_seconds_spot.setter
    def available_in_seconds_spot(self, available_in_seconds_spot: 'str'):
        """Sets the available_in_seconds_spot of this V1ClusterAccelerator.


        :param available_in_seconds_spot: The available_in_seconds_spot of this V1ClusterAccelerator.  # noqa: E501
        :type: str
        """

        self._available_in_seconds_spot = available_in_seconds_spot

    @property
    def available_zones(self) -> 'list[str]':
        """Gets the available_zones of this V1ClusterAccelerator.  # noqa: E501


        :return: The available_zones of this V1ClusterAccelerator.  # noqa: E501
        :rtype: list[str]
        """
        return self._available_zones

    @available_zones.setter
    def available_zones(self, available_zones: 'list[str]'):
        """Sets the available_zones of this V1ClusterAccelerator.


        :param available_zones: The available_zones of this V1ClusterAccelerator.  # noqa: E501
        :type: list[str]
        """

        self._available_zones = available_zones

    @property
    def byoc_only(self) -> 'bool':
        """Gets the byoc_only of this V1ClusterAccelerator.  # noqa: E501


        :return: The byoc_only of this V1ClusterAccelerator.  # noqa: E501
        :rtype: bool
        """
        return self._byoc_only

    @byoc_only.setter
    def byoc_only(self, byoc_only: 'bool'):
        """Sets the byoc_only of this V1ClusterAccelerator.


        :param byoc_only: The byoc_only of this V1ClusterAccelerator.  # noqa: E501
        :type: bool
        """

        self._byoc_only = byoc_only

    @property
    def capacity_block_only(self) -> 'bool':
        """Gets the capacity_block_only of this V1ClusterAccelerator.  # noqa: E501


        :return: The capacity_block_only of this V1ClusterAccelerator.  # noqa: E501
        :rtype: bool
        """
        return self._capacity_block_only

    @capacity_block_only.setter
    def capacity_block_only(self, capacity_block_only: 'bool'):
        """Sets the capacity_block_only of this V1ClusterAccelerator.


        :param capacity_block_only: The capacity_block_only of this V1ClusterAccelerator.  # noqa: E501
        :type: bool
        """

        self._capacity_block_only = capacity_block_only

    @property
    def capacity_block_price(self) -> 'float':
        """Gets the capacity_block_price of this V1ClusterAccelerator.  # noqa: E501


        :return: The capacity_block_price of this V1ClusterAccelerator.  # noqa: E501
        :rtype: float
        """
        return self._capacity_block_price

    @capacity_block_price.setter
    def capacity_block_price(self, capacity_block_price: 'float'):
        """Sets the capacity_block_price of this V1ClusterAccelerator.


        :param capacity_block_price: The capacity_block_price of this V1ClusterAccelerator.  # noqa: E501
        :type: float
        """

        self._capacity_block_price = capacity_block_price

    @property
    def capacity_blocks_available(self) -> 'list[V1ClusterCapacityReservation]':
        """Gets the capacity_blocks_available of this V1ClusterAccelerator.  # noqa: E501


        :return: The capacity_blocks_available of this V1ClusterAccelerator.  # noqa: E501
        :rtype: list[V1ClusterCapacityReservation]
        """
        return self._capacity_blocks_available

    @capacity_blocks_available.setter
    def capacity_blocks_available(self, capacity_blocks_available: 'list[V1ClusterCapacityReservation]'):
        """Sets the capacity_blocks_available of this V1ClusterAccelerator.


        :param capacity_blocks_available: The capacity_blocks_available of this V1ClusterAccelerator.  # noqa: E501
        :type: list[V1ClusterCapacityReservation]
        """

        self._capacity_blocks_available = capacity_blocks_available

    @property
    def cluster_id(self) -> 'str':
        """Gets the cluster_id of this V1ClusterAccelerator.  # noqa: E501


        :return: The cluster_id of this V1ClusterAccelerator.  # noqa: E501
        :rtype: str
        """
        return self._cluster_id

    @cluster_id.setter
    def cluster_id(self, cluster_id: 'str'):
        """Sets the cluster_id of this V1ClusterAccelerator.


        :param cluster_id: The cluster_id of this V1ClusterAccelerator.  # noqa: E501
        :type: str
        """

        self._cluster_id = cluster_id

    @property
    def cost(self) -> 'float':
        """Gets the cost of this V1ClusterAccelerator.  # noqa: E501


        :return: The cost of this V1ClusterAccelerator.  # noqa: E501
        :rtype: float
        """
        return self._cost

    @cost.setter
    def cost(self, cost: 'float'):
        """Sets the cost of this V1ClusterAccelerator.


        :param cost: The cost of this V1ClusterAccelerator.  # noqa: E501
        :type: float
        """

        self._cost = cost

    @property
    def detailed_quotas_info(self) -> 'list[V1AcceleratorQuotaInfo]':
        """Gets the detailed_quotas_info of this V1ClusterAccelerator.  # noqa: E501


        :return: The detailed_quotas_info of this V1ClusterAccelerator.  # noqa: E501
        :rtype: list[V1AcceleratorQuotaInfo]
        """
        return self._detailed_quotas_info

    @detailed_quotas_info.setter
    def detailed_quotas_info(self, detailed_quotas_info: 'list[V1AcceleratorQuotaInfo]'):
        """Sets the detailed_quotas_info of this V1ClusterAccelerator.


        :param detailed_quotas_info: The detailed_quotas_info of this V1ClusterAccelerator.  # noqa: E501
        :type: list[V1AcceleratorQuotaInfo]
        """

        self._detailed_quotas_info = detailed_quotas_info

    @property
    def device_card(self) -> 'str':
        """Gets the device_card of this V1ClusterAccelerator.  # noqa: E501


        :return: The device_card of this V1ClusterAccelerator.  # noqa: E501
        :rtype: str
        """
        return self._device_card

    @device_card.setter
    def device_card(self, device_card: 'str'):
        """Sets the device_card of this V1ClusterAccelerator.


        :param device_card: The device_card of this V1ClusterAccelerator.  # noqa: E501
        :type: str
        """

        self._device_card = device_card

    @property
    def device_info(self) -> 'str':
        """Gets the device_info of this V1ClusterAccelerator.  # noqa: E501


        :return: The device_info of this V1ClusterAccelerator.  # noqa: E501
        :rtype: str
        """
        return self._device_info

    @device_info.setter
    def device_info(self, device_info: 'str'):
        """Sets the device_info of this V1ClusterAccelerator.


        :param device_info: The device_info of this V1ClusterAccelerator.  # noqa: E501
        :type: str
        """

        self._device_info = device_info

    @property
    def display_name(self) -> 'str':
        """Gets the display_name of this V1ClusterAccelerator.  # noqa: E501


        :return: The display_name of this V1ClusterAccelerator.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name: 'str'):
        """Sets the display_name of this V1ClusterAccelerator.


        :param display_name: The display_name of this V1ClusterAccelerator.  # noqa: E501
        :type: str
        """

        self._display_name = display_name

    @property
    def dws_only(self) -> 'bool':
        """Gets the dws_only of this V1ClusterAccelerator.  # noqa: E501


        :return: The dws_only of this V1ClusterAccelerator.  # noqa: E501
        :rtype: bool
        """
        return self._dws_only

    @dws_only.setter
    def dws_only(self, dws_only: 'bool'):
        """Sets the dws_only of this V1ClusterAccelerator.


        :param dws_only: The dws_only of this V1ClusterAccelerator.  # noqa: E501
        :type: bool
        """

        self._dws_only = dws_only

    @property
    def enabled(self) -> 'bool':
        """Gets the enabled of this V1ClusterAccelerator.  # noqa: E501


        :return: The enabled of this V1ClusterAccelerator.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled: 'bool'):
        """Sets the enabled of this V1ClusterAccelerator.


        :param enabled: The enabled of this V1ClusterAccelerator.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def family(self) -> 'str':
        """Gets the family of this V1ClusterAccelerator.  # noqa: E501


        :return: The family of this V1ClusterAccelerator.  # noqa: E501
        :rtype: str
        """
        return self._family

    @family.setter
    def family(self, family: 'str'):
        """Sets the family of this V1ClusterAccelerator.


        :param family: The family of this V1ClusterAccelerator.  # noqa: E501
        :type: str
        """

        self._family = family

    @property
    def instance_id(self) -> 'str':
        """Gets the instance_id of this V1ClusterAccelerator.  # noqa: E501


        :return: The instance_id of this V1ClusterAccelerator.  # noqa: E501
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id: 'str'):
        """Sets the instance_id of this V1ClusterAccelerator.


        :param instance_id: The instance_id of this V1ClusterAccelerator.  # noqa: E501
        :type: str
        """

        self._instance_id = instance_id

    @property
    def is_custom(self) -> 'bool':
        """Gets the is_custom of this V1ClusterAccelerator.  # noqa: E501


        :return: The is_custom of this V1ClusterAccelerator.  # noqa: E501
        :rtype: bool
        """
        return self._is_custom

    @is_custom.setter
    def is_custom(self, is_custom: 'bool'):
        """Sets the is_custom of this V1ClusterAccelerator.


        :param is_custom: The is_custom of this V1ClusterAccelerator.  # noqa: E501
        :type: bool
        """

        self._is_custom = is_custom

    @property
    def is_tier_restricted(self) -> 'bool':
        """Gets the is_tier_restricted of this V1ClusterAccelerator.  # noqa: E501


        :return: The is_tier_restricted of this V1ClusterAccelerator.  # noqa: E501
        :rtype: bool
        """
        return self._is_tier_restricted

    @is_tier_restricted.setter
    def is_tier_restricted(self, is_tier_restricted: 'bool'):
        """Sets the is_tier_restricted of this V1ClusterAccelerator.


        :param is_tier_restricted: The is_tier_restricted of this V1ClusterAccelerator.  # noqa: E501
        :type: bool
        """

        self._is_tier_restricted = is_tier_restricted

    @property
    def local_disk_size(self) -> 'str':
        """Gets the local_disk_size of this V1ClusterAccelerator.  # noqa: E501


        :return: The local_disk_size of this V1ClusterAccelerator.  # noqa: E501
        :rtype: str
        """
        return self._local_disk_size

    @local_disk_size.setter
    def local_disk_size(self, local_disk_size: 'str'):
        """Sets the local_disk_size of this V1ClusterAccelerator.


        :param local_disk_size: The local_disk_size of this V1ClusterAccelerator.  # noqa: E501
        :type: str
        """

        self._local_disk_size = local_disk_size

    @property
    def local_disk_supported(self) -> 'bool':
        """Gets the local_disk_supported of this V1ClusterAccelerator.  # noqa: E501


        :return: The local_disk_supported of this V1ClusterAccelerator.  # noqa: E501
        :rtype: bool
        """
        return self._local_disk_supported

    @local_disk_supported.setter
    def local_disk_supported(self, local_disk_supported: 'bool'):
        """Sets the local_disk_supported of this V1ClusterAccelerator.


        :param local_disk_supported: The local_disk_supported of this V1ClusterAccelerator.  # noqa: E501
        :type: bool
        """

        self._local_disk_supported = local_disk_supported

    @property
    def max_available_quota(self) -> 'str':
        """Gets the max_available_quota of this V1ClusterAccelerator.  # noqa: E501


        :return: The max_available_quota of this V1ClusterAccelerator.  # noqa: E501
        :rtype: str
        """
        return self._max_available_quota

    @max_available_quota.setter
    def max_available_quota(self, max_available_quota: 'str'):
        """Sets the max_available_quota of this V1ClusterAccelerator.


        :param max_available_quota: The max_available_quota of this V1ClusterAccelerator.  # noqa: E501
        :type: str
        """

        self._max_available_quota = max_available_quota

    @property
    def non_spot(self) -> 'bool':
        """Gets the non_spot of this V1ClusterAccelerator.  # noqa: E501


        :return: The non_spot of this V1ClusterAccelerator.  # noqa: E501
        :rtype: bool
        """
        return self._non_spot

    @non_spot.setter
    def non_spot(self, non_spot: 'bool'):
        """Sets the non_spot of this V1ClusterAccelerator.


        :param non_spot: The non_spot of this V1ClusterAccelerator.  # noqa: E501
        :type: bool
        """

        self._non_spot = non_spot

    @property
    def quota_checked_at(self) -> 'datetime':
        """Gets the quota_checked_at of this V1ClusterAccelerator.  # noqa: E501


        :return: The quota_checked_at of this V1ClusterAccelerator.  # noqa: E501
        :rtype: datetime
        """
        return self._quota_checked_at

    @quota_checked_at.setter
    def quota_checked_at(self, quota_checked_at: 'datetime'):
        """Sets the quota_checked_at of this V1ClusterAccelerator.


        :param quota_checked_at: The quota_checked_at of this V1ClusterAccelerator.  # noqa: E501
        :type: datetime
        """

        self._quota_checked_at = quota_checked_at

    @property
    def quota_code(self) -> 'str':
        """Gets the quota_code of this V1ClusterAccelerator.  # noqa: E501


        :return: The quota_code of this V1ClusterAccelerator.  # noqa: E501
        :rtype: str
        """
        return self._quota_code

    @quota_code.setter
    def quota_code(self, quota_code: 'str'):
        """Sets the quota_code of this V1ClusterAccelerator.


        :param quota_code: The quota_code of this V1ClusterAccelerator.  # noqa: E501
        :type: str
        """

        self._quota_code = quota_code

    @property
    def quota_name(self) -> 'str':
        """Gets the quota_name of this V1ClusterAccelerator.  # noqa: E501


        :return: The quota_name of this V1ClusterAccelerator.  # noqa: E501
        :rtype: str
        """
        return self._quota_name

    @quota_name.setter
    def quota_name(self, quota_name: 'str'):
        """Sets the quota_name of this V1ClusterAccelerator.


        :param quota_name: The quota_name of this V1ClusterAccelerator.  # noqa: E501
        :type: str
        """

        self._quota_name = quota_name

    @property
    def quota_page_url(self) -> 'str':
        """Gets the quota_page_url of this V1ClusterAccelerator.  # noqa: E501


        :return: The quota_page_url of this V1ClusterAccelerator.  # noqa: E501
        :rtype: str
        """
        return self._quota_page_url

    @quota_page_url.setter
    def quota_page_url(self, quota_page_url: 'str'):
        """Sets the quota_page_url of this V1ClusterAccelerator.


        :param quota_page_url: The quota_page_url of this V1ClusterAccelerator.  # noqa: E501
        :type: str
        """

        self._quota_page_url = quota_page_url

    @property
    def quota_service_code(self) -> 'str':
        """Gets the quota_service_code of this V1ClusterAccelerator.  # noqa: E501


        :return: The quota_service_code of this V1ClusterAccelerator.  # noqa: E501
        :rtype: str
        """
        return self._quota_service_code

    @quota_service_code.setter
    def quota_service_code(self, quota_service_code: 'str'):
        """Sets the quota_service_code of this V1ClusterAccelerator.


        :param quota_service_code: The quota_service_code of this V1ClusterAccelerator.  # noqa: E501
        :type: str
        """

        self._quota_service_code = quota_service_code

    @property
    def quota_utilization(self) -> 'str':
        """Gets the quota_utilization of this V1ClusterAccelerator.  # noqa: E501


        :return: The quota_utilization of this V1ClusterAccelerator.  # noqa: E501
        :rtype: str
        """
        return self._quota_utilization

    @quota_utilization.setter
    def quota_utilization(self, quota_utilization: 'str'):
        """Sets the quota_utilization of this V1ClusterAccelerator.


        :param quota_utilization: The quota_utilization of this V1ClusterAccelerator.  # noqa: E501
        :type: str
        """

        self._quota_utilization = quota_utilization

    @property
    def quota_value(self) -> 'str':
        """Gets the quota_value of this V1ClusterAccelerator.  # noqa: E501


        :return: The quota_value of this V1ClusterAccelerator.  # noqa: E501
        :rtype: str
        """
        return self._quota_value

    @quota_value.setter
    def quota_value(self, quota_value: 'str'):
        """Sets the quota_value of this V1ClusterAccelerator.


        :param quota_value: The quota_value of this V1ClusterAccelerator.  # noqa: E501
        :type: str
        """

        self._quota_value = quota_value

    @property
    def reservable(self) -> 'bool':
        """Gets the reservable of this V1ClusterAccelerator.  # noqa: E501


        :return: The reservable of this V1ClusterAccelerator.  # noqa: E501
        :rtype: bool
        """
        return self._reservable

    @reservable.setter
    def reservable(self, reservable: 'bool'):
        """Sets the reservable of this V1ClusterAccelerator.


        :param reservable: The reservable of this V1ClusterAccelerator.  # noqa: E501
        :type: bool
        """

        self._reservable = reservable

    @property
    def reservation_available_zones(self) -> 'list[str]':
        """Gets the reservation_available_zones of this V1ClusterAccelerator.  # noqa: E501


        :return: The reservation_available_zones of this V1ClusterAccelerator.  # noqa: E501
        :rtype: list[str]
        """
        return self._reservation_available_zones

    @reservation_available_zones.setter
    def reservation_available_zones(self, reservation_available_zones: 'list[str]'):
        """Sets the reservation_available_zones of this V1ClusterAccelerator.


        :param reservation_available_zones: The reservation_available_zones of this V1ClusterAccelerator.  # noqa: E501
        :type: list[str]
        """

        self._reservation_available_zones = reservation_available_zones

    @property
    def resources(self) -> 'V1Resources':
        """Gets the resources of this V1ClusterAccelerator.  # noqa: E501


        :return: The resources of this V1ClusterAccelerator.  # noqa: E501
        :rtype: V1Resources
        """
        return self._resources

    @resources.setter
    def resources(self, resources: 'V1Resources'):
        """Sets the resources of this V1ClusterAccelerator.


        :param resources: The resources of this V1ClusterAccelerator.  # noqa: E501
        :type: V1Resources
        """

        self._resources = resources

    @property
    def slug(self) -> 'str':
        """Gets the slug of this V1ClusterAccelerator.  # noqa: E501


        :return: The slug of this V1ClusterAccelerator.  # noqa: E501
        :rtype: str
        """
        return self._slug

    @slug.setter
    def slug(self, slug: 'str'):
        """Sets the slug of this V1ClusterAccelerator.


        :param slug: The slug of this V1ClusterAccelerator.  # noqa: E501
        :type: str
        """

        self._slug = slug

    @property
    def spot_price(self) -> 'float':
        """Gets the spot_price of this V1ClusterAccelerator.  # noqa: E501


        :return: The spot_price of this V1ClusterAccelerator.  # noqa: E501
        :rtype: float
        """
        return self._spot_price

    @spot_price.setter
    def spot_price(self, spot_price: 'float'):
        """Sets the spot_price of this V1ClusterAccelerator.


        :param spot_price: The spot_price of this V1ClusterAccelerator.  # noqa: E501
        :type: float
        """

        self._spot_price = spot_price

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
        if issubclass(V1ClusterAccelerator, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1ClusterAccelerator') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1ClusterAccelerator):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1ClusterAccelerator') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
