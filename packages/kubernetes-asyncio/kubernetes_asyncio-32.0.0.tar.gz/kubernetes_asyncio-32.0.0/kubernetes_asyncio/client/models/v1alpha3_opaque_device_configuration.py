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


class V1alpha3OpaqueDeviceConfiguration(object):
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
        'driver': 'str',
        'parameters': 'object'
    }

    attribute_map = {
        'driver': 'driver',
        'parameters': 'parameters'
    }

    def __init__(self, driver=None, parameters=None, local_vars_configuration=None):  # noqa: E501
        """V1alpha3OpaqueDeviceConfiguration - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default()
        self.local_vars_configuration = local_vars_configuration

        self._driver = None
        self._parameters = None
        self.discriminator = None

        self.driver = driver
        self.parameters = parameters

    @property
    def driver(self):
        """Gets the driver of this V1alpha3OpaqueDeviceConfiguration.  # noqa: E501

        Driver is used to determine which kubelet plugin needs to be passed these configuration parameters.  An admission policy provided by the driver developer could use this to decide whether it needs to validate them.  Must be a DNS subdomain and should end with a DNS domain owned by the vendor of the driver.  # noqa: E501

        :return: The driver of this V1alpha3OpaqueDeviceConfiguration.  # noqa: E501
        :rtype: str
        """
        return self._driver

    @driver.setter
    def driver(self, driver):
        """Sets the driver of this V1alpha3OpaqueDeviceConfiguration.

        Driver is used to determine which kubelet plugin needs to be passed these configuration parameters.  An admission policy provided by the driver developer could use this to decide whether it needs to validate them.  Must be a DNS subdomain and should end with a DNS domain owned by the vendor of the driver.  # noqa: E501

        :param driver: The driver of this V1alpha3OpaqueDeviceConfiguration.  # noqa: E501
        :type driver: str
        """
        if self.local_vars_configuration.client_side_validation and driver is None:  # noqa: E501
            raise ValueError("Invalid value for `driver`, must not be `None`")  # noqa: E501

        self._driver = driver

    @property
    def parameters(self):
        """Gets the parameters of this V1alpha3OpaqueDeviceConfiguration.  # noqa: E501

        Parameters can contain arbitrary data. It is the responsibility of the driver developer to handle validation and versioning. Typically this includes self-identification and a version (\"kind\" + \"apiVersion\" for Kubernetes types), with conversion between different versions.  The length of the raw data must be smaller or equal to 10 Ki.  # noqa: E501

        :return: The parameters of this V1alpha3OpaqueDeviceConfiguration.  # noqa: E501
        :rtype: object
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Sets the parameters of this V1alpha3OpaqueDeviceConfiguration.

        Parameters can contain arbitrary data. It is the responsibility of the driver developer to handle validation and versioning. Typically this includes self-identification and a version (\"kind\" + \"apiVersion\" for Kubernetes types), with conversion between different versions.  The length of the raw data must be smaller or equal to 10 Ki.  # noqa: E501

        :param parameters: The parameters of this V1alpha3OpaqueDeviceConfiguration.  # noqa: E501
        :type parameters: object
        """
        if self.local_vars_configuration.client_side_validation and parameters is None:  # noqa: E501
            raise ValueError("Invalid value for `parameters`, must not be `None`")  # noqa: E501

        self._parameters = parameters

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
        if not isinstance(other, V1alpha3OpaqueDeviceConfiguration):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1alpha3OpaqueDeviceConfiguration):
            return True

        return self.to_dict() != other.to_dict()
