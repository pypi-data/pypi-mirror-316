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
from zarban.service.openapi_client.models.stats import Stats  # noqa: E501
from zarban.service.openapi_client.rest import ApiException

class TestStats(unittest.TestCase):
    """Stats unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Stats
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = zarban.service.openapi_client.models.stats.Stats()  # noqa: E501
        if include_optional :
            return Stats(
                stablecoin_system = zarban.service.openapi_client.models.stablecoin_system_stats.StablecoinSystemStats(
                    system_surplus = null, 
                    system_debt = null, 
                    system_debt_ceiling = null, 
                    system_surplus_buffer = null, 
                    system_bad_debt = null, 
                    system_surplus_lot_size = null, ), 
                lendingpool = zarban.service.openapi_client.models.lendingpool_stats.LendingpoolStats(
                    total_available = null, 
                    total_borrows = null, 
                    total_market_size = null, )
            )
        else :
            return Stats(
                stablecoin_system = zarban.service.openapi_client.models.stablecoin_system_stats.StablecoinSystemStats(
                    system_surplus = null, 
                    system_debt = null, 
                    system_debt_ceiling = null, 
                    system_surplus_buffer = null, 
                    system_bad_debt = null, 
                    system_surplus_lot_size = null, ),
                lendingpool = zarban.service.openapi_client.models.lendingpool_stats.LendingpoolStats(
                    total_available = null, 
                    total_borrows = null, 
                    total_market_size = null, ),
        )

    def testStats(self):
        """Test Stats"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
