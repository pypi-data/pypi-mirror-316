# coding: utf-8

"""
    Bandwidth

    Bandwidth's Communication APIs

    The version of the OpenAPI document: 1.0.0
    Contact: letstalk@bandwidth.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest
from datetime import datetime

from bandwidth.models.message_request import MessageRequest

class TestMessageRequest(unittest.TestCase):
    """MessageRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> MessageRequest:
        """Test MessageRequest
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        if include_optional:
            return MessageRequest(
                application_id = '93de2206-9669-4e07-948d-329f4b722ee2',
                to = ["+15554443333","+15552223333"],
                var_from = '+15551113333',
                text = 'Hello world',
                media = ["https://dev.bandwidth.com/images/bandwidth-logo.png","https://dev.bandwidth.com/images/github_logo.png"],
                tag = 'custom string',
                priority = 'default',
                expiration = '2021-02-01T11:29:18-05:00'
            )
        else:
            return MessageRequest(
                application_id = '93de2206-9669-4e07-948d-329f4b722ee2',
                to = ["+15554443333","+15552223333"],
                var_from = '+15551113333',
        )

    def testMessageRequest(self):
        """Test MessageRequest"""
        instance = self.make_instance(True)
        assert instance is not None
        assert isinstance(instance, MessageRequest)
        assert instance.application_id == '93de2206-9669-4e07-948d-329f4b722ee2'
        assert instance.to == ["+15554443333","+15552223333"]
        assert instance.var_from == '+15551113333'
        assert instance.text == 'Hello world'
        assert instance.media == ["https://dev.bandwidth.com/images/bandwidth-logo.png","https://dev.bandwidth.com/images/github_logo.png"]
        assert instance.tag == 'custom string'
        assert instance.priority == 'default'
        assert isinstance(instance.expiration, datetime)

if __name__ == '__main__':
    unittest.main()
