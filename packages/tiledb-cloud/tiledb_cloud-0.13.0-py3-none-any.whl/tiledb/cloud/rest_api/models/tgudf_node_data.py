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


class TGUDFNodeData(object):
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
        "registered_udf_name": "str",
        "executable_code": "str",
        "source_text": "str",
        "environment": "TGUDFEnvironment",
        "arguments": "list[TGUDFArgument]",
        "result_format": "ResultFormat",
    }

    attribute_map = {
        "registered_udf_name": "registered_udf_name",
        "executable_code": "executable_code",
        "source_text": "source_text",
        "environment": "environment",
        "arguments": "arguments",
        "result_format": "result_format",
    }

    def __init__(
        self,
        registered_udf_name=None,
        executable_code=None,
        source_text=None,
        environment=None,
        arguments=None,
        result_format=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """TGUDFNodeData - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._registered_udf_name = None
        self._executable_code = None
        self._source_text = None
        self._environment = None
        self._arguments = None
        self._result_format = None
        self.discriminator = None

        self.registered_udf_name = registered_udf_name
        self.executable_code = executable_code
        if source_text is not None:
            self.source_text = source_text
        if environment is not None:
            self.environment = environment
        if arguments is not None:
            self.arguments = arguments
        if result_format is not None:
            self.result_format = result_format

    @property
    def registered_udf_name(self):
        """Gets the registered_udf_name of this TGUDFNodeData.  # noqa: E501

        If set, the name of the registered UDF to execute, in the format `namespace/name`. Either this or `executable_code` should be set, but not both.   # noqa: E501

        :return: The registered_udf_name of this TGUDFNodeData.  # noqa: E501
        :rtype: str
        """
        return self._registered_udf_name

    @registered_udf_name.setter
    def registered_udf_name(self, registered_udf_name):
        """Sets the registered_udf_name of this TGUDFNodeData.

        If set, the name of the registered UDF to execute, in the format `namespace/name`. Either this or `executable_code` should be set, but not both.   # noqa: E501

        :param registered_udf_name: The registered_udf_name of this TGUDFNodeData.  # noqa: E501
        :type: str
        """

        self._registered_udf_name = registered_udf_name

    @property
    def executable_code(self):
        """Gets the executable_code of this TGUDFNodeData.  # noqa: E501

        If set, the base64 serialization of the code for this step, encoded in a language-specific format (e.g. Pickle for Python, serialization for R).   # noqa: E501

        :return: The executable_code of this TGUDFNodeData.  # noqa: E501
        :rtype: str
        """
        return self._executable_code

    @executable_code.setter
    def executable_code(self, executable_code):
        """Sets the executable_code of this TGUDFNodeData.

        If set, the base64 serialization of the code for this step, encoded in a language-specific format (e.g. Pickle for Python, serialization for R).   # noqa: E501

        :param executable_code: The executable_code of this TGUDFNodeData.  # noqa: E501
        :type: str
        """

        self._executable_code = executable_code

    @property
    def source_text(self):
        """Gets the source_text of this TGUDFNodeData.  # noqa: E501

        Optionally, the source text for the code passed in `executable_code`. *For reference only; only the code in `executable_code` is actually executed.* This will be included in activity logs and may be useful for debugging.   # noqa: E501

        :return: The source_text of this TGUDFNodeData.  # noqa: E501
        :rtype: str
        """
        return self._source_text

    @source_text.setter
    def source_text(self, source_text):
        """Sets the source_text of this TGUDFNodeData.

        Optionally, the source text for the code passed in `executable_code`. *For reference only; only the code in `executable_code` is actually executed.* This will be included in activity logs and may be useful for debugging.   # noqa: E501

        :param source_text: The source_text of this TGUDFNodeData.  # noqa: E501
        :type: str
        """

        self._source_text = source_text

    @property
    def environment(self):
        """Gets the environment of this TGUDFNodeData.  # noqa: E501


        :return: The environment of this TGUDFNodeData.  # noqa: E501
        :rtype: TGUDFEnvironment
        """
        return self._environment

    @environment.setter
    def environment(self, environment):
        """Sets the environment of this TGUDFNodeData.


        :param environment: The environment of this TGUDFNodeData.  # noqa: E501
        :type: TGUDFEnvironment
        """

        self._environment = environment

    @property
    def arguments(self):
        """Gets the arguments of this TGUDFNodeData.  # noqa: E501

        The arguments to a UDF function. This encompasses both named and positional arguments. The format is designed to provide compatibility across languages like Python which have a fairly traditional split between positional arguments and named arguments, and languages like R which has a rather unique way of specifying arguments. For Python (and most other languages), all positional arguments will come before all named arguments (if any are present):      // fn(arg1, arg2, arg3)     [       {value: arg1},       {value: arg2},       {value: arg3},     ]     // fn(arg1, arg2, n=kw1, a=kw2)     [       {value: arg1},       {value: arg2},       {name: \"n\", value: kw1},       {name: \"a\", value: kw2},     ]     // fn(kw=k1, only=k2)     [       {name: \"kw\", value: k1},       {name: \"only\", value: k2},     ]  However, in R, named and positional arguments may be intermixed freely:      // fn(arg, n=kw1, arg2)     [       {value: arg},       {name: \"n\", value: kw1},       {value: arg2},     ]   # noqa: E501

        :return: The arguments of this TGUDFNodeData.  # noqa: E501
        :rtype: list[TGUDFArgument]
        """
        return self._arguments

    @arguments.setter
    def arguments(self, arguments):
        """Sets the arguments of this TGUDFNodeData.

        The arguments to a UDF function. This encompasses both named and positional arguments. The format is designed to provide compatibility across languages like Python which have a fairly traditional split between positional arguments and named arguments, and languages like R which has a rather unique way of specifying arguments. For Python (and most other languages), all positional arguments will come before all named arguments (if any are present):      // fn(arg1, arg2, arg3)     [       {value: arg1},       {value: arg2},       {value: arg3},     ]     // fn(arg1, arg2, n=kw1, a=kw2)     [       {value: arg1},       {value: arg2},       {name: \"n\", value: kw1},       {name: \"a\", value: kw2},     ]     // fn(kw=k1, only=k2)     [       {name: \"kw\", value: k1},       {name: \"only\", value: k2},     ]  However, in R, named and positional arguments may be intermixed freely:      // fn(arg, n=kw1, arg2)     [       {value: arg},       {name: \"n\", value: kw1},       {value: arg2},     ]   # noqa: E501

        :param arguments: The arguments of this TGUDFNodeData.  # noqa: E501
        :type: list[TGUDFArgument]
        """

        self._arguments = arguments

    @property
    def result_format(self):
        """Gets the result_format of this TGUDFNodeData.  # noqa: E501


        :return: The result_format of this TGUDFNodeData.  # noqa: E501
        :rtype: ResultFormat
        """
        return self._result_format

    @result_format.setter
    def result_format(self, result_format):
        """Sets the result_format of this TGUDFNodeData.


        :param result_format: The result_format of this TGUDFNodeData.  # noqa: E501
        :type: ResultFormat
        """

        self._result_format = result_format

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
        if not isinstance(other, TGUDFNodeData):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TGUDFNodeData):
            return True

        return self.to_dict() != other.to_dict()
