# coding: utf-8

"""
    OpenShift API (with Kubernetes)

    OpenShift provides builds, application lifecycle, image content management, and administrative policy on top of Kubernetes. The API allows consistent management of those objects.  All API operations are authenticated via an Authorization bearer token that is provided for service accounts as a generated secret (in JWT form) or via the native OAuth endpoint located at /oauth/authorize. Core infrastructure components may use client certificates that require no authentication.  All API operations return a 'resourceVersion' string that represents the version of the object in the underlying storage. The standard LIST operation performs a snapshot read of the underlying objects, returning a resourceVersion representing a consistent version of the listed objects. The WATCH operation allows all updates to a set of objects after the provided resourceVersion to be observed by a client. By listing and beginning a watch from the returned resourceVersion, clients may observe a consistent view of the state of one or more objects. Note that WATCH always returns the update after the provided resourceVersion. Watch may be extended a limited time in the past - using etcd 2 the watch window is 1000 events (which on a large cluster may only be a few tens of seconds) so clients must explicitly handle the \"watch to old error\" by re-listing.  Objects are divided into two rough categories - those that have a lifecycle and must reflect the state of the cluster, and those that have no state. Objects with lifecycle typically have three main sections:  * 'metadata' common to all objects * a 'spec' that represents the desired state * a 'status' that represents how much of the desired state is reflected on   the cluster at the current time  Objects that have no state have 'metadata' but may lack a 'spec' or 'status' section.  Objects are divided into those that are namespace scoped (only exist inside of a namespace) and those that are cluster scoped (exist outside of a namespace). A namespace scoped resource will be deleted when the namespace is deleted and cannot be created if the namespace has not yet been created or is in the process of deletion. Cluster scoped resources are typically only accessible to admins - resources like nodes, persistent volumes, and cluster policy.  All objects have a schema that is a combination of the 'kind' and 'apiVersion' fields. This schema is additive only for any given version - no backwards incompatible changes are allowed without incrementing the apiVersion. The server will return and accept a number of standard responses that share a common schema - for instance, the common error type is 'unversioned.Status' (described below) and will be returned on any error from the API server.  The API is available in multiple serialization formats - the default is JSON (Accept: application/json and Content-Type: application/json) but clients may also use YAML (application/yaml) or the native Protobuf schema (application/vnd.kubernetes.protobuf). Note that the format of the WATCH API call is slightly different - for JSON it returns newline delimited objects while for Protobuf it returns length-delimited frames (4 bytes in network-order) that contain a 'versioned.Watch' Protobuf object.  See the OpenShift documentation at https://docs.openshift.org for more information. 

    OpenAPI spec version: v1.5.0-alpha1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class V1PodStatus(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, conditions=None, container_statuses=None, host_ip=None, message=None, phase=None, pod_ip=None, reason=None, start_time=None):
        """
        V1PodStatus - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'conditions': 'list[V1PodCondition]',
            'container_statuses': 'list[V1ContainerStatus]',
            'host_ip': 'str',
            'message': 'str',
            'phase': 'str',
            'pod_ip': 'str',
            'reason': 'str',
            'start_time': 'UnversionedTime'
        }

        self.attribute_map = {
            'conditions': 'conditions',
            'container_statuses': 'containerStatuses',
            'host_ip': 'hostIP',
            'message': 'message',
            'phase': 'phase',
            'pod_ip': 'podIP',
            'reason': 'reason',
            'start_time': 'startTime'
        }

        self._conditions = conditions
        self._container_statuses = container_statuses
        self._host_ip = host_ip
        self._message = message
        self._phase = phase
        self._pod_ip = pod_ip
        self._reason = reason
        self._start_time = start_time

    @property
    def conditions(self):
        """
        Gets the conditions of this V1PodStatus.
        Current service state of pod. More info: http://kubernetes.io/docs/user-guide/pod-states#pod-conditions

        :return: The conditions of this V1PodStatus.
        :rtype: list[V1PodCondition]
        """
        return self._conditions

    @conditions.setter
    def conditions(self, conditions):
        """
        Sets the conditions of this V1PodStatus.
        Current service state of pod. More info: http://kubernetes.io/docs/user-guide/pod-states#pod-conditions

        :param conditions: The conditions of this V1PodStatus.
        :type: list[V1PodCondition]
        """

        self._conditions = conditions

    @property
    def container_statuses(self):
        """
        Gets the container_statuses of this V1PodStatus.
        The list has one entry per container in the manifest. Each entry is currently the output of `docker inspect`. More info: http://kubernetes.io/docs/user-guide/pod-states#container-statuses

        :return: The container_statuses of this V1PodStatus.
        :rtype: list[V1ContainerStatus]
        """
        return self._container_statuses

    @container_statuses.setter
    def container_statuses(self, container_statuses):
        """
        Sets the container_statuses of this V1PodStatus.
        The list has one entry per container in the manifest. Each entry is currently the output of `docker inspect`. More info: http://kubernetes.io/docs/user-guide/pod-states#container-statuses

        :param container_statuses: The container_statuses of this V1PodStatus.
        :type: list[V1ContainerStatus]
        """

        self._container_statuses = container_statuses

    @property
    def host_ip(self):
        """
        Gets the host_ip of this V1PodStatus.
        IP address of the host to which the pod is assigned. Empty if not yet scheduled.

        :return: The host_ip of this V1PodStatus.
        :rtype: str
        """
        return self._host_ip

    @host_ip.setter
    def host_ip(self, host_ip):
        """
        Sets the host_ip of this V1PodStatus.
        IP address of the host to which the pod is assigned. Empty if not yet scheduled.

        :param host_ip: The host_ip of this V1PodStatus.
        :type: str
        """

        self._host_ip = host_ip

    @property
    def message(self):
        """
        Gets the message of this V1PodStatus.
        A human readable message indicating details about why the pod is in this condition.

        :return: The message of this V1PodStatus.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message of this V1PodStatus.
        A human readable message indicating details about why the pod is in this condition.

        :param message: The message of this V1PodStatus.
        :type: str
        """

        self._message = message

    @property
    def phase(self):
        """
        Gets the phase of this V1PodStatus.
        Current condition of the pod. More info: http://kubernetes.io/docs/user-guide/pod-states#pod-phase

        :return: The phase of this V1PodStatus.
        :rtype: str
        """
        return self._phase

    @phase.setter
    def phase(self, phase):
        """
        Sets the phase of this V1PodStatus.
        Current condition of the pod. More info: http://kubernetes.io/docs/user-guide/pod-states#pod-phase

        :param phase: The phase of this V1PodStatus.
        :type: str
        """

        self._phase = phase

    @property
    def pod_ip(self):
        """
        Gets the pod_ip of this V1PodStatus.
        IP address allocated to the pod. Routable at least within the cluster. Empty if not yet allocated.

        :return: The pod_ip of this V1PodStatus.
        :rtype: str
        """
        return self._pod_ip

    @pod_ip.setter
    def pod_ip(self, pod_ip):
        """
        Sets the pod_ip of this V1PodStatus.
        IP address allocated to the pod. Routable at least within the cluster. Empty if not yet allocated.

        :param pod_ip: The pod_ip of this V1PodStatus.
        :type: str
        """

        self._pod_ip = pod_ip

    @property
    def reason(self):
        """
        Gets the reason of this V1PodStatus.
        A brief CamelCase message indicating details about why the pod is in this state. e.g. 'OutOfDisk'

        :return: The reason of this V1PodStatus.
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """
        Sets the reason of this V1PodStatus.
        A brief CamelCase message indicating details about why the pod is in this state. e.g. 'OutOfDisk'

        :param reason: The reason of this V1PodStatus.
        :type: str
        """

        self._reason = reason

    @property
    def start_time(self):
        """
        Gets the start_time of this V1PodStatus.
        RFC 3339 date and time at which the object was acknowledged by the Kubelet. This is before the Kubelet pulled the container image(s) for the pod.

        :return: The start_time of this V1PodStatus.
        :rtype: UnversionedTime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """
        Sets the start_time of this V1PodStatus.
        RFC 3339 date and time at which the object was acknowledged by the Kubelet. This is before the Kubelet pulled the container image(s) for the pod.

        :param start_time: The start_time of this V1PodStatus.
        :type: UnversionedTime
        """

        self._start_time = start_time

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
