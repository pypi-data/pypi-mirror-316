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


class SSODomainConfigResponse(object):
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
    openapi_types = {"domain_configs": "list[SSODomainConfig]"}

    attribute_map = {"domain_configs": "domain_configs"}

    def __init__(
        self, domain_configs=None, local_vars_configuration=None
    ):  # noqa: E501
        """SSODomainConfigResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._domain_configs = None
        self.discriminator = None

        if domain_configs is not None:
            self.domain_configs = domain_configs

    @property
    def domain_configs(self):
        """Gets the domain_configs of this SSODomainConfigResponse.  # noqa: E501


        :return: The domain_configs of this SSODomainConfigResponse.  # noqa: E501
        :rtype: list[SSODomainConfig]
        """
        return self._domain_configs

    @domain_configs.setter
    def domain_configs(self, domain_configs):
        """Sets the domain_configs of this SSODomainConfigResponse.


        :param domain_configs: The domain_configs of this SSODomainConfigResponse.  # noqa: E501
        :type: list[SSODomainConfig]
        """

        self._domain_configs = domain_configs

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
        if not isinstance(other, SSODomainConfigResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SSODomainConfigResponse):
            return True

        return self.to_dict() != other.to_dict()
