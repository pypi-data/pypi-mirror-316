# coding: utf-8

"""
    Kubernetes

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v1.32.0
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from kubernetes_asyncio.client.configuration import Configuration


class V1ResourceQuotaStatus(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'hard': 'dict(str, str)',
        'used': 'dict(str, str)'
    }

    attribute_map = {
        'hard': 'hard',
        'used': 'used'
    }

    def __init__(self, hard=None, used=None, local_vars_configuration=None):  # noqa: E501
        """V1ResourceQuotaStatus - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default()
        self.local_vars_configuration = local_vars_configuration

        self._hard = None
        self._used = None
        self.discriminator = None

        if hard is not None:
            self.hard = hard
        if used is not None:
            self.used = used

    @property
    def hard(self):
        """Gets the hard of this V1ResourceQuotaStatus.  # noqa: E501

        Hard is the set of enforced hard limits for each named resource. More info: https://kubernetes.io/docs/concepts/policy/resource-quotas/  # noqa: E501

        :return: The hard of this V1ResourceQuotaStatus.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._hard

    @hard.setter
    def hard(self, hard):
        """Sets the hard of this V1ResourceQuotaStatus.

        Hard is the set of enforced hard limits for each named resource. More info: https://kubernetes.io/docs/concepts/policy/resource-quotas/  # noqa: E501

        :param hard: The hard of this V1ResourceQuotaStatus.  # noqa: E501
        :type hard: dict(str, str)
        """

        self._hard = hard

    @property
    def used(self):
        """Gets the used of this V1ResourceQuotaStatus.  # noqa: E501

        Used is the current observed total usage of the resource in the namespace.  # noqa: E501

        :return: The used of this V1ResourceQuotaStatus.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._used

    @used.setter
    def used(self, used):
        """Sets the used of this V1ResourceQuotaStatus.

        Used is the current observed total usage of the resource in the namespace.  # noqa: E501

        :param used: The used of this V1ResourceQuotaStatus.  # noqa: E501
        :type used: dict(str, str)
        """

        self._used = used

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, V1ResourceQuotaStatus):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1ResourceQuotaStatus):
            return True

        return self.to_dict() != other.to_dict()
