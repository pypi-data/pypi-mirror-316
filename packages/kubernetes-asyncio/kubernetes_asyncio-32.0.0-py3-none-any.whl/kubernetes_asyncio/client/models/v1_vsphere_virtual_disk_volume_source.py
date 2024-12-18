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


class V1VsphereVirtualDiskVolumeSource(object):
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
        'fs_type': 'str',
        'storage_policy_id': 'str',
        'storage_policy_name': 'str',
        'volume_path': 'str'
    }

    attribute_map = {
        'fs_type': 'fsType',
        'storage_policy_id': 'storagePolicyID',
        'storage_policy_name': 'storagePolicyName',
        'volume_path': 'volumePath'
    }

    def __init__(self, fs_type=None, storage_policy_id=None, storage_policy_name=None, volume_path=None, local_vars_configuration=None):  # noqa: E501
        """V1VsphereVirtualDiskVolumeSource - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default()
        self.local_vars_configuration = local_vars_configuration

        self._fs_type = None
        self._storage_policy_id = None
        self._storage_policy_name = None
        self._volume_path = None
        self.discriminator = None

        if fs_type is not None:
            self.fs_type = fs_type
        if storage_policy_id is not None:
            self.storage_policy_id = storage_policy_id
        if storage_policy_name is not None:
            self.storage_policy_name = storage_policy_name
        self.volume_path = volume_path

    @property
    def fs_type(self):
        """Gets the fs_type of this V1VsphereVirtualDiskVolumeSource.  # noqa: E501

        fsType is filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. \"ext4\", \"xfs\", \"ntfs\". Implicitly inferred to be \"ext4\" if unspecified.  # noqa: E501

        :return: The fs_type of this V1VsphereVirtualDiskVolumeSource.  # noqa: E501
        :rtype: str
        """
        return self._fs_type

    @fs_type.setter
    def fs_type(self, fs_type):
        """Sets the fs_type of this V1VsphereVirtualDiskVolumeSource.

        fsType is filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. \"ext4\", \"xfs\", \"ntfs\". Implicitly inferred to be \"ext4\" if unspecified.  # noqa: E501

        :param fs_type: The fs_type of this V1VsphereVirtualDiskVolumeSource.  # noqa: E501
        :type fs_type: str
        """

        self._fs_type = fs_type

    @property
    def storage_policy_id(self):
        """Gets the storage_policy_id of this V1VsphereVirtualDiskVolumeSource.  # noqa: E501

        storagePolicyID is the storage Policy Based Management (SPBM) profile ID associated with the StoragePolicyName.  # noqa: E501

        :return: The storage_policy_id of this V1VsphereVirtualDiskVolumeSource.  # noqa: E501
        :rtype: str
        """
        return self._storage_policy_id

    @storage_policy_id.setter
    def storage_policy_id(self, storage_policy_id):
        """Sets the storage_policy_id of this V1VsphereVirtualDiskVolumeSource.

        storagePolicyID is the storage Policy Based Management (SPBM) profile ID associated with the StoragePolicyName.  # noqa: E501

        :param storage_policy_id: The storage_policy_id of this V1VsphereVirtualDiskVolumeSource.  # noqa: E501
        :type storage_policy_id: str
        """

        self._storage_policy_id = storage_policy_id

    @property
    def storage_policy_name(self):
        """Gets the storage_policy_name of this V1VsphereVirtualDiskVolumeSource.  # noqa: E501

        storagePolicyName is the storage Policy Based Management (SPBM) profile name.  # noqa: E501

        :return: The storage_policy_name of this V1VsphereVirtualDiskVolumeSource.  # noqa: E501
        :rtype: str
        """
        return self._storage_policy_name

    @storage_policy_name.setter
    def storage_policy_name(self, storage_policy_name):
        """Sets the storage_policy_name of this V1VsphereVirtualDiskVolumeSource.

        storagePolicyName is the storage Policy Based Management (SPBM) profile name.  # noqa: E501

        :param storage_policy_name: The storage_policy_name of this V1VsphereVirtualDiskVolumeSource.  # noqa: E501
        :type storage_policy_name: str
        """

        self._storage_policy_name = storage_policy_name

    @property
    def volume_path(self):
        """Gets the volume_path of this V1VsphereVirtualDiskVolumeSource.  # noqa: E501

        volumePath is the path that identifies vSphere volume vmdk  # noqa: E501

        :return: The volume_path of this V1VsphereVirtualDiskVolumeSource.  # noqa: E501
        :rtype: str
        """
        return self._volume_path

    @volume_path.setter
    def volume_path(self, volume_path):
        """Sets the volume_path of this V1VsphereVirtualDiskVolumeSource.

        volumePath is the path that identifies vSphere volume vmdk  # noqa: E501

        :param volume_path: The volume_path of this V1VsphereVirtualDiskVolumeSource.  # noqa: E501
        :type volume_path: str
        """
        if self.local_vars_configuration.client_side_validation and volume_path is None:  # noqa: E501
            raise ValueError("Invalid value for `volume_path`, must not be `None`")  # noqa: E501

        self._volume_path = volume_path

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
        if not isinstance(other, V1VsphereVirtualDiskVolumeSource):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1VsphereVirtualDiskVolumeSource):
            return True

        return self.to_dict() != other.to_dict()
