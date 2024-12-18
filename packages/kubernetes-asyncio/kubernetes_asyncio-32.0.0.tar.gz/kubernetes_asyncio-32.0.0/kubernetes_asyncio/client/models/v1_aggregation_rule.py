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


class V1AggregationRule(object):
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
        'cluster_role_selectors': 'list[V1LabelSelector]'
    }

    attribute_map = {
        'cluster_role_selectors': 'clusterRoleSelectors'
    }

    def __init__(self, cluster_role_selectors=None, local_vars_configuration=None):  # noqa: E501
        """V1AggregationRule - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default()
        self.local_vars_configuration = local_vars_configuration

        self._cluster_role_selectors = None
        self.discriminator = None

        if cluster_role_selectors is not None:
            self.cluster_role_selectors = cluster_role_selectors

    @property
    def cluster_role_selectors(self):
        """Gets the cluster_role_selectors of this V1AggregationRule.  # noqa: E501

        ClusterRoleSelectors holds a list of selectors which will be used to find ClusterRoles and create the rules. If any of the selectors match, then the ClusterRole's permissions will be added  # noqa: E501

        :return: The cluster_role_selectors of this V1AggregationRule.  # noqa: E501
        :rtype: list[V1LabelSelector]
        """
        return self._cluster_role_selectors

    @cluster_role_selectors.setter
    def cluster_role_selectors(self, cluster_role_selectors):
        """Sets the cluster_role_selectors of this V1AggregationRule.

        ClusterRoleSelectors holds a list of selectors which will be used to find ClusterRoles and create the rules. If any of the selectors match, then the ClusterRole's permissions will be added  # noqa: E501

        :param cluster_role_selectors: The cluster_role_selectors of this V1AggregationRule.  # noqa: E501
        :type cluster_role_selectors: list[V1LabelSelector]
        """

        self._cluster_role_selectors = cluster_role_selectors

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
        if not isinstance(other, V1AggregationRule):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1AggregationRule):
            return True

        return self.to_dict() != other.to_dict()
