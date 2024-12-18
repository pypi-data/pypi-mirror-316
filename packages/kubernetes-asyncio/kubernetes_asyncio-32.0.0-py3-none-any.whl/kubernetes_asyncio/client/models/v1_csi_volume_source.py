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


class V1CSIVolumeSource(object):
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
        'fs_type': 'str',
        'node_publish_secret_ref': 'V1LocalObjectReference',
        'read_only': 'bool',
        'volume_attributes': 'dict(str, str)'
    }

    attribute_map = {
        'driver': 'driver',
        'fs_type': 'fsType',
        'node_publish_secret_ref': 'nodePublishSecretRef',
        'read_only': 'readOnly',
        'volume_attributes': 'volumeAttributes'
    }

    def __init__(self, driver=None, fs_type=None, node_publish_secret_ref=None, read_only=None, volume_attributes=None, local_vars_configuration=None):  # noqa: E501
        """V1CSIVolumeSource - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default()
        self.local_vars_configuration = local_vars_configuration

        self._driver = None
        self._fs_type = None
        self._node_publish_secret_ref = None
        self._read_only = None
        self._volume_attributes = None
        self.discriminator = None

        self.driver = driver
        if fs_type is not None:
            self.fs_type = fs_type
        if node_publish_secret_ref is not None:
            self.node_publish_secret_ref = node_publish_secret_ref
        if read_only is not None:
            self.read_only = read_only
        if volume_attributes is not None:
            self.volume_attributes = volume_attributes

    @property
    def driver(self):
        """Gets the driver of this V1CSIVolumeSource.  # noqa: E501

        driver is the name of the CSI driver that handles this volume. Consult with your admin for the correct name as registered in the cluster.  # noqa: E501

        :return: The driver of this V1CSIVolumeSource.  # noqa: E501
        :rtype: str
        """
        return self._driver

    @driver.setter
    def driver(self, driver):
        """Sets the driver of this V1CSIVolumeSource.

        driver is the name of the CSI driver that handles this volume. Consult with your admin for the correct name as registered in the cluster.  # noqa: E501

        :param driver: The driver of this V1CSIVolumeSource.  # noqa: E501
        :type driver: str
        """
        if self.local_vars_configuration.client_side_validation and driver is None:  # noqa: E501
            raise ValueError("Invalid value for `driver`, must not be `None`")  # noqa: E501

        self._driver = driver

    @property
    def fs_type(self):
        """Gets the fs_type of this V1CSIVolumeSource.  # noqa: E501

        fsType to mount. Ex. \"ext4\", \"xfs\", \"ntfs\". If not provided, the empty value is passed to the associated CSI driver which will determine the default filesystem to apply.  # noqa: E501

        :return: The fs_type of this V1CSIVolumeSource.  # noqa: E501
        :rtype: str
        """
        return self._fs_type

    @fs_type.setter
    def fs_type(self, fs_type):
        """Sets the fs_type of this V1CSIVolumeSource.

        fsType to mount. Ex. \"ext4\", \"xfs\", \"ntfs\". If not provided, the empty value is passed to the associated CSI driver which will determine the default filesystem to apply.  # noqa: E501

        :param fs_type: The fs_type of this V1CSIVolumeSource.  # noqa: E501
        :type fs_type: str
        """

        self._fs_type = fs_type

    @property
    def node_publish_secret_ref(self):
        """Gets the node_publish_secret_ref of this V1CSIVolumeSource.  # noqa: E501


        :return: The node_publish_secret_ref of this V1CSIVolumeSource.  # noqa: E501
        :rtype: V1LocalObjectReference
        """
        return self._node_publish_secret_ref

    @node_publish_secret_ref.setter
    def node_publish_secret_ref(self, node_publish_secret_ref):
        """Sets the node_publish_secret_ref of this V1CSIVolumeSource.


        :param node_publish_secret_ref: The node_publish_secret_ref of this V1CSIVolumeSource.  # noqa: E501
        :type node_publish_secret_ref: V1LocalObjectReference
        """

        self._node_publish_secret_ref = node_publish_secret_ref

    @property
    def read_only(self):
        """Gets the read_only of this V1CSIVolumeSource.  # noqa: E501

        readOnly specifies a read-only configuration for the volume. Defaults to false (read/write).  # noqa: E501

        :return: The read_only of this V1CSIVolumeSource.  # noqa: E501
        :rtype: bool
        """
        return self._read_only

    @read_only.setter
    def read_only(self, read_only):
        """Sets the read_only of this V1CSIVolumeSource.

        readOnly specifies a read-only configuration for the volume. Defaults to false (read/write).  # noqa: E501

        :param read_only: The read_only of this V1CSIVolumeSource.  # noqa: E501
        :type read_only: bool
        """

        self._read_only = read_only

    @property
    def volume_attributes(self):
        """Gets the volume_attributes of this V1CSIVolumeSource.  # noqa: E501

        volumeAttributes stores driver-specific properties that are passed to the CSI driver. Consult your driver's documentation for supported values.  # noqa: E501

        :return: The volume_attributes of this V1CSIVolumeSource.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._volume_attributes

    @volume_attributes.setter
    def volume_attributes(self, volume_attributes):
        """Sets the volume_attributes of this V1CSIVolumeSource.

        volumeAttributes stores driver-specific properties that are passed to the CSI driver. Consult your driver's documentation for supported values.  # noqa: E501

        :param volume_attributes: The volume_attributes of this V1CSIVolumeSource.  # noqa: E501
        :type volume_attributes: dict(str, str)
        """

        self._volume_attributes = volume_attributes

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
        if not isinstance(other, V1CSIVolumeSource):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1CSIVolumeSource):
            return True

        return self.to_dict() != other.to_dict()
