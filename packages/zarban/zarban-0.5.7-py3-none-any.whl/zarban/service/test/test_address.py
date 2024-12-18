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
from zarban.service.openapi_client.models.address import Address  # noqa: E501
from zarban.service.openapi_client.rest import ApiException

class TestAddress(unittest.TestCase):
    """Address unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Address
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = zarban.service.openapi_client.models.address.Address()  # noqa: E501
        if include_optional :
            return Address(
                label = 'vat', 
                address = '0x1234567890123456789012345678901234567890'
            )
        else :
            return Address(
                label = 'vat',
                address = '0x1234567890123456789012345678901234567890',
        )

    def testAddress(self):
        """Test Address"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
