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
