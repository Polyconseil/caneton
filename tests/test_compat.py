# -*- coding: utf-8 -*-
# Copyright © 2015 Polyconseil SAS
# SPDX-License-Identifier: BSD-3-Clause
#

from unittest import TestCase

import caneton.compat


class CompatTestCase(TestCase):

    def test_from_bytes(self):
        self.assertEqual(caneton.compat.int_from_bytes(b'\x00\x10', byteorder='big'), 16)

    def test_from_bytes_little_endian(self):
        self.assertEqual(caneton.compat.int_from_bytes(b'\x00\x10', byteorder='little'), 4096)

    def test_int_from_bytes_negative(self):
        self.assertEqual(caneton.compat.int_from_bytes(b'\xfc\x00', byteorder='big', signed=True), -1024)

    def test_int_from_bytes_signed(self):
        self.assertEqual(caneton.compat.int_from_bytes(b'\xfc\x00', byteorder='big', signed=False), 64512)

    def test_int_from_bytes_iterable(self):
        self.assertEqual(caneton.compat.int_from_bytes([255, 0, 0], byteorder='big'), 16711680)

    def test_from_bytes_cpython(self):
        # test suite taken from cpython code
        # https://hg.python.org/cpython/file/3.4/Lib/test/test_long.py#l1075

        def check(tests, byteorder, signed=False):
            for test, expected in tests.items():
                try:
                    self.assertEqual(
                        caneton.compat.int_from_bytes(test, byteorder, signed=signed),
                        expected
                    )
                except Exception:
                    raise AssertionError(
                        "failed to convert {0} with byteorder={1!r} and signed={2}"
                        .format(test, byteorder, signed)
                    )

        # Convert signed big-endian byte arrays to integers.
        tests1 = {
            b'': 0,
            b'\x00': 0,
            b'\x00\x00': 0,
            b'\x01': 1,
            b'\x00\x01': 1,
            b'\xff': -1,
            b'\xff\xff': -1,
            b'\x81': -127,
            b'\x80': -128,
            b'\xff\x7f': -129,
            b'\x7f': 127,
            b'\x00\x81': 129,
            b'\xff\x01': -255,
            b'\xff\x00': -256,
            b'\x00\xff': 255,
            b'\x01\x00': 256,
            b'\x7f\xff': 32767,
            b'\x80\x00': -32768,
            b'\x00\xff\xff': 65535,
            b'\xff\x00\x00': -65536,
            b'\x80\x00\x00': -8388608
        }
        check(tests1, 'big', signed=True)

        # Convert signed little-endian byte arrays to integers.
        tests2 = {
            b'': 0,
            b'\x00': 0,
            b'\x00\x00': 0,
            b'\x01': 1,
            b'\x00\x01': 256,
            b'\xff': -1,
            b'\xff\xff': -1,
            b'\x81': -127,
            b'\x80': -128,
            b'\x7f\xff': -129,
            b'\x7f': 127,
            b'\x81\x00': 129,
            b'\x01\xff': -255,
            b'\x00\xff': -256,
            b'\xff\x00': 255,
            b'\x00\x01': 256,
            b'\xff\x7f': 32767,
            b'\x00\x80': -32768,
            b'\xff\xff\x00': 65535,
            b'\x00\x00\xff': -65536,
            b'\x00\x00\x80': -8388608
        }
        check(tests2, 'little', signed=True)

        # Convert unsigned big-endian byte arrays to integers.
        tests3 = {
            b'': 0,
            b'\x00': 0,
            b'\x01': 1,
            b'\x7f': 127,
            b'\x80': 128,
            b'\xff': 255,
            b'\x01\x00': 256,
            b'\x7f\xff': 32767,
            b'\x80\x00': 32768,
            b'\xff\xff': 65535,
            b'\x01\x00\x00': 65536,
        }
        check(tests3, 'big', signed=False)

        # Convert integers to unsigned little-endian byte arrays.
        tests4 = {
            b'': 0,
            b'\x00': 0,
            b'\x01': 1,
            b'\x7f': 127,
            b'\x80': 128,
            b'\xff': 255,
            b'\x00\x01': 256,
            b'\xff\x7f': 32767,
            b'\x00\x80': 32768,
            b'\xff\xff': 65535,
            b'\x00\x00\x01': 65536,
        }
        check(tests4, 'little', signed=False)
