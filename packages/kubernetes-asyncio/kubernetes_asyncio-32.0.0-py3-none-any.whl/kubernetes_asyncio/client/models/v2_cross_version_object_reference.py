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


class V2CrossVersionObjectReference(object):
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
        'name': 'str'
    }

    attribute_map = {
        'api_version': 'apiVersion',
        'kind': 'kind',
        'name': 'name'
    }

    def __init__(self, api_version=None, kind=None, name=None, local_vars_configuration=None):  # noqa: E501
        """V2CrossVersionObjectReference - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default()
        self.local_vars_configuration = local_vars_configuration

        self._api_version = None
        self._kind = None
        self._name = None
        self.discriminator = None

        if api_version is not None:
            self.api_version = api_version
        self.kind = kind
        self.name = name

    @property
    def api_version(self):
        """Gets the api_version of this V2CrossVersionObjectReference.  # noqa: E501

        apiVersion is the API version of the referent  # noqa: E501

        :return: The api_version of this V2CrossVersionObjectReference.  # noqa: E501
        :rtype: str
        """
        return self._api_version

    @api_version.setter
    def api_version(self, api_version):
        """Sets the api_version of this V2CrossVersionObjectReference.

        apiVersion is the API version of the referent  # noqa: E501

        :param api_version: The api_version of this V2CrossVersionObjectReference.  # noqa: E501
        :type api_version: str
        """

        self._api_version = api_version

    @property
    def kind(self):
        """Gets the kind of this V2CrossVersionObjectReference.  # noqa: E501

        kind is the kind of the referent; More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa: E501

        :return: The kind of this V2CrossVersionObjectReference.  # noqa: E501
        :rtype: str
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """Sets the kind of this V2CrossVersionObjectReference.

        kind is the kind of the referent; More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa: E501

        :param kind: The kind of this V2CrossVersionObjectReference.  # noqa: E501
        :type kind: str
        """
        if self.local_vars_configuration.client_side_validation and kind is None:  # noqa: E501
            raise ValueError("Invalid value for `kind`, must not be `None`")  # noqa: E501

        self._kind = kind

    @property
    def name(self):
        """Gets the name of this V2CrossVersionObjectReference.  # noqa: E501

        name is the name of the referent; More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names  # noqa: E501

        :return: The name of this V2CrossVersionObjectReference.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this V2CrossVersionObjectReference.

        name is the name of the referent; More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names  # noqa: E501

        :param name: The name of this V2CrossVersionObjectReference.  # noqa: E501
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
        if not isinstance(other, V2CrossVersionObjectReference):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V2CrossVersionObjectReference):
            return True

        return self.to_dict() != other.to_dict()
