# coding: utf-8

"""
    Zarban Wallet API

    API for Zarban wallet services.  # noqa: E501

    The version of the OpenAPI document: 2.0.0
    Contact: info@zarban.io
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import zarban.wallet.openapi_client
from zarban.wallet.openapi_client.models.sign_up_request import SignUpRequest  # noqa: E501
from zarban.wallet.openapi_client.rest import ApiException

class TestSignUpRequest(unittest.TestCase):
    """SignUpRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test SignUpRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = zarban.wallet.openapi_client.models.sign_up_request.SignUpRequest()  # noqa: E501
        if include_optional :
            return SignUpRequest(
                email = 'example@domain.com', 
                password = 'password'
            )
        else :
            return SignUpRequest(
                email = 'example@domain.com',
                password = 'password',
        )

    def testSignUpRequest(self):
        """Test SignUpRequest"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
