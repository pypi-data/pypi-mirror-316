# coding: utf-8

"""
    Bandwidth

    Bandwidth's Communication APIs

    The version of the OpenAPI document: 1.0.0
    Contact: letstalk@bandwidth.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import os
import sys
from setuptools import setup, find_packages  # noqa: H301

NAME = "bandwidth-sdk"
VERSION = os.environ['RELEASE_VERSION']

with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()

with open('requirements.txt') as f:
    REQUIRES = f.read().splitlines()

PYTHON_REQUIRES = ">=3.7"

setup(
    name=NAME,
    version=VERSION,
    description="Bandwidth",
    author="Bandwidth",
    author_email="letstalk@bandwidth.com",
    url="https://dev.bandwidth.com/sdks/python",
    keywords=["OpenAPI", "OpenAPI-Generator", "Bandwidth"],
    python_requires=PYTHON_REQUIRES,
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
