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


class V1beta1Device(object):
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
        'basic': 'V1beta1BasicDevice',
        'name': 'str'
    }

    attribute_map = {
        'basic': 'basic',
        'name': 'name'
    }

    def __init__(self, basic=None, name=None, local_vars_configuration=None):  # noqa: E501
        """V1beta1Device - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default()
        self.local_vars_configuration = local_vars_configuration

        self._basic = None
        self._name = None
        self.discriminator = None

        if basic is not None:
            self.basic = basic
        self.name = name

    @property
    def basic(self):
        """Gets the basic of this V1beta1Device.  # noqa: E501


        :return: The basic of this V1beta1Device.  # noqa: E501
        :rtype: V1beta1BasicDevice
        """
        return self._basic

    @basic.setter
    def basic(self, basic):
        """Sets the basic of this V1beta1Device.


        :param basic: The basic of this V1beta1Device.  # noqa: E501
        :type basic: V1beta1BasicDevice
        """

        self._basic = basic

    @property
    def name(self):
        """Gets the name of this V1beta1Device.  # noqa: E501

        Name is unique identifier among all devices managed by the driver in the pool. It must be a DNS label.  # noqa: E501

        :return: The name of this V1beta1Device.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this V1beta1Device.

        Name is unique identifier among all devices managed by the driver in the pool. It must be a DNS label.  # noqa: E501

        :param name: The name of this V1beta1Device.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

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
        if not isinstance(other, V1beta1Device):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1beta1Device):
            return True

        return self.to_dict() != other.to_dict()
