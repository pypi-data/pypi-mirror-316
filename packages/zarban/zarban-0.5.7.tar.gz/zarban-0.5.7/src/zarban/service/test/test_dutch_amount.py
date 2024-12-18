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
from zarban.service.openapi_client.models.dutch_amount import DutchAmount  # noqa: E501
from zarban.service.openapi_client.rest import ApiException

class TestDutchAmount(unittest.TestCase):
    """DutchAmount unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test DutchAmount
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = zarban.service.openapi_client.models.dutch_amount.DutchAmount()  # noqa: E501
        if include_optional :
            return DutchAmount(
                token = zarban.service.openapi_client.models.token.Token(
                    name = 'Zar Stablecoin', 
                    symbol = 'USD', 
                    decimals = 18, 
                    address = '0x1234567890123456789012345678901234567890', 
                    logo_uri = '/assets/logos/dai.svg', 
                    chain_id = 1, 
                    persian_name = 'زر', ), 
                start_amount = {"USD":"1.23","TMN":"45.67","ZAR":"89.01","ETH":"0.02"}, 
                end_amount = {"USD":"1.23","TMN":"45.67","ZAR":"89.01","ETH":"0.02"}, 
                recipient = 'a'
            )
        else :
            return DutchAmount(
                token = zarban.service.openapi_client.models.token.Token(
                    name = 'Zar Stablecoin', 
                    symbol = 'USD', 
                    decimals = 18, 
                    address = '0x1234567890123456789012345678901234567890', 
                    logo_uri = '/assets/logos/dai.svg', 
                    chain_id = 1, 
                    persian_name = 'زر', ),
                start_amount = {"USD":"1.23","TMN":"45.67","ZAR":"89.01","ETH":"0.02"},
                end_amount = {"USD":"1.23","TMN":"45.67","ZAR":"89.01","ETH":"0.02"},
        )

    def testDutchAmount(self):
        """Test DutchAmount"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
