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

class V1BillingSubscription(object):
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
        'amount': 'int',
        'card_last4': 'str',
        'card_type': 'str',
        'features': 'list[V1BillingFeature]',
        'name': 'str',
        'period': 'str',
        'period_end': 'datetime',
        'seats': 'int',
        'status': 'str',
        'stripe_managed': 'bool'
    }

    attribute_map = {
        'amount': 'amount',
        'card_last4': 'cardLast4',
        'card_type': 'cardType',
        'features': 'features',
        'name': 'name',
        'period': 'period',
        'period_end': 'periodEnd',
        'seats': 'seats',
        'status': 'status',
        'stripe_managed': 'stripeManaged'
    }

    def __init__(self, amount: 'int' =None, card_last4: 'str' =None, card_type: 'str' =None, features: 'list[V1BillingFeature]' =None, name: 'str' =None, period: 'str' =None, period_end: 'datetime' =None, seats: 'int' =None, status: 'str' =None, stripe_managed: 'bool' =None):  # noqa: E501
        """V1BillingSubscription - a model defined in Swagger"""  # noqa: E501
        self._amount = None
        self._card_last4 = None
        self._card_type = None
        self._features = None
        self._name = None
        self._period = None
        self._period_end = None
        self._seats = None
        self._status = None
        self._stripe_managed = None
        self.discriminator = None
        if amount is not None:
            self.amount = amount
        if card_last4 is not None:
            self.card_last4 = card_last4
        if card_type is not None:
            self.card_type = card_type
        if features is not None:
            self.features = features
        if name is not None:
            self.name = name
        if period is not None:
            self.period = period
        if period_end is not None:
            self.period_end = period_end
        if seats is not None:
            self.seats = seats
        if status is not None:
            self.status = status
        if stripe_managed is not None:
            self.stripe_managed = stripe_managed

    @property
    def amount(self) -> 'int':
        """Gets the amount of this V1BillingSubscription.  # noqa: E501


        :return: The amount of this V1BillingSubscription.  # noqa: E501
        :rtype: int
        """
        return self._amount

    @amount.setter
    def amount(self, amount: 'int'):
        """Sets the amount of this V1BillingSubscription.


        :param amount: The amount of this V1BillingSubscription.  # noqa: E501
        :type: int
        """

        self._amount = amount

    @property
    def card_last4(self) -> 'str':
        """Gets the card_last4 of this V1BillingSubscription.  # noqa: E501


        :return: The card_last4 of this V1BillingSubscription.  # noqa: E501
        :rtype: str
        """
        return self._card_last4

    @card_last4.setter
    def card_last4(self, card_last4: 'str'):
        """Sets the card_last4 of this V1BillingSubscription.


        :param card_last4: The card_last4 of this V1BillingSubscription.  # noqa: E501
        :type: str
        """

        self._card_last4 = card_last4

    @property
    def card_type(self) -> 'str':
        """Gets the card_type of this V1BillingSubscription.  # noqa: E501


        :return: The card_type of this V1BillingSubscription.  # noqa: E501
        :rtype: str
        """
        return self._card_type

    @card_type.setter
    def card_type(self, card_type: 'str'):
        """Sets the card_type of this V1BillingSubscription.


        :param card_type: The card_type of this V1BillingSubscription.  # noqa: E501
        :type: str
        """

        self._card_type = card_type

    @property
    def features(self) -> 'list[V1BillingFeature]':
        """Gets the features of this V1BillingSubscription.  # noqa: E501


        :return: The features of this V1BillingSubscription.  # noqa: E501
        :rtype: list[V1BillingFeature]
        """
        return self._features

    @features.setter
    def features(self, features: 'list[V1BillingFeature]'):
        """Sets the features of this V1BillingSubscription.


        :param features: The features of this V1BillingSubscription.  # noqa: E501
        :type: list[V1BillingFeature]
        """

        self._features = features

    @property
    def name(self) -> 'str':
        """Gets the name of this V1BillingSubscription.  # noqa: E501


        :return: The name of this V1BillingSubscription.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: 'str'):
        """Sets the name of this V1BillingSubscription.


        :param name: The name of this V1BillingSubscription.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def period(self) -> 'str':
        """Gets the period of this V1BillingSubscription.  # noqa: E501


        :return: The period of this V1BillingSubscription.  # noqa: E501
        :rtype: str
        """
        return self._period

    @period.setter
    def period(self, period: 'str'):
        """Sets the period of this V1BillingSubscription.


        :param period: The period of this V1BillingSubscription.  # noqa: E501
        :type: str
        """

        self._period = period

    @property
    def period_end(self) -> 'datetime':
        """Gets the period_end of this V1BillingSubscription.  # noqa: E501


        :return: The period_end of this V1BillingSubscription.  # noqa: E501
        :rtype: datetime
        """
        return self._period_end

    @period_end.setter
    def period_end(self, period_end: 'datetime'):
        """Sets the period_end of this V1BillingSubscription.


        :param period_end: The period_end of this V1BillingSubscription.  # noqa: E501
        :type: datetime
        """

        self._period_end = period_end

    @property
    def seats(self) -> 'int':
        """Gets the seats of this V1BillingSubscription.  # noqa: E501


        :return: The seats of this V1BillingSubscription.  # noqa: E501
        :rtype: int
        """
        return self._seats

    @seats.setter
    def seats(self, seats: 'int'):
        """Sets the seats of this V1BillingSubscription.


        :param seats: The seats of this V1BillingSubscription.  # noqa: E501
        :type: int
        """

        self._seats = seats

    @property
    def status(self) -> 'str':
        """Gets the status of this V1BillingSubscription.  # noqa: E501


        :return: The status of this V1BillingSubscription.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: 'str'):
        """Sets the status of this V1BillingSubscription.


        :param status: The status of this V1BillingSubscription.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def stripe_managed(self) -> 'bool':
        """Gets the stripe_managed of this V1BillingSubscription.  # noqa: E501


        :return: The stripe_managed of this V1BillingSubscription.  # noqa: E501
        :rtype: bool
        """
        return self._stripe_managed

    @stripe_managed.setter
    def stripe_managed(self, stripe_managed: 'bool'):
        """Sets the stripe_managed of this V1BillingSubscription.


        :param stripe_managed: The stripe_managed of this V1BillingSubscription.  # noqa: E501
        :type: bool
        """

        self._stripe_managed = stripe_managed

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
        if issubclass(V1BillingSubscription, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1BillingSubscription') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1BillingSubscription):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1BillingSubscription') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
