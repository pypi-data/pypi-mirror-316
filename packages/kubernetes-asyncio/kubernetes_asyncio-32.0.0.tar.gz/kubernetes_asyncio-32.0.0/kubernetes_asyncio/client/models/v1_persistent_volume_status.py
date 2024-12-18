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


class V1PersistentVolumeStatus(object):
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
        'last_phase_transition_time': 'datetime',
        'message': 'str',
        'phase': 'str',
        'reason': 'str'
    }

    attribute_map = {
        'last_phase_transition_time': 'lastPhaseTransitionTime',
        'message': 'message',
        'phase': 'phase',
        'reason': 'reason'
    }

    def __init__(self, last_phase_transition_time=None, message=None, phase=None, reason=None, local_vars_configuration=None):  # noqa: E501
        """V1PersistentVolumeStatus - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default()
        self.local_vars_configuration = local_vars_configuration

        self._last_phase_transition_time = None
        self._message = None
        self._phase = None
        self._reason = None
        self.discriminator = None

        if last_phase_transition_time is not None:
            self.last_phase_transition_time = last_phase_transition_time
        if message is not None:
            self.message = message
        if phase is not None:
            self.phase = phase
        if reason is not None:
            self.reason = reason

    @property
    def last_phase_transition_time(self):
        """Gets the last_phase_transition_time of this V1PersistentVolumeStatus.  # noqa: E501

        lastPhaseTransitionTime is the time the phase transitioned from one to another and automatically resets to current time everytime a volume phase transitions.  # noqa: E501

        :return: The last_phase_transition_time of this V1PersistentVolumeStatus.  # noqa: E501
        :rtype: datetime
        """
        return self._last_phase_transition_time

    @last_phase_transition_time.setter
    def last_phase_transition_time(self, last_phase_transition_time):
        """Sets the last_phase_transition_time of this V1PersistentVolumeStatus.

        lastPhaseTransitionTime is the time the phase transitioned from one to another and automatically resets to current time everytime a volume phase transitions.  # noqa: E501

        :param last_phase_transition_time: The last_phase_transition_time of this V1PersistentVolumeStatus.  # noqa: E501
        :type last_phase_transition_time: datetime
        """

        self._last_phase_transition_time = last_phase_transition_time

    @property
    def message(self):
        """Gets the message of this V1PersistentVolumeStatus.  # noqa: E501

        message is a human-readable message indicating details about why the volume is in this state.  # noqa: E501

        :return: The message of this V1PersistentVolumeStatus.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this V1PersistentVolumeStatus.

        message is a human-readable message indicating details about why the volume is in this state.  # noqa: E501

        :param message: The message of this V1PersistentVolumeStatus.  # noqa: E501
        :type message: str
        """

        self._message = message

    @property
    def phase(self):
        """Gets the phase of this V1PersistentVolumeStatus.  # noqa: E501

        phase indicates if a volume is available, bound to a claim, or released by a claim. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#phase  # noqa: E501

        :return: The phase of this V1PersistentVolumeStatus.  # noqa: E501
        :rtype: str
        """
        return self._phase

    @phase.setter
    def phase(self, phase):
        """Sets the phase of this V1PersistentVolumeStatus.

        phase indicates if a volume is available, bound to a claim, or released by a claim. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#phase  # noqa: E501

        :param phase: The phase of this V1PersistentVolumeStatus.  # noqa: E501
        :type phase: str
        """

        self._phase = phase

    @property
    def reason(self):
        """Gets the reason of this V1PersistentVolumeStatus.  # noqa: E501

        reason is a brief CamelCase string that describes any failure and is meant for machine parsing and tidy display in the CLI.  # noqa: E501

        :return: The reason of this V1PersistentVolumeStatus.  # noqa: E501
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """Sets the reason of this V1PersistentVolumeStatus.

        reason is a brief CamelCase string that describes any failure and is meant for machine parsing and tidy display in the CLI.  # noqa: E501

        :param reason: The reason of this V1PersistentVolumeStatus.  # noqa: E501
        :type reason: str
        """

        self._reason = reason

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
        if not isinstance(other, V1PersistentVolumeStatus):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1PersistentVolumeStatus):
            return True

        return self.to_dict() != other.to_dict()
