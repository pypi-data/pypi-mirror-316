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


class V2ExternalMetricStatus(object):
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
        'current': 'V2MetricValueStatus',
        'metric': 'V2MetricIdentifier'
    }

    attribute_map = {
        'current': 'current',
        'metric': 'metric'
    }

    def __init__(self, current=None, metric=None, local_vars_configuration=None):  # noqa: E501
        """V2ExternalMetricStatus - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default()
        self.local_vars_configuration = local_vars_configuration

        self._current = None
        self._metric = None
        self.discriminator = None

        self.current = current
        self.metric = metric

    @property
    def current(self):
        """Gets the current of this V2ExternalMetricStatus.  # noqa: E501


        :return: The current of this V2ExternalMetricStatus.  # noqa: E501
        :rtype: V2MetricValueStatus
        """
        return self._current

    @current.setter
    def current(self, current):
        """Sets the current of this V2ExternalMetricStatus.


        :param current: The current of this V2ExternalMetricStatus.  # noqa: E501
        :type current: V2MetricValueStatus
        """
        if self.local_vars_configuration.client_side_validation and current is None:  # noqa: E501
            raise ValueError("Invalid value for `current`, must not be `None`")  # noqa: E501

        self._current = current

    @property
    def metric(self):
        """Gets the metric of this V2ExternalMetricStatus.  # noqa: E501


        :return: The metric of this V2ExternalMetricStatus.  # noqa: E501
        :rtype: V2MetricIdentifier
        """
        return self._metric

    @metric.setter
    def metric(self, metric):
        """Sets the metric of this V2ExternalMetricStatus.


        :param metric: The metric of this V2ExternalMetricStatus.  # noqa: E501
        :type metric: V2MetricIdentifier
        """
        if self.local_vars_configuration.client_side_validation and metric is None:  # noqa: E501
            raise ValueError("Invalid value for `metric`, must not be `None`")  # noqa: E501

        self._metric = metric

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
        if not isinstance(other, V2ExternalMetricStatus):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V2ExternalMetricStatus):
            return True

        return self.to_dict() != other.to_dict()
