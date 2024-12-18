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


class StorageLocation(object):
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
    openapi_types = {"path": "str", "credentials_name": "str"}

    attribute_map = {"path": "path", "credentials_name": "credentials_name"}

    def __init__(
        self, path=None, credentials_name=None, local_vars_configuration=None
    ):  # noqa: E501
        """StorageLocation - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._path = None
        self._credentials_name = None
        self.discriminator = None

        self.path = path
        self.credentials_name = credentials_name

    @property
    def path(self):
        """Gets the path of this StorageLocation.  # noqa: E501

        The path to store this asset type. If unset, a suffix of the user's `default_s3_path` is used. When updating, explicitly set to `\"\"`, the empty string, to clear this path; leaving it `null` (or absent) will leave the path unchanged.   # noqa: E501

        :return: The path of this StorageLocation.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this StorageLocation.

        The path to store this asset type. If unset, a suffix of the user's `default_s3_path` is used. When updating, explicitly set to `\"\"`, the empty string, to clear this path; leaving it `null` (or absent) will leave the path unchanged.   # noqa: E501

        :param path: The path of this StorageLocation.  # noqa: E501
        :type: str
        """

        self._path = path

    @property
    def credentials_name(self):
        """Gets the credentials_name of this StorageLocation.  # noqa: E501

        The name of the credentials used to acess this storage path. If unset, the `default_s3_path_credentials_name` is used. When updating, explicitly set to `\"\"`, the empty string, to clear this name; leaving it `null` (or absent) will leave the name unchanged.   # noqa: E501

        :return: The credentials_name of this StorageLocation.  # noqa: E501
        :rtype: str
        """
        return self._credentials_name

    @credentials_name.setter
    def credentials_name(self, credentials_name):
        """Sets the credentials_name of this StorageLocation.

        The name of the credentials used to acess this storage path. If unset, the `default_s3_path_credentials_name` is used. When updating, explicitly set to `\"\"`, the empty string, to clear this name; leaving it `null` (or absent) will leave the name unchanged.   # noqa: E501

        :param credentials_name: The credentials_name of this StorageLocation.  # noqa: E501
        :type: str
        """

        self._credentials_name = credentials_name

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
        if not isinstance(other, StorageLocation):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, StorageLocation):
            return True

        return self.to_dict() != other.to_dict()
