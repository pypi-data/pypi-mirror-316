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
import datetime

import zarban.service.openapi_client
from zarban.service.openapi_client.models.v3_pool_in_route import V3PoolInRoute  # noqa: E501
from zarban.service.openapi_client.rest import ApiException

class TestV3PoolInRoute(unittest.TestCase):
    """V3PoolInRoute unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test V3PoolInRoute
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = zarban.service.openapi_client.models.v3_pool_in_route.V3PoolInRoute()  # noqa: E501
        if include_optional :
            return V3PoolInRoute(
                address = 'a', 
                token_in = zarban.service.openapi_client.models.token.Token(
                    name = 'Zar Stablecoin', 
                    symbol = 'USD', 
                    decimals = 18, 
                    address = '0x1234567890123456789012345678901234567890', 
                    logo_uri = '/assets/logos/dai.svg', 
                    chain_id = 1, 
                    persian_name = 'زر', ), 
                token_out = zarban.service.openapi_client.models.token.Token(
                    name = 'Zar Stablecoin', 
                    symbol = 'USD', 
                    decimals = 18, 
                    address = '0x1234567890123456789012345678901234567890', 
                    logo_uri = '/assets/logos/dai.svg', 
                    chain_id = 1, 
                    persian_name = 'زر', ), 
                fee = '0'
            )
        else :
            return V3PoolInRoute(
                address = 'a',
                token_in = zarban.service.openapi_client.models.token.Token(
                    name = 'Zar Stablecoin', 
                    symbol = 'USD', 
                    decimals = 18, 
                    address = '0x1234567890123456789012345678901234567890', 
                    logo_uri = '/assets/logos/dai.svg', 
                    chain_id = 1, 
                    persian_name = 'زر', ),
                token_out = zarban.service.openapi_client.models.token.Token(
                    name = 'Zar Stablecoin', 
                    symbol = 'USD', 
                    decimals = 18, 
                    address = '0x1234567890123456789012345678901234567890', 
                    logo_uri = '/assets/logos/dai.svg', 
                    chain_id = 1, 
                    persian_name = 'زر', ),
                fee = '0',
        )

    def testV3PoolInRoute(self):
        """Test V3PoolInRoute"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
