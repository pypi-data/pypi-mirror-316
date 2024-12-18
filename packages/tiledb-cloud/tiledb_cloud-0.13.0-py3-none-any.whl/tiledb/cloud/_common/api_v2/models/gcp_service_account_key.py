# coding: utf-8

"""
    Tiledb Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 1.4.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from tiledb.cloud._common.api_v2.configuration import Configuration


class GCPServiceAccountKey(object):
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
    openapi_types = {"account_id": "str", "key_id": "str", "key_text": "str"}

    attribute_map = {
        "account_id": "account_id",
        "key_id": "key_id",
        "key_text": "key_text",
    }

    def __init__(
        self, account_id=None, key_id=None, key_text=None, local_vars_configuration=None
    ):  # noqa: E501
        """GCPServiceAccountKey - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._account_id = None
        self._key_id = None
        self._key_text = None
        self.discriminator = None

        if account_id is not None:
            self.account_id = account_id
        if key_id is not None:
            self.key_id = key_id
        if key_text is not None:
            self.key_text = key_text

    @property
    def account_id(self):
        """Gets the account_id of this GCPServiceAccountKey.  # noqa: E501

        The ID of the service account (i.e., its email address).  This is ignored when uploading key information, and is only provided by the server when downloading metadata about an existing key.   # noqa: E501

        :return: The account_id of this GCPServiceAccountKey.  # noqa: E501
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """Sets the account_id of this GCPServiceAccountKey.

        The ID of the service account (i.e., its email address).  This is ignored when uploading key information, and is only provided by the server when downloading metadata about an existing key.   # noqa: E501

        :param account_id: The account_id of this GCPServiceAccountKey.  # noqa: E501
        :type: str
        """

        self._account_id = account_id

    @property
    def key_id(self):
        """Gets the key_id of this GCPServiceAccountKey.  # noqa: E501

        The ID of the particular key. This identifies it among other keys issued for this service account.  This is ignored when uploading key information, and is only provided by the server when downloading metadata about an existing key.   # noqa: E501

        :return: The key_id of this GCPServiceAccountKey.  # noqa: E501
        :rtype: str
        """
        return self._key_id

    @key_id.setter
    def key_id(self, key_id):
        """Sets the key_id of this GCPServiceAccountKey.

        The ID of the particular key. This identifies it among other keys issued for this service account.  This is ignored when uploading key information, and is only provided by the server when downloading metadata about an existing key.   # noqa: E501

        :param key_id: The key_id of this GCPServiceAccountKey.  # noqa: E501
        :type: str
        """

        self._key_id = key_id

    @property
    def key_text(self):
        """Gets the key_text of this GCPServiceAccountKey.  # noqa: E501

        The full file provided by Google Cloud. This is usually in the form of a JSON document, but TileDB Cloud treats it as opaque (except to attempt to extract the service account ID and the key ID).   # noqa: E501

        :return: The key_text of this GCPServiceAccountKey.  # noqa: E501
        :rtype: str
        """
        return self._key_text

    @key_text.setter
    def key_text(self, key_text):
        """Sets the key_text of this GCPServiceAccountKey.

        The full file provided by Google Cloud. This is usually in the form of a JSON document, but TileDB Cloud treats it as opaque (except to attempt to extract the service account ID and the key ID).   # noqa: E501

        :param key_text: The key_text of this GCPServiceAccountKey.  # noqa: E501
        :type: str
        """

        self._key_text = key_text

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
        if not isinstance(other, GCPServiceAccountKey):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GCPServiceAccountKey):
            return True

        return self.to_dict() != other.to_dict()
