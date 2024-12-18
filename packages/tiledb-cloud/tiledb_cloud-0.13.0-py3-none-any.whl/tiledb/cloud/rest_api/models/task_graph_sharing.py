# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.17.51
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from tiledb.cloud.rest_api.configuration import Configuration


class TaskGraphSharing(object):
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
        "actions": "list[TaskGraphActions]",
        "namespace": "str",
        "namespace_type": "str",
    }

    attribute_map = {
        "actions": "actions",
        "namespace": "namespace",
        "namespace_type": "namespace_type",
    }

    def __init__(
        self,
        actions=None,
        namespace=None,
        namespace_type=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """TaskGraphSharing - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._actions = None
        self._namespace = None
        self._namespace_type = None
        self.discriminator = None

        if actions is not None:
            self.actions = actions
        if namespace is not None:
            self.namespace = namespace
        if namespace_type is not None:
            self.namespace_type = namespace_type

    @property
    def actions(self):
        """Gets the actions of this TaskGraphSharing.  # noqa: E501

        List of permitted actions  # noqa: E501

        :return: The actions of this TaskGraphSharing.  # noqa: E501
        :rtype: list[TaskGraphActions]
        """
        return self._actions

    @actions.setter
    def actions(self, actions):
        """Sets the actions of this TaskGraphSharing.

        List of permitted actions  # noqa: E501

        :param actions: The actions of this TaskGraphSharing.  # noqa: E501
        :type: list[TaskGraphActions]
        """

        self._actions = actions

    @property
    def namespace(self):
        """Gets the namespace of this TaskGraphSharing.  # noqa: E501

        namespace being granted array access can be a user or organization  # noqa: E501

        :return: The namespace of this TaskGraphSharing.  # noqa: E501
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this TaskGraphSharing.

        namespace being granted array access can be a user or organization  # noqa: E501

        :param namespace: The namespace of this TaskGraphSharing.  # noqa: E501
        :type: str
        """

        self._namespace = namespace

    @property
    def namespace_type(self):
        """Gets the namespace_type of this TaskGraphSharing.  # noqa: E501

        details on if the namespace is a organization or user  # noqa: E501

        :return: The namespace_type of this TaskGraphSharing.  # noqa: E501
        :rtype: str
        """
        return self._namespace_type

    @namespace_type.setter
    def namespace_type(self, namespace_type):
        """Sets the namespace_type of this TaskGraphSharing.

        details on if the namespace is a organization or user  # noqa: E501

        :param namespace_type: The namespace_type of this TaskGraphSharing.  # noqa: E501
        :type: str
        """

        self._namespace_type = namespace_type

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, TaskGraphSharing):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TaskGraphSharing):
            return True

        return self.to_dict() != other.to_dict()
