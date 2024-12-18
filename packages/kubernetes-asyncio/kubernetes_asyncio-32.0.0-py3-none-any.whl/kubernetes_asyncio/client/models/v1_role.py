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


class V1Role(object):
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
        'api_version': 'str',
        'kind': 'str',
        'metadata': 'V1ObjectMeta',
        'rules': 'list[V1PolicyRule]'
    }

    attribute_map = {
        'api_version': 'apiVersion',
        'kind': 'kind',
        'metadata': 'metadata',
        'rules': 'rules'
    }

    def __init__(self, api_version=None, kind=None, metadata=None, rules=None, local_vars_configuration=None):  # noqa: E501
        """V1Role - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default()
        self.local_vars_configuration = local_vars_configuration

        self._api_version = None
        self._kind = None
        self._metadata = None
        self._rules = None
        self.discriminator = None

        if api_version is not None:
            self.api_version = api_version
        if kind is not None:
            self.kind = kind
        if metadata is not None:
            self.metadata = metadata
        if rules is not None:
            self.rules = rules

    @property
    def api_version(self):
        """Gets the api_version of this V1Role.  # noqa: E501

        APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa: E501

        :return: The api_version of this V1Role.  # noqa: E501
        :rtype: str
        """
        return self._api_version

    @api_version.setter
    def api_version(self, api_version):
        """Sets the api_version of this V1Role.

        APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa: E501

        :param api_version: The api_version of this V1Role.  # noqa: E501
        :type api_version: str
        """

        self._api_version = api_version

    @property
    def kind(self):
        """Gets the kind of this V1Role.  # noqa: E501

        Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa: E501

        :return: The kind of this V1Role.  # noqa: E501
        :rtype: str
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """Sets the kind of this V1Role.

        Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa: E501

        :param kind: The kind of this V1Role.  # noqa: E501
        :type kind: str
        """

        self._kind = kind

    @property
    def metadata(self):
        """Gets the metadata of this V1Role.  # noqa: E501


        :return: The metadata of this V1Role.  # noqa: E501
        :rtype: V1ObjectMeta
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this V1Role.


        :param metadata: The metadata of this V1Role.  # noqa: E501
        :type metadata: V1ObjectMeta
        """

        self._metadata = metadata

    @property
    def rules(self):
        """Gets the rules of this V1Role.  # noqa: E501

        Rules holds all the PolicyRules for this Role  # noqa: E501

        :return: The rules of this V1Role.  # noqa: E501
        :rtype: list[V1PolicyRule]
        """
        return self._rules

    @rules.setter
    def rules(self, rules):
        """Sets the rules of this V1Role.

        Rules holds all the PolicyRules for this Role  # noqa: E501

        :param rules: The rules of this V1Role.  # noqa: E501
        :type rules: list[V1PolicyRule]
        """

        self._rules = rules

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
        if not isinstance(other, V1Role):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1Role):
            return True

        return self.to_dict() != other.to_dict()
