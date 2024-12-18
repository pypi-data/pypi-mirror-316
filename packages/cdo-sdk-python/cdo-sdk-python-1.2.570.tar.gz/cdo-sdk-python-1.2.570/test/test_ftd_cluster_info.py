# coding: utf-8

"""
    CDO API

    Use the documentation to explore the endpoints CDO has to offer

    The version of the OpenAPI document: 1.3.0
    Contact: cdo.tac@cisco.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from cdo_sdk_python.models.ftd_cluster_info import FtdClusterInfo

class TestFtdClusterInfo(unittest.TestCase):
    """FtdClusterInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> FtdClusterInfo:
        """Test FtdClusterInfo
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `FtdClusterInfo`
        """
        model = FtdClusterInfo()
        if include_optional:
            return FtdClusterInfo(
                control_node = cdo_sdk_python.models.cluster_node.ClusterNode(
                    serial = 'JAD24500xxx', 
                    software_version = '7.4.1', 
                    uid_on_fmc = '6131daad-e813-4b8f-8f42-be1e241e8cdb', 
                    status = 'NORMAL', ),
                data_nodes = [
                    cdo_sdk_python.models.cluster_node.ClusterNode(
                        serial = 'JAD24500xxx', 
                        software_version = '7.4.1', 
                        uid_on_fmc = '6131daad-e813-4b8f-8f42-be1e241e8cdb', 
                        status = 'NORMAL', )
                    ]
            )
        else:
            return FtdClusterInfo(
        )
        """

    def testFtdClusterInfo(self):
        """Test FtdClusterInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
