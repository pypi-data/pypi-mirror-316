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
from zarban.wallet.openapi_client.models.task_response import TaskResponse  # noqa: E501
from zarban.wallet.openapi_client.rest import ApiException

class TestTaskResponse(unittest.TestCase):
    """TaskResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TaskResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = zarban.wallet.openapi_client.models.task_response.TaskResponse()  # noqa: E501
        if include_optional :
            return TaskResponse(
                data = [
                    zarban.wallet.openapi_client.models.task.Task(
                        id = '1234567890', 
                        description = 'Complete your profile to earn rewards', 
                        points = 10, 
                        status = 'Pending', 
                        completed_at = zarban.wallet.openapi_client.models.timestamp.Timestamp(
                            jalaali = '1399-01-01T00:00:00Z', 
                            gregorian = '2020-01-01T00:00:00Z', ), )
                    ]
            )
        else :
            return TaskResponse(
                data = [
                    zarban.wallet.openapi_client.models.task.Task(
                        id = '1234567890', 
                        description = 'Complete your profile to earn rewards', 
                        points = 10, 
                        status = 'Pending', 
                        completed_at = zarban.wallet.openapi_client.models.timestamp.Timestamp(
                            jalaali = '1399-01-01T00:00:00Z', 
                            gregorian = '2020-01-01T00:00:00Z', ), )
                    ],
        )

    def testTaskResponse(self):
        """Test TaskResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
