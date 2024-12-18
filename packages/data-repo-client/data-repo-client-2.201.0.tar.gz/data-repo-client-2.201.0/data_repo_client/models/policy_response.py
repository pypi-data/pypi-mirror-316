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


class PolicyResponse(object):
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
        'policies': 'list[PolicyModel]',
        'auth_domain': 'list[str]',
        'workspaces': 'list[WorkspacePolicyModel]',
        'inaccessible_workspaces': 'list[InaccessibleWorkspacePolicyModel]'
    }

    attribute_map = {
        'policies': 'policies',
        'auth_domain': 'authDomain',
        'workspaces': 'workspaces',
        'inaccessible_workspaces': 'inaccessibleWorkspaces'
    }

    def __init__(self, policies=None, auth_domain=None, workspaces=None, inaccessible_workspaces=None, local_vars_configuration=None):  # noqa: E501
        """PolicyResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._policies = None
        self._auth_domain = None
        self._workspaces = None
        self._inaccessible_workspaces = None
        self.discriminator = None

        if policies is not None:
            self.policies = policies
        if auth_domain is not None:
            self.auth_domain = auth_domain
        if workspaces is not None:
            self.workspaces = workspaces
        if inaccessible_workspaces is not None:
            self.inaccessible_workspaces = inaccessible_workspaces

    @property
    def policies(self):
        """Gets the policies of this PolicyResponse.  # noqa: E501


        :return: The policies of this PolicyResponse.  # noqa: E501
        :rtype: list[PolicyModel]
        """
        return self._policies

    @policies.setter
    def policies(self, policies):
        """Sets the policies of this PolicyResponse.


        :param policies: The policies of this PolicyResponse.  # noqa: E501
        :type: list[PolicyModel]
        """

        self._policies = policies

    @property
    def auth_domain(self):
        """Gets the auth_domain of this PolicyResponse.  # noqa: E501


        :return: The auth_domain of this PolicyResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._auth_domain

    @auth_domain.setter
    def auth_domain(self, auth_domain):
        """Sets the auth_domain of this PolicyResponse.


        :param auth_domain: The auth_domain of this PolicyResponse.  # noqa: E501
        :type: list[str]
        """

        self._auth_domain = auth_domain

    @property
    def workspaces(self):
        """Gets the workspaces of this PolicyResponse.  # noqa: E501


        :return: The workspaces of this PolicyResponse.  # noqa: E501
        :rtype: list[WorkspacePolicyModel]
        """
        return self._workspaces

    @workspaces.setter
    def workspaces(self, workspaces):
        """Sets the workspaces of this PolicyResponse.


        :param workspaces: The workspaces of this PolicyResponse.  # noqa: E501
        :type: list[WorkspacePolicyModel]
        """

        self._workspaces = workspaces

    @property
    def inaccessible_workspaces(self):
        """Gets the inaccessible_workspaces of this PolicyResponse.  # noqa: E501


        :return: The inaccessible_workspaces of this PolicyResponse.  # noqa: E501
        :rtype: list[InaccessibleWorkspacePolicyModel]
        """
        return self._inaccessible_workspaces

    @inaccessible_workspaces.setter
    def inaccessible_workspaces(self, inaccessible_workspaces):
        """Sets the inaccessible_workspaces of this PolicyResponse.


        :param inaccessible_workspaces: The inaccessible_workspaces of this PolicyResponse.  # noqa: E501
        :type: list[InaccessibleWorkspacePolicyModel]
        """

        self._inaccessible_workspaces = inaccessible_workspaces

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
        if not isinstance(other, PolicyResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PolicyResponse):
            return True

        return self.to_dict() != other.to_dict()
