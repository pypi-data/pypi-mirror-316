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

from bandwidth.models.deferred_result import DeferredResult

class TestDeferredResult(unittest.TestCase):
    """DeferredResult unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DeferredResult:
        """Test DeferredResult
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        if include_optional:
            return DeferredResult(
                result = None,
                set_or_expired = True
            )
        else:
            return DeferredResult(
        )

    def testDeferredResult(self):
        """Test DeferredResult"""
        instance = self.make_instance(True)
        assert instance is not None
        assert isinstance(instance, DeferredResult)
        assert instance.result is None
        assert instance.set_or_expired == True

if __name__ == '__main__':
    unittest.main()
