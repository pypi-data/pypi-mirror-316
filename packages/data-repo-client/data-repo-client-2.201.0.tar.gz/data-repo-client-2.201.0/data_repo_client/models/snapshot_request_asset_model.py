# coding: utf-8

"""
    Data Repository API

    <details><summary>This document defines the REST API for the Terra Data Repository.</summary> <p> **Status: design in progress** There are a few top-level endpoints (besides some used by swagger):  * / - generated by swagger: swagger API page that provides this documentation and a live UI for submitting REST requests  * /status - provides the operational status of the service  * /configuration - provides the basic configuration and information about the service  * /api - is the authenticated and authorized Data Repository API  * /ga4gh/drs/v1 - is a transcription of the Data Repository Service API  The API endpoints are organized by interface. Each interface is separately versioned. <p> **Notes on Naming** <p> All of the reference items are suffixed with \\\"Model\\\". Those names are used as the class names in the generated Java code. It is helpful to distinguish these model classes from other related classes, like the DAO classes and the operation classes. </details>   # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from data_repo_client.configuration import Configuration


class SnapshotRequestAssetModel(object):
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
        'asset_name': 'str',
        'root_values': 'list[str]'
    }

    attribute_map = {
        'asset_name': 'assetName',
        'root_values': 'rootValues'
    }

    def __init__(self, asset_name=None, root_values=None, local_vars_configuration=None):  # noqa: E501
        """SnapshotRequestAssetModel - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._asset_name = None
        self._root_values = None
        self.discriminator = None

        self.asset_name = asset_name
        self.root_values = root_values

    @property
    def asset_name(self):
        """Gets the asset_name of this SnapshotRequestAssetModel.  # noqa: E501

        Table names follow this pattern. This should be used for the name of any non-column object in the system. It enforces BigQuery naming rules except it disallows a leading underscore so we avoid collisions with any extra tables the DR adds. For table names, this is shorter than what BigQuery allows.   # noqa: E501

        :return: The asset_name of this SnapshotRequestAssetModel.  # noqa: E501
        :rtype: str
        """
        return self._asset_name

    @asset_name.setter
    def asset_name(self, asset_name):
        """Sets the asset_name of this SnapshotRequestAssetModel.

        Table names follow this pattern. This should be used for the name of any non-column object in the system. It enforces BigQuery naming rules except it disallows a leading underscore so we avoid collisions with any extra tables the DR adds. For table names, this is shorter than what BigQuery allows.   # noqa: E501

        :param asset_name: The asset_name of this SnapshotRequestAssetModel.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and asset_name is None:  # noqa: E501
            raise ValueError("Invalid value for `asset_name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                asset_name is not None and len(asset_name) > 63):
            raise ValueError("Invalid value for `asset_name`, length must be less than or equal to `63`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                asset_name is not None and len(asset_name) < 1):
            raise ValueError("Invalid value for `asset_name`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                asset_name is not None and not re.search(r'^[a-zA-Z0-9][_a-zA-Z0-9]*$', asset_name)):  # noqa: E501
            raise ValueError(r"Invalid value for `asset_name`, must be a follow pattern or equal to `/^[a-zA-Z0-9][_a-zA-Z0-9]*$/`")  # noqa: E501

        self._asset_name = asset_name

    @property
    def root_values(self):
        """Gets the root_values of this SnapshotRequestAssetModel.  # noqa: E501


        :return: The root_values of this SnapshotRequestAssetModel.  # noqa: E501
        :rtype: list[str]
        """
        return self._root_values

    @root_values.setter
    def root_values(self, root_values):
        """Sets the root_values of this SnapshotRequestAssetModel.


        :param root_values: The root_values of this SnapshotRequestAssetModel.  # noqa: E501
        :type: list[str]
        """
        if self.local_vars_configuration.client_side_validation and root_values is None:  # noqa: E501
            raise ValueError("Invalid value for `root_values`, must not be `None`")  # noqa: E501

        self._root_values = root_values

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SnapshotRequestAssetModel):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SnapshotRequestAssetModel):
            return True

        return self.to_dict() != other.to_dict()
