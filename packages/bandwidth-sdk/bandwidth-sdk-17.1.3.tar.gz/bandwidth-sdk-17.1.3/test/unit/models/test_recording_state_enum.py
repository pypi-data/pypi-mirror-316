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

from bandwidth.models.recording_state_enum import RecordingStateEnum

class TestRecordingStateEnum(unittest.TestCase):
    """RecordingStateEnum unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testRecordingStateEnum(self):
        """Test RecordingStateEnum"""
        paused = RecordingStateEnum('paused')
        recording = RecordingStateEnum('recording')
        assert paused == 'paused'
        assert recording == 'recording'

if __name__ == '__main__':
    unittest.main()
