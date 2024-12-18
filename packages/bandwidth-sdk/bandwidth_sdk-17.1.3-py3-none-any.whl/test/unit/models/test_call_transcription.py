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

from bandwidth.models.call_transcription import CallTranscription

class TestCallTranscription(unittest.TestCase):
    """CallTranscription unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CallTranscription:
        """Test CallTranscription
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        instance = CallTranscription()
        if include_optional:
            return CallTranscription(
                detected_language = 'en-US',
                track = 'inbound',
                transcript = 'Hello World! This is an example.',
                confidence = 0.9
            )
        else:
            return CallTranscription(
        )

    def testCallTranscription(self):
        """Test CallTranscription"""
        instance = self.make_instance(True)
        assert instance is not None
        assert isinstance(instance, CallTranscription)
        assert instance.detected_language == 'en-US'
        assert instance.track == 'inbound'
        assert instance.transcript == 'Hello World! This is an example.'
        assert instance.confidence == 0.9

if __name__ == '__main__':
    unittest.main()
