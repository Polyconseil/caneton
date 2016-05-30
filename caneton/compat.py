# -*- coding: utf-8 -*-
# Copyright © 2015 Polyconseil SAS
# SPDX-License-Identifier: BSD-3-Clause
#

import sys

PY_VERSION = sys.version_info[0]

IS_PY3 = PY_VERSION == 3
IS_PY2 = not IS_PY3


def int_from_bytes(data, byteorder, signed=False):
    """Convert bytes to an integer

    Args:
        data: bytes, the bytes to convert
        byteorder: 'big' or 'little', indicates the endianness
        signed: indicates whether two’s complement is used to represent the integer.

    """
    if IS_PY3:
        return int.from_bytes(data, byteorder, signed=signed)

    if not len(data):
        return 0
    if byteorder == 'big':
        data = bytearray(reversed(data))
    if isinstance(data, str):
        data = bytearray(data)
    num = 0
    for offset, byte in enumerate(data):
        num += byte << (offset * 8)
    if signed and (data[-1] & 0x80):
        num = num - (2 ** (len(data) * 8))
    return num
