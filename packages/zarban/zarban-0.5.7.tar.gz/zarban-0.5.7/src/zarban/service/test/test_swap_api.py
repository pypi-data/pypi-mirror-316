# coding: utf-8

"""
    Zarban API

    API for Zarban services.  # noqa: E501

    The version of the OpenAPI document: 2.0.0
    Contact: info@zarban.io
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import zarban.service.openapi_client
from zarban.service.openapi_client.api.swap_api import SwapApi  # noqa: E501
from zarban.service.openapi_client.rest import ApiException


class TestSwapApi(unittest.TestCase):
    """SwapApi unit test stubs"""

    def setUp(self):
        self.api = zarban.service.openapi_client.api.swap_api.SwapApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_swap_quote(self):
        """Test case for get_swap_quote

        Get a quote for a swap  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
