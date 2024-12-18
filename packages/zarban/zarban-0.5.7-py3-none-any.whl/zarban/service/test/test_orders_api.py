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
from zarban.service.openapi_client.api.orders_api import OrdersApi  # noqa: E501
from zarban.service.openapi_client.rest import ApiException


class TestOrdersApi(unittest.TestCase):
    """OrdersApi unit test stubs"""

    def setUp(self):
        self.api = zarban.service.openapi_client.api.orders_api.OrdersApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_unfilled_orders(self):
        """Test case for get_unfilled_orders

        Fetch Unfilled Orders  # noqa: E501
        """
        pass

    def test_sync_order(self):
        """Test case for sync_order

        Updates Order Entity  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
