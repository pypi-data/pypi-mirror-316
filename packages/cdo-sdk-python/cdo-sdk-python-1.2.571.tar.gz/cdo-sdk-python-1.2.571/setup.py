# coding: utf-8

"""
    Cisco Security Cloud Control API

    Use the documentation to explore the endpoints Security Cloud Control has to offer

    The version of the OpenAPI document: 1.5.0
    Contact: cdo.tac@cisco.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from setuptools import setup, find_packages  # noqa: H301

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
NAME = "cdo-sdk-python"
VERSION = "1.2.571"
PYTHON_REQUIRES = ">=3.7"
REQUIRES = [
    "urllib3 >= 1.25.3, < 2.1.0",
    "python-dateutil",
    "pydantic >= 2",
    "typing-extensions >= 4.7.1",
]

setup(
    name=NAME,
    version=VERSION,
    description="Cisco Security Cloud Control API",
    author="Cisco Security Cloud Control TAC",
    author_email="cdo.tac@cisco.com",
    url="",
    keywords=["OpenAPI", "OpenAPI-Generator", "Cisco Security Cloud Control API"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description_content_type='text/markdown',
    long_description=open('../../SDK-DESC.md', 'r', encoding='utf-8').read(),
    package_data={"cdo_sdk_python": ["py.typed"]},
)
