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

class V1CreateSubscriptionCheckoutSessionRequest(object):
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
        'billing_period': 'V1BillingPeriod',
        'org_id': 'str',
        'product_id': 'str',
        'redirect_url_failed': 'str',
        'redirect_url_succeeded': 'str',
        'seats': 'int'
    }

    attribute_map = {
        'billing_period': 'billingPeriod',
        'org_id': 'orgId',
        'product_id': 'productId',
        'redirect_url_failed': 'redirectUrlFailed',
        'redirect_url_succeeded': 'redirectUrlSucceeded',
        'seats': 'seats'
    }

    def __init__(self, billing_period: 'V1BillingPeriod' =None, org_id: 'str' =None, product_id: 'str' =None, redirect_url_failed: 'str' =None, redirect_url_succeeded: 'str' =None, seats: 'int' =None):  # noqa: E501
        """V1CreateSubscriptionCheckoutSessionRequest - a model defined in Swagger"""  # noqa: E501
        self._billing_period = None
        self._org_id = None
        self._product_id = None
        self._redirect_url_failed = None
        self._redirect_url_succeeded = None
        self._seats = None
        self.discriminator = None
        if billing_period is not None:
            self.billing_period = billing_period
        if org_id is not None:
            self.org_id = org_id
        if product_id is not None:
            self.product_id = product_id
        if redirect_url_failed is not None:
            self.redirect_url_failed = redirect_url_failed
        if redirect_url_succeeded is not None:
            self.redirect_url_succeeded = redirect_url_succeeded
        if seats is not None:
            self.seats = seats

    @property
    def billing_period(self) -> 'V1BillingPeriod':
        """Gets the billing_period of this V1CreateSubscriptionCheckoutSessionRequest.  # noqa: E501


        :return: The billing_period of this V1CreateSubscriptionCheckoutSessionRequest.  # noqa: E501
        :rtype: V1BillingPeriod
        """
        return self._billing_period

    @billing_period.setter
    def billing_period(self, billing_period: 'V1BillingPeriod'):
        """Sets the billing_period of this V1CreateSubscriptionCheckoutSessionRequest.


        :param billing_period: The billing_period of this V1CreateSubscriptionCheckoutSessionRequest.  # noqa: E501
        :type: V1BillingPeriod
        """

        self._billing_period = billing_period

    @property
    def org_id(self) -> 'str':
        """Gets the org_id of this V1CreateSubscriptionCheckoutSessionRequest.  # noqa: E501


        :return: The org_id of this V1CreateSubscriptionCheckoutSessionRequest.  # noqa: E501
        :rtype: str
        """
        return self._org_id

    @org_id.setter
    def org_id(self, org_id: 'str'):
        """Sets the org_id of this V1CreateSubscriptionCheckoutSessionRequest.


        :param org_id: The org_id of this V1CreateSubscriptionCheckoutSessionRequest.  # noqa: E501
        :type: str
        """

        self._org_id = org_id

    @property
    def product_id(self) -> 'str':
        """Gets the product_id of this V1CreateSubscriptionCheckoutSessionRequest.  # noqa: E501


        :return: The product_id of this V1CreateSubscriptionCheckoutSessionRequest.  # noqa: E501
        :rtype: str
        """
        return self._product_id

    @product_id.setter
    def product_id(self, product_id: 'str'):
        """Sets the product_id of this V1CreateSubscriptionCheckoutSessionRequest.


        :param product_id: The product_id of this V1CreateSubscriptionCheckoutSessionRequest.  # noqa: E501
        :type: str
        """

        self._product_id = product_id

    @property
    def redirect_url_failed(self) -> 'str':
        """Gets the redirect_url_failed of this V1CreateSubscriptionCheckoutSessionRequest.  # noqa: E501


        :return: The redirect_url_failed of this V1CreateSubscriptionCheckoutSessionRequest.  # noqa: E501
        :rtype: str
        """
        return self._redirect_url_failed

    @redirect_url_failed.setter
    def redirect_url_failed(self, redirect_url_failed: 'str'):
        """Sets the redirect_url_failed of this V1CreateSubscriptionCheckoutSessionRequest.


        :param redirect_url_failed: The redirect_url_failed of this V1CreateSubscriptionCheckoutSessionRequest.  # noqa: E501
        :type: str
        """

        self._redirect_url_failed = redirect_url_failed

    @property
    def redirect_url_succeeded(self) -> 'str':
        """Gets the redirect_url_succeeded of this V1CreateSubscriptionCheckoutSessionRequest.  # noqa: E501


        :return: The redirect_url_succeeded of this V1CreateSubscriptionCheckoutSessionRequest.  # noqa: E501
        :rtype: str
        """
        return self._redirect_url_succeeded

    @redirect_url_succeeded.setter
    def redirect_url_succeeded(self, redirect_url_succeeded: 'str'):
        """Sets the redirect_url_succeeded of this V1CreateSubscriptionCheckoutSessionRequest.


        :param redirect_url_succeeded: The redirect_url_succeeded of this V1CreateSubscriptionCheckoutSessionRequest.  # noqa: E501
        :type: str
        """

        self._redirect_url_succeeded = redirect_url_succeeded

    @property
    def seats(self) -> 'int':
        """Gets the seats of this V1CreateSubscriptionCheckoutSessionRequest.  # noqa: E501


        :return: The seats of this V1CreateSubscriptionCheckoutSessionRequest.  # noqa: E501
        :rtype: int
        """
        return self._seats

    @seats.setter
    def seats(self, seats: 'int'):
        """Sets the seats of this V1CreateSubscriptionCheckoutSessionRequest.


        :param seats: The seats of this V1CreateSubscriptionCheckoutSessionRequest.  # noqa: E501
        :type: int
        """

        self._seats = seats

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
        if issubclass(V1CreateSubscriptionCheckoutSessionRequest, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1CreateSubscriptionCheckoutSessionRequest') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1CreateSubscriptionCheckoutSessionRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1CreateSubscriptionCheckoutSessionRequest') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
