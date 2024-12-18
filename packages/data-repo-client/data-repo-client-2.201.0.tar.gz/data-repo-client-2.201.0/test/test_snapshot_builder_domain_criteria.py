# coding: utf-8

"""
    Data Repository API

    <details><summary>This document defines the REST API for the Terra Data Repository.</summary> <p> **Status: design in progress** There are a few top-level endpoints (besides some used by swagger):  * / - generated by swagger: swagger API page that provides this documentation and a live UI for submitting REST requests  * /status - provides the operational status of the service  * /configuration - provides the basic configuration and information about the service  * /api - is the authenticated and authorized Data Repository API  * /ga4gh/drs/v1 - is a transcription of the Data Repository Service API  The API endpoints are organized by interface. Each interface is separately versioned. <p> **Notes on Naming** <p> All of the reference items are suffixed with \\\"Model\\\". Those names are used as the class names in the generated Java code. It is helpful to distinguish these model classes from other related classes, like the DAO classes and the operation classes. </details>   # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import data_repo_client
from data_repo_client.models.snapshot_builder_domain_criteria import SnapshotBuilderDomainCriteria  # noqa: E501
from data_repo_client.rest import ApiException

class TestSnapshotBuilderDomainCriteria(unittest.TestCase):
    """SnapshotBuilderDomainCriteria unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test SnapshotBuilderDomainCriteria
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = data_repo_client.models.snapshot_builder_domain_criteria.SnapshotBuilderDomainCriteria()  # noqa: E501
        if include_optional :
            return SnapshotBuilderDomainCriteria(
                concept_id = 56
            )
        else :
            return SnapshotBuilderDomainCriteria(
                concept_id = 56,
        )

    def testSnapshotBuilderDomainCriteria(self):
        """Test SnapshotBuilderDomainCriteria"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
