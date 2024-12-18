# coding: utf-8

"""
    Cisco Security Cloud Control API

    Use the documentation to explore the endpoints Security Cloud Control has to offer

    The version of the OpenAPI document: 1.5.0
    Contact: cdo.tac@cisco.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from cdo_sdk_python.models.taglib_descriptor import TaglibDescriptor

class TestTaglibDescriptor(unittest.TestCase):
    """TaglibDescriptor unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> TaglibDescriptor:
        """Test TaglibDescriptor
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TaglibDescriptor`
        """
        model = TaglibDescriptor()
        if include_optional:
            return TaglibDescriptor(
                taglib_uri = '',
                taglib_location = ''
            )
        else:
            return TaglibDescriptor(
        )
        """

    def testTaglibDescriptor(self):
        """Test TaglibDescriptor"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
