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


class Enumeration(object):
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
        "name": "str",
        "path_name": "str",
        "type": "str",
        "cell_val_num": "int",
        "ordered": "bool",
        "data": "list[int]",
        "offsets": "list[int]",
    }

    attribute_map = {
        "name": "name",
        "path_name": "path_name",
        "type": "type",
        "cell_val_num": "cell_val_num",
        "ordered": "ordered",
        "data": "data",
        "offsets": "offsets",
    }

    def __init__(
        self,
        name=None,
        path_name=None,
        type=None,
        cell_val_num=None,
        ordered=None,
        data=None,
        offsets=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """Enumeration - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._path_name = None
        self._type = None
        self._cell_val_num = None
        self._ordered = None
        self._data = None
        self._offsets = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if path_name is not None:
            self.path_name = path_name
        if type is not None:
            self.type = type
        if cell_val_num is not None:
            self.cell_val_num = cell_val_num
        if ordered is not None:
            self.ordered = ordered
        if data is not None:
            self.data = data
        if offsets is not None:
            self.offsets = offsets

    @property
    def name(self):
        """Gets the name of this Enumeration.  # noqa: E501


        :return: The name of this Enumeration.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Enumeration.


        :param name: The name of this Enumeration.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def path_name(self):
        """Gets the path_name of this Enumeration.  # noqa: E501


        :return: The path_name of this Enumeration.  # noqa: E501
        :rtype: str
        """
        return self._path_name

    @path_name.setter
    def path_name(self, path_name):
        """Sets the path_name of this Enumeration.


        :param path_name: The path_name of this Enumeration.  # noqa: E501
        :type: str
        """

        self._path_name = path_name

    @property
    def type(self):
        """Gets the type of this Enumeration.  # noqa: E501


        :return: The type of this Enumeration.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Enumeration.


        :param type: The type of this Enumeration.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def cell_val_num(self):
        """Gets the cell_val_num of this Enumeration.  # noqa: E501


        :return: The cell_val_num of this Enumeration.  # noqa: E501
        :rtype: int
        """
        return self._cell_val_num

    @cell_val_num.setter
    def cell_val_num(self, cell_val_num):
        """Sets the cell_val_num of this Enumeration.


        :param cell_val_num: The cell_val_num of this Enumeration.  # noqa: E501
        :type: int
        """

        self._cell_val_num = cell_val_num

    @property
    def ordered(self):
        """Gets the ordered of this Enumeration.  # noqa: E501


        :return: The ordered of this Enumeration.  # noqa: E501
        :rtype: bool
        """
        return self._ordered

    @ordered.setter
    def ordered(self, ordered):
        """Sets the ordered of this Enumeration.


        :param ordered: The ordered of this Enumeration.  # noqa: E501
        :type: bool
        """

        self._ordered = ordered

    @property
    def data(self):
        """Gets the data of this Enumeration.  # noqa: E501


        :return: The data of this Enumeration.  # noqa: E501
        :rtype: list[int]
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this Enumeration.


        :param data: The data of this Enumeration.  # noqa: E501
        :type: list[int]
        """

        self._data = data

    @property
    def offsets(self):
        """Gets the offsets of this Enumeration.  # noqa: E501


        :return: The offsets of this Enumeration.  # noqa: E501
        :rtype: list[int]
        """
        return self._offsets

    @offsets.setter
    def offsets(self, offsets):
        """Sets the offsets of this Enumeration.


        :param offsets: The offsets of this Enumeration.  # noqa: E501
        :type: list[int]
        """

        self._offsets = offsets

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
        if not isinstance(other, Enumeration):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Enumeration):
            return True

        return self.to_dict() != other.to_dict()
