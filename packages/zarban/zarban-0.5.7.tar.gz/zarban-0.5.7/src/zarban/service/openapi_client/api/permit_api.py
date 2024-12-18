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


class PermitApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_single_token_permit(self, token, user, **kwargs):  # noqa: E501
        """Get permit for single token  # noqa: E501

        Get permit for single token  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_single_token_permit(token, user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str token: Ethereum address of the token (required)
        :param str user: Ethereum address of the user (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: PermitSingle
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.get_single_token_permit_with_http_info(token, user, **kwargs)  # noqa: E501

    def get_single_token_permit_with_http_info(self, token, user, **kwargs):  # noqa: E501
        """Get permit for single token  # noqa: E501

        Get permit for single token  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_single_token_permit_with_http_info(token, user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str token: Ethereum address of the token (required)
        :param str user: Ethereum address of the user (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(PermitSingle, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'token',
            'user'
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
                    " to method get_single_token_permit" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'token' is set
        if self.api_client.client_side_validation and ('token' not in local_var_params or  # noqa: E501
                                                        local_var_params['token'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `token` when calling `get_single_token_permit`")  # noqa: E501
        # verify the required parameter 'user' is set
        if self.api_client.client_side_validation and ('user' not in local_var_params or  # noqa: E501
                                                        local_var_params['user'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `user` when calling `get_single_token_permit`")  # noqa: E501

        if self.api_client.client_side_validation and 'token' in local_var_params and not re.search(r'0x[a-fA-F0-9]{40}', local_var_params['token']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `token` when calling `get_single_token_permit`, must conform to the pattern `/0x[a-fA-F0-9]{40}/`")  # noqa: E501
        if self.api_client.client_side_validation and 'user' in local_var_params and not re.search(r'0x[a-fA-F0-9]{40}', local_var_params['user']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `user` when calling `get_single_token_permit`, must conform to the pattern `/0x[a-fA-F0-9]{40}/`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'token' in local_var_params and local_var_params['token'] is not None:  # noqa: E501
            query_params.append(('token', local_var_params['token']))  # noqa: E501
        if 'user' in local_var_params and local_var_params['user'] is not None:  # noqa: E501
            query_params.append(('user', local_var_params['user']))  # noqa: E501

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
            '/v2/permit/single', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='PermitSingle',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
