# coding: utf-8

"""
    Zarban API

    API for Zarban services.  # noqa: E501

    The version of the OpenAPI document: 2.0.0
    Contact: info@zarban.io
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from zarban.service.openapi_client.api_client import ApiClient
from zarban.service.openapi_client.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class BorrowsApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_user_borrows(self, **kwargs):  # noqa: E501
        """Get user borrows of lendingpool  # noqa: E501

        Get user borrows of lendingpool  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_user_borrows(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str user: Ethereum address of the user
        :param str reserve: Ethereum address of the reserve
        :param int cursor: Cursor for pagination
        :param int limit: Limit the number of deposits returned (default is 50)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserBorrowsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.get_user_borrows_with_http_info(**kwargs)  # noqa: E501

    def get_user_borrows_with_http_info(self, **kwargs):  # noqa: E501
        """Get user borrows of lendingpool  # noqa: E501

        Get user borrows of lendingpool  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_user_borrows_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str user: Ethereum address of the user
        :param str reserve: Ethereum address of the reserve
        :param int cursor: Cursor for pagination
        :param int limit: Limit the number of deposits returned (default is 50)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(UserBorrowsResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'user',
            'reserve',
            'cursor',
            'limit'
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
                    " to method get_user_borrows" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        if self.api_client.client_side_validation and 'user' in local_var_params and not re.search(r'0x[a-fA-F0-9]{40}', local_var_params['user']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `user` when calling `get_user_borrows`, must conform to the pattern `/0x[a-fA-F0-9]{40}/`")  # noqa: E501
        if self.api_client.client_side_validation and 'reserve' in local_var_params and not re.search(r'0x[a-fA-F0-9]{40}', local_var_params['reserve']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `reserve` when calling `get_user_borrows`, must conform to the pattern `/0x[a-fA-F0-9]{40}/`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'user' in local_var_params and local_var_params['user'] is not None:  # noqa: E501
            query_params.append(('user', local_var_params['user']))  # noqa: E501
        if 'reserve' in local_var_params and local_var_params['reserve'] is not None:  # noqa: E501
            query_params.append(('reserve', local_var_params['reserve']))  # noqa: E501
        if 'cursor' in local_var_params and local_var_params['cursor'] is not None:  # noqa: E501
            query_params.append(('cursor', local_var_params['cursor']))  # noqa: E501
        if 'limit' in local_var_params and local_var_params['limit'] is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/v2/lendingpool/borrows', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserBorrowsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
