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

from bandwidth.models.message_delivered_callback_message import MessageDeliveredCallbackMessage

class TestMessageDeliveredCallbackMessage(unittest.TestCase):
    """MessageDeliveredCallbackMessage unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> MessageDeliveredCallbackMessage:
        """Test MessageDeliveredCallbackMessage
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        if include_optional:
            return MessageDeliveredCallbackMessage(
                id = '1661365814859loidf7mcwd4qacn7',
                owner = '+15553332222',
                application_id = '93de2206-9669-4e07-948d-329f4b722ee2',
                time = '2016-09-14T18:20:16Z',
                segment_count = 1,
                direction = 'in',
                to = ["+15552223333"],
                var_from = '+15553332222',
                text = 'Hello world',
                tag = 'custom string',
                media = ["https://dev.bandwidth.com/images/bandwidth-logo.png","https://dev.bandwidth.com/images/github_logo.png"],
                priority = 'default'
            )
        else:
            return MessageDeliveredCallbackMessage(
                id = '1661365814859loidf7mcwd4qacn7',
                owner = '+15553332222',
                application_id = '93de2206-9669-4e07-948d-329f4b722ee2',
                time = '2016-09-14T18:20:16Z',
                segment_count = 1,
                direction = 'in',
                to = ["+15552223333"],
                var_from = '+15553332222',
                text = 'Hello world',
                tag = 'custom string',
        )

    def testMessageDeliveredCallbackMessage(self):
        """Test MessageDeliveredCallbackMessage"""
        instance = self.make_instance(True)
        assert instance is not None
        assert isinstance(instance, MessageDeliveredCallbackMessage)
        assert instance.id == '1661365814859loidf7mcwd4qacn7'
        assert instance.owner == '+15553332222'
        assert instance.application_id == '93de2206-9669-4e07-948d-329f4b722ee2'
        assert isinstance(instance.time, datetime)
        assert instance.segment_count == 1
        assert instance.direction == 'in'
        assert instance.to == ["+15552223333"]
        assert instance.var_from == '+15553332222'
        assert instance.text == 'Hello world'
        assert instance.tag == 'custom string'
        assert instance.media == ["https://dev.bandwidth.com/images/bandwidth-logo.png","https://dev.bandwidth.com/images/github_logo.png"]
        assert instance.priority == 'default'

if __name__ == '__main__':
    unittest.main()
