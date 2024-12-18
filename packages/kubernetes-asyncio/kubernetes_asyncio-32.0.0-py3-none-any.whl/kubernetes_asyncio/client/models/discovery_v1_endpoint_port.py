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


class DiscoveryV1EndpointPort(object):
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
        'app_protocol': 'str',
        'name': 'str',
        'port': 'int',
        'protocol': 'str'
    }

    attribute_map = {
        'app_protocol': 'appProtocol',
        'name': 'name',
        'port': 'port',
        'protocol': 'protocol'
    }

    def __init__(self, app_protocol=None, name=None, port=None, protocol=None, local_vars_configuration=None):  # noqa: E501
        """DiscoveryV1EndpointPort - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default()
        self.local_vars_configuration = local_vars_configuration

        self._app_protocol = None
        self._name = None
        self._port = None
        self._protocol = None
        self.discriminator = None

        if app_protocol is not None:
            self.app_protocol = app_protocol
        if name is not None:
            self.name = name
        if port is not None:
            self.port = port
        if protocol is not None:
            self.protocol = protocol

    @property
    def app_protocol(self):
        """Gets the app_protocol of this DiscoveryV1EndpointPort.  # noqa: E501

        The application protocol for this port. This is used as a hint for implementations to offer richer behavior for protocols that they understand. This field follows standard Kubernetes label syntax. Valid values are either:  * Un-prefixed protocol names - reserved for IANA standard service names (as per RFC-6335 and https://www.iana.org/assignments/service-names).  * Kubernetes-defined prefixed names:   * 'kubernetes.io/h2c' - HTTP/2 prior knowledge over cleartext as described in https://www.rfc-editor.org/rfc/rfc9113.html#name-starting-http-2-with-prior-   * 'kubernetes.io/ws'  - WebSocket over cleartext as described in https://www.rfc-editor.org/rfc/rfc6455   * 'kubernetes.io/wss' - WebSocket over TLS as described in https://www.rfc-editor.org/rfc/rfc6455  * Other protocols should use implementation-defined prefixed names such as mycompany.com/my-custom-protocol.  # noqa: E501

        :return: The app_protocol of this DiscoveryV1EndpointPort.  # noqa: E501
        :rtype: str
        """
        return self._app_protocol

    @app_protocol.setter
    def app_protocol(self, app_protocol):
        """Sets the app_protocol of this DiscoveryV1EndpointPort.

        The application protocol for this port. This is used as a hint for implementations to offer richer behavior for protocols that they understand. This field follows standard Kubernetes label syntax. Valid values are either:  * Un-prefixed protocol names - reserved for IANA standard service names (as per RFC-6335 and https://www.iana.org/assignments/service-names).  * Kubernetes-defined prefixed names:   * 'kubernetes.io/h2c' - HTTP/2 prior knowledge over cleartext as described in https://www.rfc-editor.org/rfc/rfc9113.html#name-starting-http-2-with-prior-   * 'kubernetes.io/ws'  - WebSocket over cleartext as described in https://www.rfc-editor.org/rfc/rfc6455   * 'kubernetes.io/wss' - WebSocket over TLS as described in https://www.rfc-editor.org/rfc/rfc6455  * Other protocols should use implementation-defined prefixed names such as mycompany.com/my-custom-protocol.  # noqa: E501

        :param app_protocol: The app_protocol of this DiscoveryV1EndpointPort.  # noqa: E501
        :type app_protocol: str
        """

        self._app_protocol = app_protocol

    @property
    def name(self):
        """Gets the name of this DiscoveryV1EndpointPort.  # noqa: E501

        name represents the name of this port. All ports in an EndpointSlice must have a unique name. If the EndpointSlice is derived from a Kubernetes service, this corresponds to the Service.ports[].name. Name must either be an empty string or pass DNS_LABEL validation: * must be no more than 63 characters long. * must consist of lower case alphanumeric characters or '-'. * must start and end with an alphanumeric character. Default is empty string.  # noqa: E501

        :return: The name of this DiscoveryV1EndpointPort.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this DiscoveryV1EndpointPort.

        name represents the name of this port. All ports in an EndpointSlice must have a unique name. If the EndpointSlice is derived from a Kubernetes service, this corresponds to the Service.ports[].name. Name must either be an empty string or pass DNS_LABEL validation: * must be no more than 63 characters long. * must consist of lower case alphanumeric characters or '-'. * must start and end with an alphanumeric character. Default is empty string.  # noqa: E501

        :param name: The name of this DiscoveryV1EndpointPort.  # noqa: E501
        :type name: str
        """

        self._name = name

    @property
    def port(self):
        """Gets the port of this DiscoveryV1EndpointPort.  # noqa: E501

        port represents the port number of the endpoint. If this is not specified, ports are not restricted and must be interpreted in the context of the specific consumer.  # noqa: E501

        :return: The port of this DiscoveryV1EndpointPort.  # noqa: E501
        :rtype: int
        """
        return self._port

    @port.setter
    def port(self, port):
        """Sets the port of this DiscoveryV1EndpointPort.

        port represents the port number of the endpoint. If this is not specified, ports are not restricted and must be interpreted in the context of the specific consumer.  # noqa: E501

        :param port: The port of this DiscoveryV1EndpointPort.  # noqa: E501
        :type port: int
        """

        self._port = port

    @property
    def protocol(self):
        """Gets the protocol of this DiscoveryV1EndpointPort.  # noqa: E501

        protocol represents the IP protocol for this port. Must be UDP, TCP, or SCTP. Default is TCP.  # noqa: E501

        :return: The protocol of this DiscoveryV1EndpointPort.  # noqa: E501
        :rtype: str
        """
        return self._protocol

    @protocol.setter
    def protocol(self, protocol):
        """Sets the protocol of this DiscoveryV1EndpointPort.

        protocol represents the IP protocol for this port. Must be UDP, TCP, or SCTP. Default is TCP.  # noqa: E501

        :param protocol: The protocol of this DiscoveryV1EndpointPort.  # noqa: E501
        :type protocol: str
        """

        self._protocol = protocol

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
        if not isinstance(other, DiscoveryV1EndpointPort):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DiscoveryV1EndpointPort):
            return True

        return self.to_dict() != other.to_dict()
