#!/usr/bin/env python
# Copyright (c) Polyconseil SAS. All rights reserved.

from setuptools import find_packages, setup

from caneton.version import VERSION

setup(
    name="caneton",
    version=VERSION,
    author="Polyconseil dev team",
    author_email="autolib-dev@polyconseil.fr",
    description="Decode CAN messages",
    license="BSD-3-Clause",
    keywords="CAN DBC",
    url="https://github.com/polyconseil/caneton",
    packages=find_packages(),
    long_description="",
    entry_points={
        'console_scripts': [
            'caneton-decode = caneton.cli:main',
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
    test_suite='',
    include_package_data=True,
)
