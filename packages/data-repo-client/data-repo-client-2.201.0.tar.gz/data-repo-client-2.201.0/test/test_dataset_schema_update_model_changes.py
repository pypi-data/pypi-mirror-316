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
from data_repo_client.models.dataset_schema_update_model_changes import DatasetSchemaUpdateModelChanges  # noqa: E501
from data_repo_client.rest import ApiException

class TestDatasetSchemaUpdateModelChanges(unittest.TestCase):
    """DatasetSchemaUpdateModelChanges unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test DatasetSchemaUpdateModelChanges
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = data_repo_client.models.dataset_schema_update_model_changes.DatasetSchemaUpdateModelChanges()  # noqa: E501
        if include_optional :
            return DatasetSchemaUpdateModelChanges(
                add_tables = [
                    data_repo_client.models.table_model.TableModel(
                        name = 'a', 
                        columns = [
                            data_repo_client.models.column_model.ColumnModel(
                                name = 'a', 
                                datatype = 'string', 
                                array_of = True, 
                                required = True, )
                            ], 
                        primary_key = [
                            'a'
                            ], 
                        partition_mode = 'none', 
                        date_partition_options = data_repo_client.models.date_partition_options_model.DatePartitionOptionsModel(
                            column = 'a', ), 
                        int_partition_options = data_repo_client.models.int_partition_options_model.IntPartitionOptionsModel(
                            column = 'a', 
                            min = 56, 
                            max = 56, 
                            interval = 56, ), 
                        row_count = 56, )
                    ], 
                add_columns = [
                    data_repo_client.models.dataset_schema_column_update_model.DatasetSchemaColumnUpdateModel(
                        table_name = '0', 
                        columns = [
                            data_repo_client.models.column_model.ColumnModel(
                                name = 'a', 
                                datatype = 'string', 
                                array_of = True, 
                                required = True, )
                            ], )
                    ], 
                add_relationships = [
                    data_repo_client.models.relationship_model.RelationshipModel(
                        name = '0', 
                        from = data_repo_client.models.relationship_term_model.RelationshipTermModel(
                            table = 'a', 
                            column = 'a', ), 
                        to = data_repo_client.models.relationship_term_model.RelationshipTermModel(
                            table = 'a', 
                            column = 'a', ), )
                    ]
            )
        else :
            return DatasetSchemaUpdateModelChanges(
        )

    def testDatasetSchemaUpdateModelChanges(self):
        """Test DatasetSchemaUpdateModelChanges"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
