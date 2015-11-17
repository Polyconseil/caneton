#!/usr/bin/env python3
# Copyright (c) Polyconseil SAS. All rights reserved.

from setuptools import find_packages, setup

VERSION = '1.0.3'

setup(
    name="caneton",
    version=VERSION,
    author="Polyconseil dev team",
    author_email="autolib-dev@polyconseil.fr",
    description=("Decode CAN messages"),
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
        "Programming Language :: Python :: 3",
    ],
    test_suite='',
    include_package_data=True,
)
