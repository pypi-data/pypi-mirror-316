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


class GroupActivityResponse(object):
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
        "activity_logs": "list[AssetActivityLog]",
        "pagination_metadata": "PaginationMetadata",
    }

    attribute_map = {
        "activity_logs": "activity_logs",
        "pagination_metadata": "pagination_metadata",
    }

    def __init__(
        self,
        activity_logs=None,
        pagination_metadata=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """GroupActivityResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._activity_logs = None
        self._pagination_metadata = None
        self.discriminator = None

        if activity_logs is not None:
            self.activity_logs = activity_logs
        if pagination_metadata is not None:
            self.pagination_metadata = pagination_metadata

    @property
    def activity_logs(self):
        """Gets the activity_logs of this GroupActivityResponse.  # noqa: E501

        Array of activity logs, including both group and array activities  # noqa: E501

        :return: The activity_logs of this GroupActivityResponse.  # noqa: E501
        :rtype: list[AssetActivityLog]
        """
        return self._activity_logs

    @activity_logs.setter
    def activity_logs(self, activity_logs):
        """Sets the activity_logs of this GroupActivityResponse.

        Array of activity logs, including both group and array activities  # noqa: E501

        :param activity_logs: The activity_logs of this GroupActivityResponse.  # noqa: E501
        :type: list[AssetActivityLog]
        """

        self._activity_logs = activity_logs

    @property
    def pagination_metadata(self):
        """Gets the pagination_metadata of this GroupActivityResponse.  # noqa: E501


        :return: The pagination_metadata of this GroupActivityResponse.  # noqa: E501
        :rtype: PaginationMetadata
        """
        return self._pagination_metadata

    @pagination_metadata.setter
    def pagination_metadata(self, pagination_metadata):
        """Sets the pagination_metadata of this GroupActivityResponse.


        :param pagination_metadata: The pagination_metadata of this GroupActivityResponse.  # noqa: E501
        :type: PaginationMetadata
        """

        self._pagination_metadata = pagination_metadata

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
        if not isinstance(other, GroupActivityResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GroupActivityResponse):
            return True

        return self.to_dict() != other.to_dict()
