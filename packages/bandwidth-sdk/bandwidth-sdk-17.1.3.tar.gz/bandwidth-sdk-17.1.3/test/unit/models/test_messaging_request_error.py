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

from bandwidth.models.messaging_request_error import MessagingRequestError

class TestMessagingRequestError(unittest.TestCase):
    """MessagingRequestError unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> MessagingRequestError:
        """Test MessagingRequestError
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        if include_optional:
            return MessagingRequestError(
                type = '',
                description = ''
            )
        else:
            return MessagingRequestError(
                type = '',
                description = '',
        )

    def testMessagingRequestError(self):
        """Test MessagingRequestError"""
        instance = self.make_instance(True)
        assert instance is not None
        assert isinstance(instance, MessagingRequestError)
        assert instance.type == ''
        assert instance.description == ''

if __name__ == '__main__':
    unittest.main()
