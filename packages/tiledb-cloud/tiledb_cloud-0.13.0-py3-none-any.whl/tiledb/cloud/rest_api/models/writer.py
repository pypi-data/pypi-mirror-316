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


class Writer(object):
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
        "check_coord_dups": "bool",
        "check_coord_oob": "bool",
        "dedup_coords": "bool",
        "subarray": "DomainArray",
    }

    attribute_map = {
        "check_coord_dups": "checkCoordDups",
        "check_coord_oob": "checkCoordOOB",
        "dedup_coords": "dedupCoords",
        "subarray": "subarray",
    }

    def __init__(
        self,
        check_coord_dups=None,
        check_coord_oob=None,
        dedup_coords=None,
        subarray=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """Writer - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._check_coord_dups = None
        self._check_coord_oob = None
        self._dedup_coords = None
        self._subarray = None
        self.discriminator = None

        if check_coord_dups is not None:
            self.check_coord_dups = check_coord_dups
        if check_coord_oob is not None:
            self.check_coord_oob = check_coord_oob
        if dedup_coords is not None:
            self.dedup_coords = dedup_coords
        if subarray is not None:
            self.subarray = subarray

    @property
    def check_coord_dups(self):
        """Gets the check_coord_dups of this Writer.  # noqa: E501


        :return: The check_coord_dups of this Writer.  # noqa: E501
        :rtype: bool
        """
        return self._check_coord_dups

    @check_coord_dups.setter
    def check_coord_dups(self, check_coord_dups):
        """Sets the check_coord_dups of this Writer.


        :param check_coord_dups: The check_coord_dups of this Writer.  # noqa: E501
        :type: bool
        """

        self._check_coord_dups = check_coord_dups

    @property
    def check_coord_oob(self):
        """Gets the check_coord_oob of this Writer.  # noqa: E501


        :return: The check_coord_oob of this Writer.  # noqa: E501
        :rtype: bool
        """
        return self._check_coord_oob

    @check_coord_oob.setter
    def check_coord_oob(self, check_coord_oob):
        """Sets the check_coord_oob of this Writer.


        :param check_coord_oob: The check_coord_oob of this Writer.  # noqa: E501
        :type: bool
        """

        self._check_coord_oob = check_coord_oob

    @property
    def dedup_coords(self):
        """Gets the dedup_coords of this Writer.  # noqa: E501


        :return: The dedup_coords of this Writer.  # noqa: E501
        :rtype: bool
        """
        return self._dedup_coords

    @dedup_coords.setter
    def dedup_coords(self, dedup_coords):
        """Sets the dedup_coords of this Writer.


        :param dedup_coords: The dedup_coords of this Writer.  # noqa: E501
        :type: bool
        """

        self._dedup_coords = dedup_coords

    @property
    def subarray(self):
        """Gets the subarray of this Writer.  # noqa: E501


        :return: The subarray of this Writer.  # noqa: E501
        :rtype: DomainArray
        """
        return self._subarray

    @subarray.setter
    def subarray(self, subarray):
        """Sets the subarray of this Writer.


        :param subarray: The subarray of this Writer.  # noqa: E501
        :type: DomainArray
        """

        self._subarray = subarray

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
        if not isinstance(other, Writer):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Writer):
            return True

        return self.to_dict() != other.to_dict()
