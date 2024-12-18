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


class SubarrayPartitionerState(object):
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
        "start": "int",
        "end": "int",
        "single_range": "list[Subarray]",
        "multi_range": "list[Subarray]",
    }

    attribute_map = {
        "start": "start",
        "end": "end",
        "single_range": "singleRange",
        "multi_range": "multiRange",
    }

    def __init__(
        self,
        start=None,
        end=None,
        single_range=None,
        multi_range=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """SubarrayPartitionerState - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._start = None
        self._end = None
        self._single_range = None
        self._multi_range = None
        self.discriminator = None

        if start is not None:
            self.start = start
        if end is not None:
            self.end = end
        if single_range is not None:
            self.single_range = single_range
        if multi_range is not None:
            self.multi_range = multi_range

    @property
    def start(self):
        """Gets the start of this SubarrayPartitionerState.  # noqa: E501

        State start  # noqa: E501

        :return: The start of this SubarrayPartitionerState.  # noqa: E501
        :rtype: int
        """
        return self._start

    @start.setter
    def start(self, start):
        """Sets the start of this SubarrayPartitionerState.

        State start  # noqa: E501

        :param start: The start of this SubarrayPartitionerState.  # noqa: E501
        :type: int
        """

        self._start = start

    @property
    def end(self):
        """Gets the end of this SubarrayPartitionerState.  # noqa: E501

        State end  # noqa: E501

        :return: The end of this SubarrayPartitionerState.  # noqa: E501
        :rtype: int
        """
        return self._end

    @end.setter
    def end(self, end):
        """Sets the end of this SubarrayPartitionerState.

        State end  # noqa: E501

        :param end: The end of this SubarrayPartitionerState.  # noqa: E501
        :type: int
        """

        self._end = end

    @property
    def single_range(self):
        """Gets the single_range of this SubarrayPartitionerState.  # noqa: E501

        State singleRange  # noqa: E501

        :return: The single_range of this SubarrayPartitionerState.  # noqa: E501
        :rtype: list[Subarray]
        """
        return self._single_range

    @single_range.setter
    def single_range(self, single_range):
        """Sets the single_range of this SubarrayPartitionerState.

        State singleRange  # noqa: E501

        :param single_range: The single_range of this SubarrayPartitionerState.  # noqa: E501
        :type: list[Subarray]
        """

        self._single_range = single_range

    @property
    def multi_range(self):
        """Gets the multi_range of this SubarrayPartitionerState.  # noqa: E501

        State multiRange  # noqa: E501

        :return: The multi_range of this SubarrayPartitionerState.  # noqa: E501
        :rtype: list[Subarray]
        """
        return self._multi_range

    @multi_range.setter
    def multi_range(self, multi_range):
        """Sets the multi_range of this SubarrayPartitionerState.

        State multiRange  # noqa: E501

        :param multi_range: The multi_range of this SubarrayPartitionerState.  # noqa: E501
        :type: list[Subarray]
        """

        self._multi_range = multi_range

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
        if not isinstance(other, SubarrayPartitionerState):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SubarrayPartitionerState):
            return True

        return self.to_dict() != other.to_dict()
