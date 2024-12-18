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

import zarban.wallet.openapi_client
from zarban.wallet.openapi_client.api.loans_api import LoansApi  # noqa: E501
from zarban.wallet.openapi_client.rest import ApiException


class TestLoansApi(unittest.TestCase):
    """LoansApi unit test stubs"""

    def setUp(self):
        self.api = zarban.wallet.openapi_client.api.loans_api.LoansApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_loan_vault(self):
        """Test case for create_loan_vault

        Create vault  # noqa: E501
        """
        pass

    def test_estimate_loan_collateral(self):
        """Test case for estimate_loan_collateral

        Get collateral and loan amount estimation  # noqa: E501
        """
        pass

    def test_get_all_loan_plans(self):
        """Test case for get_all_loan_plans

        Get all plan loans  # noqa: E501
        """
        pass

    def test_get_loan_details(self):
        """Test case for get_loan_details

        Get loan  # noqa: E501
        """
        pass

    def test_get_user_loans(self):
        """Test case for get_user_loans

        Get user loans  # noqa: E501
        """
        pass

    def test_repay_loan(self):
        """Test case for repay_loan

        Repay Loan  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
