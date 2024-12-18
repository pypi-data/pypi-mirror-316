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


class V1NamedRuleWithOperations(object):
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
        'api_groups': 'list[str]',
        'api_versions': 'list[str]',
        'operations': 'list[str]',
        'resource_names': 'list[str]',
        'resources': 'list[str]',
        'scope': 'str'
    }

    attribute_map = {
        'api_groups': 'apiGroups',
        'api_versions': 'apiVersions',
        'operations': 'operations',
        'resource_names': 'resourceNames',
        'resources': 'resources',
        'scope': 'scope'
    }

    def __init__(self, api_groups=None, api_versions=None, operations=None, resource_names=None, resources=None, scope=None, local_vars_configuration=None):  # noqa: E501
        """V1NamedRuleWithOperations - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default()
        self.local_vars_configuration = local_vars_configuration

        self._api_groups = None
        self._api_versions = None
        self._operations = None
        self._resource_names = None
        self._resources = None
        self._scope = None
        self.discriminator = None

        if api_groups is not None:
            self.api_groups = api_groups
        if api_versions is not None:
            self.api_versions = api_versions
        if operations is not None:
            self.operations = operations
        if resource_names is not None:
            self.resource_names = resource_names
        if resources is not None:
            self.resources = resources
        if scope is not None:
            self.scope = scope

    @property
    def api_groups(self):
        """Gets the api_groups of this V1NamedRuleWithOperations.  # noqa: E501

        APIGroups is the API groups the resources belong to. '*' is all groups. If '*' is present, the length of the slice must be one. Required.  # noqa: E501

        :return: The api_groups of this V1NamedRuleWithOperations.  # noqa: E501
        :rtype: list[str]
        """
        return self._api_groups

    @api_groups.setter
    def api_groups(self, api_groups):
        """Sets the api_groups of this V1NamedRuleWithOperations.

        APIGroups is the API groups the resources belong to. '*' is all groups. If '*' is present, the length of the slice must be one. Required.  # noqa: E501

        :param api_groups: The api_groups of this V1NamedRuleWithOperations.  # noqa: E501
        :type api_groups: list[str]
        """

        self._api_groups = api_groups

    @property
    def api_versions(self):
        """Gets the api_versions of this V1NamedRuleWithOperations.  # noqa: E501

        APIVersions is the API versions the resources belong to. '*' is all versions. If '*' is present, the length of the slice must be one. Required.  # noqa: E501

        :return: The api_versions of this V1NamedRuleWithOperations.  # noqa: E501
        :rtype: list[str]
        """
        return self._api_versions

    @api_versions.setter
    def api_versions(self, api_versions):
        """Sets the api_versions of this V1NamedRuleWithOperations.

        APIVersions is the API versions the resources belong to. '*' is all versions. If '*' is present, the length of the slice must be one. Required.  # noqa: E501

        :param api_versions: The api_versions of this V1NamedRuleWithOperations.  # noqa: E501
        :type api_versions: list[str]
        """

        self._api_versions = api_versions

    @property
    def operations(self):
        """Gets the operations of this V1NamedRuleWithOperations.  # noqa: E501

        Operations is the operations the admission hook cares about - CREATE, UPDATE, DELETE, CONNECT or * for all of those operations and any future admission operations that are added. If '*' is present, the length of the slice must be one. Required.  # noqa: E501

        :return: The operations of this V1NamedRuleWithOperations.  # noqa: E501
        :rtype: list[str]
        """
        return self._operations

    @operations.setter
    def operations(self, operations):
        """Sets the operations of this V1NamedRuleWithOperations.

        Operations is the operations the admission hook cares about - CREATE, UPDATE, DELETE, CONNECT or * for all of those operations and any future admission operations that are added. If '*' is present, the length of the slice must be one. Required.  # noqa: E501

        :param operations: The operations of this V1NamedRuleWithOperations.  # noqa: E501
        :type operations: list[str]
        """

        self._operations = operations

    @property
    def resource_names(self):
        """Gets the resource_names of this V1NamedRuleWithOperations.  # noqa: E501

        ResourceNames is an optional white list of names that the rule applies to.  An empty set means that everything is allowed.  # noqa: E501

        :return: The resource_names of this V1NamedRuleWithOperations.  # noqa: E501
        :rtype: list[str]
        """
        return self._resource_names

    @resource_names.setter
    def resource_names(self, resource_names):
        """Sets the resource_names of this V1NamedRuleWithOperations.

        ResourceNames is an optional white list of names that the rule applies to.  An empty set means that everything is allowed.  # noqa: E501

        :param resource_names: The resource_names of this V1NamedRuleWithOperations.  # noqa: E501
        :type resource_names: list[str]
        """

        self._resource_names = resource_names

    @property
    def resources(self):
        """Gets the resources of this V1NamedRuleWithOperations.  # noqa: E501

        Resources is a list of resources this rule applies to.  For example: 'pods' means pods. 'pods/log' means the log subresource of pods. '*' means all resources, but not subresources. 'pods/*' means all subresources of pods. '*/scale' means all scale subresources. '*/*' means all resources and their subresources.  If wildcard is present, the validation rule will ensure resources do not overlap with each other.  Depending on the enclosing object, subresources might not be allowed. Required.  # noqa: E501

        :return: The resources of this V1NamedRuleWithOperations.  # noqa: E501
        :rtype: list[str]
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """Sets the resources of this V1NamedRuleWithOperations.

        Resources is a list of resources this rule applies to.  For example: 'pods' means pods. 'pods/log' means the log subresource of pods. '*' means all resources, but not subresources. 'pods/*' means all subresources of pods. '*/scale' means all scale subresources. '*/*' means all resources and their subresources.  If wildcard is present, the validation rule will ensure resources do not overlap with each other.  Depending on the enclosing object, subresources might not be allowed. Required.  # noqa: E501

        :param resources: The resources of this V1NamedRuleWithOperations.  # noqa: E501
        :type resources: list[str]
        """

        self._resources = resources

    @property
    def scope(self):
        """Gets the scope of this V1NamedRuleWithOperations.  # noqa: E501

        scope specifies the scope of this rule. Valid values are \"Cluster\", \"Namespaced\", and \"*\" \"Cluster\" means that only cluster-scoped resources will match this rule. Namespace API objects are cluster-scoped. \"Namespaced\" means that only namespaced resources will match this rule. \"*\" means that there are no scope restrictions. Subresources match the scope of their parent resource. Default is \"*\".  # noqa: E501

        :return: The scope of this V1NamedRuleWithOperations.  # noqa: E501
        :rtype: str
        """
        return self._scope

    @scope.setter
    def scope(self, scope):
        """Sets the scope of this V1NamedRuleWithOperations.

        scope specifies the scope of this rule. Valid values are \"Cluster\", \"Namespaced\", and \"*\" \"Cluster\" means that only cluster-scoped resources will match this rule. Namespace API objects are cluster-scoped. \"Namespaced\" means that only namespaced resources will match this rule. \"*\" means that there are no scope restrictions. Subresources match the scope of their parent resource. Default is \"*\".  # noqa: E501

        :param scope: The scope of this V1NamedRuleWithOperations.  # noqa: E501
        :type scope: str
        """

        self._scope = scope

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
        if not isinstance(other, V1NamedRuleWithOperations):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1NamedRuleWithOperations):
            return True

        return self.to_dict() != other.to_dict()
