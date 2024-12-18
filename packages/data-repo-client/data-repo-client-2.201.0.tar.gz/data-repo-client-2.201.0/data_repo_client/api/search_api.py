# coding: utf-8

"""
    Data Repository API

    <details><summary>This document defines the REST API for the Terra Data Repository.</summary> <p> **Status: design in progress** There are a few top-level endpoints (besides some used by swagger):  * / - generated by swagger: swagger API page that provides this documentation and a live UI for submitting REST requests  * /status - provides the operational status of the service  * /configuration - provides the basic configuration and information about the service  * /api - is the authenticated and authorized Data Repository API  * /ga4gh/drs/v1 - is a transcription of the Data Repository Service API  The API endpoints are organized by interface. Each interface is separately versioned. <p> **Notes on Naming** <p> All of the reference items are suffixed with \\\"Model\\\". Those names are used as the class names in the generated Java code. It is helpful to distinguish these model classes from other related classes, like the DAO classes and the operation classes. </details>   # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from data_repo_client.api_client import ApiClient
from data_repo_client.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class SearchApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def lookup_dataset_data_by_id(self, id, table, **kwargs):  # noqa: E501
        """lookup_dataset_data_by_id  # noqa: E501

        Retrieve data for a table in a dataset. This endpoint is deprecated, please use the POST version.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.lookup_dataset_data_by_id(id, table, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id: A UUID to used to identify an object in the repository (required)
        :param str table: Name of table to get data from (required)
        :param int offset: The number of rows to skip when retrieving the next page
        :param int limit: The number of rows to return for the data
        :param str sort: The table column to sort by
        :param SqlSortDirectionAscDefault direction: The direction to sort.
        :param str filter: A SQL WHERE clause to filter the table results.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: DatasetDataModel
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.lookup_dataset_data_by_id_with_http_info(id, table, **kwargs)  # noqa: E501

    def lookup_dataset_data_by_id_with_http_info(self, id, table, **kwargs):  # noqa: E501
        """lookup_dataset_data_by_id  # noqa: E501

        Retrieve data for a table in a dataset. This endpoint is deprecated, please use the POST version.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.lookup_dataset_data_by_id_with_http_info(id, table, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id: A UUID to used to identify an object in the repository (required)
        :param str table: Name of table to get data from (required)
        :param int offset: The number of rows to skip when retrieving the next page
        :param int limit: The number of rows to return for the data
        :param str sort: The table column to sort by
        :param SqlSortDirectionAscDefault direction: The direction to sort.
        :param str filter: A SQL WHERE clause to filter the table results.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(DatasetDataModel, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'id',
            'table',
            'offset',
            'limit',
            'sort',
            'direction',
            'filter'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method lookup_dataset_data_by_id" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id' is set
        if self.api_client.client_side_validation and ('id' not in local_var_params or  # noqa: E501
                                                        local_var_params['id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `id` when calling `lookup_dataset_data_by_id`")  # noqa: E501
        # verify the required parameter 'table' is set
        if self.api_client.client_side_validation and ('table' not in local_var_params or  # noqa: E501
                                                        local_var_params['table'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `table` when calling `lookup_dataset_data_by_id`")  # noqa: E501

        if self.api_client.client_side_validation and 'offset' in local_var_params and local_var_params['offset'] < 0:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `offset` when calling `lookup_dataset_data_by_id`, must be a value greater than or equal to `0`")  # noqa: E501
        if self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params['limit'] > 1000:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `limit` when calling `lookup_dataset_data_by_id`, must be a value less than or equal to `1000`")  # noqa: E501
        if self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params['limit'] < 1:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `limit` when calling `lookup_dataset_data_by_id`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'id' in local_var_params:
            path_params['id'] = local_var_params['id']  # noqa: E501
        if 'table' in local_var_params:
            path_params['table'] = local_var_params['table']  # noqa: E501

        query_params = []
        if 'offset' in local_var_params and local_var_params['offset'] is not None:  # noqa: E501
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if 'limit' in local_var_params and local_var_params['limit'] is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'sort' in local_var_params and local_var_params['sort'] is not None:  # noqa: E501
            query_params.append(('sort', local_var_params['sort']))  # noqa: E501
        if 'direction' in local_var_params and local_var_params['direction'] is not None:  # noqa: E501
            query_params.append(('direction', local_var_params['direction']))  # noqa: E501
        if 'filter' in local_var_params and local_var_params['filter'] is not None:  # noqa: E501
            query_params.append(('filter', local_var_params['filter']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oidc']  # noqa: E501

        return self.api_client.call_api(
            '/api/repository/v1/datasets/{id}/data/{table}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DatasetDataModel',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def lookup_snapshot_preview_by_id(self, id, table, **kwargs):  # noqa: E501
        """lookup_snapshot_preview_by_id  # noqa: E501

        Retrieve data for a table in a snapshot. This endpoint is deprecated, please use the POST version.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.lookup_snapshot_preview_by_id(id, table, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id: A UUID to used to identify an object in the repository (required)
        :param str table: Name of table to get data from (required)
        :param int offset: The number of rows to skip when retrieving the next page
        :param int limit: The number of rows to return for the data
        :param str sort: The table column to sort by
        :param SqlSortDirectionAscDefault direction: The direction to sort.
        :param str filter: A SQL WHERE clause to filter the table results.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: SnapshotPreviewModel
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.lookup_snapshot_preview_by_id_with_http_info(id, table, **kwargs)  # noqa: E501

    def lookup_snapshot_preview_by_id_with_http_info(self, id, table, **kwargs):  # noqa: E501
        """lookup_snapshot_preview_by_id  # noqa: E501

        Retrieve data for a table in a snapshot. This endpoint is deprecated, please use the POST version.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.lookup_snapshot_preview_by_id_with_http_info(id, table, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id: A UUID to used to identify an object in the repository (required)
        :param str table: Name of table to get data from (required)
        :param int offset: The number of rows to skip when retrieving the next page
        :param int limit: The number of rows to return for the data
        :param str sort: The table column to sort by
        :param SqlSortDirectionAscDefault direction: The direction to sort.
        :param str filter: A SQL WHERE clause to filter the table results.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(SnapshotPreviewModel, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'id',
            'table',
            'offset',
            'limit',
            'sort',
            'direction',
            'filter'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method lookup_snapshot_preview_by_id" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id' is set
        if self.api_client.client_side_validation and ('id' not in local_var_params or  # noqa: E501
                                                        local_var_params['id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `id` when calling `lookup_snapshot_preview_by_id`")  # noqa: E501
        # verify the required parameter 'table' is set
        if self.api_client.client_side_validation and ('table' not in local_var_params or  # noqa: E501
                                                        local_var_params['table'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `table` when calling `lookup_snapshot_preview_by_id`")  # noqa: E501

        if self.api_client.client_side_validation and 'offset' in local_var_params and local_var_params['offset'] < 0:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `offset` when calling `lookup_snapshot_preview_by_id`, must be a value greater than or equal to `0`")  # noqa: E501
        if self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params['limit'] > 1000:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `limit` when calling `lookup_snapshot_preview_by_id`, must be a value less than or equal to `1000`")  # noqa: E501
        if self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params['limit'] < 1:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `limit` when calling `lookup_snapshot_preview_by_id`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'id' in local_var_params:
            path_params['id'] = local_var_params['id']  # noqa: E501
        if 'table' in local_var_params:
            path_params['table'] = local_var_params['table']  # noqa: E501

        query_params = []
        if 'offset' in local_var_params and local_var_params['offset'] is not None:  # noqa: E501
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if 'limit' in local_var_params and local_var_params['limit'] is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'sort' in local_var_params and local_var_params['sort'] is not None:  # noqa: E501
            query_params.append(('sort', local_var_params['sort']))  # noqa: E501
        if 'direction' in local_var_params and local_var_params['direction'] is not None:  # noqa: E501
            query_params.append(('direction', local_var_params['direction']))  # noqa: E501
        if 'filter' in local_var_params and local_var_params['filter'] is not None:  # noqa: E501
            query_params.append(('filter', local_var_params['filter']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oidc']  # noqa: E501

        return self.api_client.call_api(
            '/api/repository/v1/snapshots/{id}/data/{table}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SnapshotPreviewModel',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def query_dataset_data_by_id(self, id, table, **kwargs):  # noqa: E501
        """query_dataset_data_by_id  # noqa: E501

        Retrieve data for a table in a dataset.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.query_dataset_data_by_id(id, table, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id: A UUID to used to identify an object in the repository (required)
        :param str table: Name of table to get data from (required)
        :param QueryDataRequestModel query_data_request_model: Parameters to filter results
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: DatasetDataModel
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.query_dataset_data_by_id_with_http_info(id, table, **kwargs)  # noqa: E501

    def query_dataset_data_by_id_with_http_info(self, id, table, **kwargs):  # noqa: E501
        """query_dataset_data_by_id  # noqa: E501

        Retrieve data for a table in a dataset.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.query_dataset_data_by_id_with_http_info(id, table, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id: A UUID to used to identify an object in the repository (required)
        :param str table: Name of table to get data from (required)
        :param QueryDataRequestModel query_data_request_model: Parameters to filter results
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(DatasetDataModel, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'id',
            'table',
            'query_data_request_model'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method query_dataset_data_by_id" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id' is set
        if self.api_client.client_side_validation and ('id' not in local_var_params or  # noqa: E501
                                                        local_var_params['id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `id` when calling `query_dataset_data_by_id`")  # noqa: E501
        # verify the required parameter 'table' is set
        if self.api_client.client_side_validation and ('table' not in local_var_params or  # noqa: E501
                                                        local_var_params['table'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `table` when calling `query_dataset_data_by_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in local_var_params:
            path_params['id'] = local_var_params['id']  # noqa: E501
        if 'table' in local_var_params:
            path_params['table'] = local_var_params['table']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'query_data_request_model' in local_var_params:
            body_params = local_var_params['query_data_request_model']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oidc']  # noqa: E501

        return self.api_client.call_api(
            '/api/repository/v1/datasets/{id}/data/{table}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DatasetDataModel',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def query_snapshot_data_by_id(self, id, table, **kwargs):  # noqa: E501
        """query_snapshot_data_by_id  # noqa: E501

        Retrieve data for a table in a snapshot.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.query_snapshot_data_by_id(id, table, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id: A UUID to used to identify an object in the repository (required)
        :param str table: Name of table to get data from (required)
        :param QueryDataRequestModel query_data_request_model: Parameters to filter results
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: SnapshotPreviewModel
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.query_snapshot_data_by_id_with_http_info(id, table, **kwargs)  # noqa: E501

    def query_snapshot_data_by_id_with_http_info(self, id, table, **kwargs):  # noqa: E501
        """query_snapshot_data_by_id  # noqa: E501

        Retrieve data for a table in a snapshot.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.query_snapshot_data_by_id_with_http_info(id, table, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id: A UUID to used to identify an object in the repository (required)
        :param str table: Name of table to get data from (required)
        :param QueryDataRequestModel query_data_request_model: Parameters to filter results
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(SnapshotPreviewModel, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'id',
            'table',
            'query_data_request_model'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method query_snapshot_data_by_id" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id' is set
        if self.api_client.client_side_validation and ('id' not in local_var_params or  # noqa: E501
                                                        local_var_params['id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `id` when calling `query_snapshot_data_by_id`")  # noqa: E501
        # verify the required parameter 'table' is set
        if self.api_client.client_side_validation and ('table' not in local_var_params or  # noqa: E501
                                                        local_var_params['table'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `table` when calling `query_snapshot_data_by_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in local_var_params:
            path_params['id'] = local_var_params['id']  # noqa: E501
        if 'table' in local_var_params:
            path_params['table'] = local_var_params['table']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'query_data_request_model' in local_var_params:
            body_params = local_var_params['query_data_request_model']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oidc']  # noqa: E501

        return self.api_client.call_api(
            '/api/repository/v1/snapshots/{id}/data/{table}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SnapshotPreviewModel',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
