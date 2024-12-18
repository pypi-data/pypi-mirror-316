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


class V1ProjectedVolumeSource(object):
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
        'default_mode': 'int',
        'sources': 'list[V1VolumeProjection]'
    }

    attribute_map = {
        'default_mode': 'defaultMode',
        'sources': 'sources'
    }

    def __init__(self, default_mode=None, sources=None, local_vars_configuration=None):  # noqa: E501
        """V1ProjectedVolumeSource - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default()
        self.local_vars_configuration = local_vars_configuration

        self._default_mode = None
        self._sources = None
        self.discriminator = None

        if default_mode is not None:
            self.default_mode = default_mode
        if sources is not None:
            self.sources = sources

    @property
    def default_mode(self):
        """Gets the default_mode of this V1ProjectedVolumeSource.  # noqa: E501

        defaultMode are the mode bits used to set permissions on created files by default. Must be an octal value between 0000 and 0777 or a decimal value between 0 and 511. YAML accepts both octal and decimal values, JSON requires decimal values for mode bits. Directories within the path are not affected by this setting. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set.  # noqa: E501

        :return: The default_mode of this V1ProjectedVolumeSource.  # noqa: E501
        :rtype: int
        """
        return self._default_mode

    @default_mode.setter
    def default_mode(self, default_mode):
        """Sets the default_mode of this V1ProjectedVolumeSource.

        defaultMode are the mode bits used to set permissions on created files by default. Must be an octal value between 0000 and 0777 or a decimal value between 0 and 511. YAML accepts both octal and decimal values, JSON requires decimal values for mode bits. Directories within the path are not affected by this setting. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set.  # noqa: E501

        :param default_mode: The default_mode of this V1ProjectedVolumeSource.  # noqa: E501
        :type default_mode: int
        """

        self._default_mode = default_mode

    @property
    def sources(self):
        """Gets the sources of this V1ProjectedVolumeSource.  # noqa: E501

        sources is the list of volume projections. Each entry in this list handles one source.  # noqa: E501

        :return: The sources of this V1ProjectedVolumeSource.  # noqa: E501
        :rtype: list[V1VolumeProjection]
        """
        return self._sources

    @sources.setter
    def sources(self, sources):
        """Sets the sources of this V1ProjectedVolumeSource.

        sources is the list of volume projections. Each entry in this list handles one source.  # noqa: E501

        :param sources: The sources of this V1ProjectedVolumeSource.  # noqa: E501
        :type sources: list[V1VolumeProjection]
        """

        self._sources = sources

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
        if not isinstance(other, V1ProjectedVolumeSource):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1ProjectedVolumeSource):
            return True

        return self.to_dict() != other.to_dict()
